#!/usr/bin/env python3
"""Build a local-source inventory; reading evidence is supplied, never inferred.

Usage: python3 editorial/build_source_audit.py --engineering ROOT --claude ROOT
       --reader REPORT [--reader REPORT ...]
Only editorial JSON outputs are written. Source repositories remain read-only.
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def headings(text):
    result = []
    fence = None
    comment = False
    for number, line in enumerate(text.splitlines(), 1):
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
            result.append({'line': number, 'level': len(match[1]), 'heading': match[2]})
    return result


def git(root, *args):
    p = subprocess.run(['git', '-C', str(root), *args], text=True, capture_output=True)
    return p.stdout.strip() if p.returncode == 0 else None


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engineering', required=True, type=Path)
    parser.add_argument('--claude', required=True, type=Path)
    parser.add_argument('--reader', action='append', default=[], type=Path)
    parser.add_argument('--overrides', type=Path)
    args = parser.parse_args()
    package = Path(__file__).resolve().parents[1]
    editorial = package / 'editorial'
    coverage = json.loads((package / 'coverage.json').read_text())
    curriculum = json.loads((package / 'curriculum.json').read_text())
    lesson_ids = {x['id'] for x in curriculum['lessons']}
    source_roots = {'engineering': args.engineering, 'claude': args.claude}
    repo_ids = {}
    for kind, root in source_roots.items():
        repo_ids[kind] = {
            'alias': 'engineering-book' if kind == 'engineering' else 'claude-guide',
            'repository_name': root.name,
            'git_head': git(root, 'rev-parse', 'HEAD'),
            'origin_url': git(root, 'config', '--get', 'remote.origin.url'),
            'canonical_basis': (
                'P01 brief specifies content/cilt*/bolum*/bolum*.md as canonical source; generated editions and panel copies excluded.'
                if kind == 'engineering' else
                'README.md identifies this repository as book source; P01 brief selects docs/ chapter Markdown, excluding dist/ and panel copies.'
            ),
        }
    evidence = {}
    overrides = json.loads(args.overrides.read_text())['objectives'] if args.overrides else {}
    for report in args.reader:
        data = json.loads(report.read_text())
        for chapter in data['chapters']:
            sid = chapter['source_id']
            if sid in evidence:
                raise ValueError(f'Duplicate reader evidence: {sid}')
            evidence[sid] = chapter
    records, logs, objectives, cases = [], [], [], []
    for chapter in coverage['chapters']:
        sid = chapter['id']
        kind = 'engineering' if chapter['source_kind'] == 'engineering' else 'claude'
        root = source_roots[kind]
        source = root / chapter['source_path']
        raw = source.read_bytes()
        text = raw.decode('utf-8')
        current = sha(raw)
        baseline = chapter['sha256']
        pilot = any(int(x[1:]) <= 8 for x in chapter['lessons'])
        group = 'U01-U08' if pilot else f'U{((min(int(x[1:]) for x in chapter["lessons"]) - 1) // 8) * 8 + 1:02}-U{min(36, ((min(int(x[1:]) for x in chapter["lessons"]) - 1) // 8 + 1) * 8):02}'
        hs = headings(text)
        reader = evidence.get(sid)
        if reader:
            if reader['sha256'] != current or not reader['full_read']:
                raise ValueError(f'Incomplete or stale reader evidence: {sid}')
            if reader['source_path'] != chapter['source_path']:
                raise ValueError(f'Source path differs: {sid}')
            declared = {re.sub(r'^#+\s*', '', h['heading']) for h in reader['headings']}
            missing = {h['heading'] for h in hs if h['level'] == 2} - declared
            if missing:
                raise ValueError(f'Unassigned level-2 headings: {sid}: {missing}')
            for o in reader['objectives']:
                if o['source_id'] != sid or not set(o['lesson_ids']) <= lesson_ids:
                    raise ValueError(f'Invalid objective links: {o["id"]}')
                if o['status'] not in {'mapped', 'gap', 'out_of_scope'}:
                    raise ValueError(f'Invalid status: {o["id"]}')
                if o['status'] == 'mapped' and (not o['output_paths'] or not o['acceptance_case'] or not o['lesson_ids']):
                    raise ValueError(f'Mapped objective lacks concrete mapping: {o["id"]}')
                if o['status'] != 'mapped' and not o['gap_reason']:
                    raise ValueError(f'Gap lacks reason: {o["id"]}')
                obj = dict(o)
                obj.update(overrides.get(o['id'], {}))
                case_body = str(obj.get('acceptance_case', {}))
                is_pilot_objective = any(int(l[1:]) <= 8 for l in obj['lesson_ids'])
                if not is_pilot_objective and (
                    'gerekli dayanak, kapsam veya insan denetimi eksik' in case_body
                    or 'Olumlu örnek kabul edilir; olumsuz örnek reddedilir' in case_body
                    or obj.get('acceptance_case', {}).get('design_status') == 'needs_design'
                ):
                    obj['reader_status'] = obj['status']
                    obj['status'] = 'gap'
                    obj['acceptance_status'] = 'needs_design'
                    obj['gap_reason'] = (obj.get('gap_reason') or '') + ' İleri uygulama için hedefe özgü sentetik girdi, yanlış aday ve kabul kararı tasarlanmalı; genel kabul cümlesi yeterli kanıt değildir.'
                if is_pilot_objective and 'acceptance_status' not in obj:
                    obj['acceptance_status'] = 'proposed_concrete'
                case = obj.pop('acceptance_case')
                if case:
                    case = dict(case)
                    if 'scenario' not in case and 'positive_candidate' in case:
                        case['scenario'] = {'positive': case['positive_candidate'], 'negative': case['negative_candidate']}
                    if 'expected' not in case and 'verdict' in case:
                        case['expected'] = case['verdict']
                    obj['acceptance_case'] = case['id']
                    cases.append({**case, 'objective_id': o['id'], 'lesson_ids': obj['lesson_ids'], 'design_status': obj.get('acceptance_status', 'proposed'), 'runtime_status': 'not_run', 'observed': None})
                else:
                    obj['acceptance_case'] = None
                obj['runtime_status'] = 'not_run'
                obj['source_revision'] = current
                objectives.append(obj)
            logs.append({
                'source_id': sid, 'source_path': chapter['source_path'], 'sha256': current,
                'full_read': True, 'lines_read': reader['lines_read'],
                'headings': reader['headings'], 'notes': reader.get('notes', []),
                'evidence_kind': 'reader_attestation_with_ranges_and_content_dispositions',
            })
        records.append({
            'source_id': sid, 'source_repo': repo_ids[kind]['alias'],
            'source_path': chapter['source_path'], 'title': chapter['title'],
            'baseline_sha256': baseline, 'current_sha256': current,
            'revision_status': 'unchanged' if baseline == current else 'changed',
            'revisions': [{'kind': 'coverage_baseline', 'sha256': baseline}, {'kind': 'current_working_tree', 'sha256': current, 'observed_on': '2026-10-26'}],
            'canonical_reason': repo_ids[kind]['canonical_basis'],
            'revision_basis': 'Current file bytes; repository HEAD identifies the checkout, not a claim of a clean working tree.',
            'review_status': 'full_read' if reader else 'pending_full_read',
            'planned_audit_group': group, 'lesson_ids': chapter['lessons'],
            'audited_lesson_ids': sorted({l for o in objectives if o['source_id'] == sid for l in o['lesson_ids']}),
            'pilot': pilot, 'bytes': len(raw), 'line_count': len(text.splitlines()),
            'headings': hs,
        })
    for name, rows in [('objective', objectives), ('case', cases)]:
        ids = [x['id'] for x in rows]
        if len(ids) != len(set(ids)):
            raise ValueError(f'Duplicate {name} IDs')
    if not set(evidence) <= {r['source_id'] for r in records}:
        raise ValueError('Unknown source in reader evidence')
    pilot_read_complete = all(not s['pilot'] or s['review_status'] == 'full_read' for s in records)
    pilot_gaps = sum(o['status'] == 'gap' and any(int(l[1:]) <= 8 for l in o['lesson_ids']) for o in objectives)
    source_map = {'schema_version': 1, 'observed_on': '2026-10-26', 'full_text_audit_complete': len(logs) == 100,
                  'audit_status': 'audit_complete' if pilot_read_complete else 'audit_incomplete',
                  'audit_scope': '100-source revision inventory and 31-source U01-U08 full-reading pilot',
                  'pilot_gate_status': 'pilot_gap_resolution_pending' if pilot_gaps or not pilot_read_complete else 'pilot_teaching_mapping_complete',
                  'pilot_gap_count': pilot_gaps,
                  'scope_note': 'Hash and heading extraction is inventory only. Full read requires separate reader evidence. No runtime or external-primary-source verification is asserted.',
                  'repositories': repo_ids, 'sources': records}
    write(editorial / 'source-map.json', source_map)
    write(editorial / 'pilot-reading-log.json', {'schema_version': 1, 'full_read_count': len(logs), 'pilot_total': sum(r['pilot'] for r in records), 'chapters': logs})
    write(editorial / 'learning-objectives.json', {'schema_version': 1, 'mapped_meaning': 'Editorial teaching assignment; does not assert execution or successful learning.', 'objectives': objectives})
    write(editorial / 'pilot-acceptance-cases.json', {'schema_version': 1, 'case_kind': 'synthetic_proposed_acceptance', 'runtime_status': 'not_run', 'cases': cases})
    print(json.dumps({'sources': len(records), 'changed': sum(x['revision_status'] == 'changed' for x in records), 'full_read': len(logs), 'objectives': len(objectives), 'cases': len(cases)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
