#!/usr/bin/env python3
"""Check editorial links and evidence claims, without running the Pusula product."""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


def source_headings(text):
    """Read real Markdown headings, excluding fenced examples and comments."""
    result, fence, comment = [], None, False
    for line in text.splitlines():
        if '<!--' in line:
            comment = True
        if comment:
            if '-->' in line:
                comment = False
            continue
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = marker[1][0]
            elif fence == marker[1][0]:
                fence = None
            continue
        match = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
        if fence is None and match:
            result.append({'level': len(match[1]), 'heading': match[2]})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--books-root', type=Path, required=True)
    parser.add_argument('--guide-root', type=Path, required=True)
    args = parser.parse_args()
    source_roots = {'engineering-book': args.books_root, 'claude-guide': args.guide_root}
    package = Path(__file__).resolve().parents[1]
    editorial = package / 'editorial'

    def read(name):
        return json.loads((editorial / name).read_text())

    sm = read('source-map.json')
    logs = read('pilot-reading-log.json')
    lo = read('learning-objectives.json')['objectives']
    cases = read('pilot-acceptance-cases.json')['cases']
    coverage = json.loads((package / 'coverage.json').read_text())
    lessons = {x['id']: x for x in json.loads((package / 'curriculum.json').read_text())['lessons']}
    sources = {s['source_id']: s for s in sm['sources']}
    assert len(sources) == len(sm['sources']) == 100
    assert set(sources) == {c['id'] for c in coverage['chapters']}
    assert sm['full_text_audit_complete'] is False
    assert coverage['full_text_audit_complete'] is False
    assert len([s for s in sources.values() if s['pilot']]) == 31
    assert len([s for s in sources.values() if s['review_status'] == 'full_read']) == len(logs['chapters'])
    assert len({x['source_id'] for x in logs['chapters']}) == len(logs['chapters'])
    live_headings = {}
    for s in sources.values():
        assert re.fullmatch('[a-f0-9]{64}', s['baseline_sha256'])
        assert re.fullmatch('[a-f0-9]{64}', s['current_sha256'])
        assert s['planned_audit_group']
        assert s['source_path'] and not s['source_path'].startswith('/')
        assert s['source_repo'] in {r['alias'] for r in sm['repositories'].values()}
        baseline = next(c for c in coverage['chapters'] if c['id'] == s['source_id'])
        assert baseline['sha256'] == s['baseline_sha256'], 'Baseline overwritten'
        assert s['revisions'][0]['sha256'] == s['baseline_sha256']
        assert s['revisions'][-1]['sha256'] == s['current_sha256']
        root = source_roots[s['source_repo']].resolve()
        source = (root / s['source_path']).resolve()
        assert source.is_relative_to(root), f'Source path escapes checkout: {s["source_id"]}'
        raw = source.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == s['current_sha256'], f'Source revision changed: {s["source_id"]}'
        assert len(raw) == s['bytes'], f'Source size changed: {s["source_id"]}'
        text = raw.decode('utf-8')
        assert len(text.splitlines()) == s['line_count'], f'Source lines changed: {s["source_id"]}'
        if s['review_status'] == 'full_read':
            live_headings[s['source_id']] = source_headings(text)
    for log in logs['chapters']:
        s = sources[log['source_id']]
        assert log['full_read'] is True
        assert log['sha256'] == s['current_sha256']
        ranges = log['lines_read']
        if isinstance(ranges, dict):
            ranges = [[ranges['start'], ranges['end']]]
        reached = set()
        for start, end in ranges:
            assert 1 <= start <= end <= s['line_count']
            reached.update(range(start, end + 1))
        assert len(reached) == s['line_count'], f'Incomplete line coverage: {s["source_id"]}'
        actual_headings = live_headings[s['source_id']]
        h2 = {h['heading'] for h in actual_headings if h['level'] == 2}
        declared = {re.sub(r'^#+\s*', '', h['heading']) for h in log['headings']}
        assert h2 <= declared, f'Missing heading disposition: {s["source_id"]}'
        assert declared <= {h['heading'] for h in actual_headings}, f'Unknown heading: {s["source_id"]}'
        for h in log['headings']:
            assert h['disposition'] in {'pilot', 'later', 'context'}
            assert set(h['lesson_ids']) <= set(lessons)
            assert h['reason']
    assert len({x['id'] for x in lo}) == len(lo)
    case_by_id = {x['id']: x for x in cases}
    assert len(case_by_id) == len(cases)
    for o in lo:
        s = sources[o['source_id']]
        assert s['review_status'] == 'full_read'
        assert re.sub(r'^#+\s*', '', o['heading']) in {h['heading'] for h in live_headings[o['source_id']]}, o['id']
        assert o['source_revision'] == s['current_sha256']
        assert o['runtime_status'] == 'not_run'
        assert o['status'] in {'mapped', 'gap', 'out_of_scope'}
        assert set(o['lesson_ids']) <= set(lessons) and o['lesson_ids']
        allowed = [p for l in o['lesson_ids'] for p in lessons[l]['outputs']]
        for output in o['output_paths']:
            assert any(output == a or (a.endswith('/') and output.startswith(a)) for a in allowed), (o['id'], output)
        if o['status'] == 'mapped':
            assert o['output_paths'] and o['acceptance_case']
            assert o.get('acceptance_status') != 'needs_design'
        else:
            assert o['gap_reason']
        if o['acceptance_case']:
            c = case_by_id[o['acceptance_case']]
            assert c['objective_id'] == o['id']
            assert c['runtime_status'] == 'not_run' and c['observed'] is None
            assert c['scenario'] and c['expected']
            if any(int(l[1:]) <= 8 for l in o['lesson_ids']):
                assert o.get('acceptance_status') == 'proposed_concrete', o['id']
                if isinstance(c['scenario'], str):
                    paired = 'Olumlu:' in c['scenario'] and 'Olumsuz:' in c['scenario']
                    candidates = 'Fixture' in c['scenario'] and 'Doğru aday:' in c['scenario'] and 'Verdict:' in str(c['expected'])
                    assert paired or candidates, o['id']
                else:
                    assert c['scenario'].get('positive') and c['scenario'].get('negative'), o['id']
                assert 'gerekli dayanak, kapsam veya insan denetimi eksik' not in str(c['scenario'])
    for f in editorial.rglob('*'):
        if f.suffix in {'.json', '.md'}:
            assert '/Users/' not in f.read_text(), f'Personal absolute path: {f.name}'
    counts = {
        'sources': len(sources), 'baseline_changed': sum(s['revision_status'] == 'changed' for s in sources.values()),
        'full_read': len(logs['chapters']), 'pilot_sources': 31,
        'objectives': len(lo), 'objective_status': dict(Counter(o['status'] for o in lo)),
        'acceptance_cases': len(cases), 'runtime': 'not_run',
        'pending_full_read': sum(s['review_status'] == 'pending_full_read' for s in sources.values()),
        'fresh_source_hashes_checked': len(sources), 'live_pilot_headings_checked': len(live_headings),
    }
    print('PASS: ' + json.dumps(counts, ensure_ascii=False))
    print('Structural evidence check only; reader attestations and semantic judgments still require review.')


if __name__ == '__main__':
    main()
