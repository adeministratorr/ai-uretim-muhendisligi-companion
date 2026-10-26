#!/usr/bin/env python3
"""Check P02 editorial references; no product or model calls."""
import json
from pathlib import Path


def validate(package):
    def read(name):
        return json.loads((package / name).read_text())

    lessons = {x['id']: x for x in read('curriculum.json')['lessons']}
    source_rows = read('sources.json')['sources']
    source_ids = {s['id'] for s in source_rows}
    assert len(source_ids) == len(source_rows), 'Duplicate primary source id'
    assert len({s['url'].rstrip('/') for s in source_rows}) == len(source_rows), 'Duplicate primary URL'
    inv = read('editorial/approach-inventory.json')
    proposals = {p['id']: p for p in inv['proposals']}
    assert set(proposals) == {f'proposal-{n:02}' for n in range(1, 13)}
    terms = inv['terms']
    assert len({t['id'] for t in terms}) == len(terms) == 121
    assert len({t['name'] for t in terms}) == len(terms)
    for row in list(proposals.values()) + terms:
        assert row['lesson_ids'] and set(row['lesson_ids']) <= set(lessons), row['id']
        assert set(row['source_ids']) <= source_ids, row['id']
        assert row['runtime_status'] == 'not_run', row['id']
        assert row['author_review'] == 'pending', row['id']
        assert row['rationale'], row['id']
    for p in proposals.values():
        assert p['source_ids'] and p['acceptance'], p['id']
        outputs = {path for uid in p['lesson_ids'] for path in lessons[uid]['outputs']}
        assert set(p['output_paths']) <= outputs, p['id']
    aliases = {a['alias'] for a in inv['attachments']}
    for term in terms:
        assert term['proposal_id'] is None or term['proposal_id'] in proposals, term['id']
        assert term['occurrences'] and term['acceptance_boundary'], term['id']
        for occurrence in term['occurrences']:
            assert occurrence['attachment_alias'] in aliases and occurrence['line'] > 0, term['id']
    objectives = read('editorial/learning-objectives.json')['objectives']
    cases = {c['id']: c for c in read('editorial/pilot-acceptance-cases.json')['cases']}
    resolutions = [o for o in objectives if o.get('editorial_resolution', {}).get('phase') == 'P02']
    assert len(resolutions) == 27
    assert sum(o['editorial_resolution']['disposition'] == 'moved_to_later_lesson' for o in resolutions) == 2
    for objective in resolutions:
        r = objective['editorial_resolution']
        assert r['previous']['status'] == 'gap' and r['previous']['gap_reason'], objective['id']
        assert objective['status'] == 'mapped' and objective['runtime_status'] == 'not_run'
        assert r['prompt'] in {lessons[uid]['prompt'] for uid in objective['lesson_ids']}, objective['id']
        assert (package / r['prompt']).is_file(), objective['id']
        assert r['acceptance_case'] == objective['acceptance_case']
        assert cases[r['acceptance_case']]['objective_id'] == objective['id']
    source_chapters = {s['source_id'] for s in read('editorial/source-map.json')['sources']}
    updates = read('editorial/book-updates.json')['updates']
    assert len({u['id'] for u in updates}) == len(updates) == 15
    for u in updates:
        assert set(u['source_chapters']) <= source_chapters, u['id']
        assert u['status'] == 'proposed' and u['source_modified'] is False
    return {'proposals': len(proposals), 'terms': len(terms), 'gap_resolutions': len(resolutions), 'book_update_proposals': len(updates)}


if __name__ == '__main__':
    print('PASS: ' + json.dumps(validate(Path(__file__).resolve().parents[1]), ensure_ascii=False))
    print('Editorial relationship check only; semantic acceptance and runtime remain separate.')
