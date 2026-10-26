#!/usr/bin/env python3
"""Pusula kitap paketinin yapısını denetler; model veya uygulama çalıştırmaz."""
from pathlib import Path
import json
import re
import sys
from urllib.parse import unquote


def validate(root):
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def read_json(name):
        try:
            return json.loads((root / name).read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc:
            errors.append(f'{name}: {exc}')
            return {}

    curriculum = read_json('curriculum.json')
    coverage = read_json('coverage.json')
    sources = read_json('sources.json')
    skills = read_json('skill-tests.json')
    lessons = curriculum.get('lessons', [])
    ids = [x.get('id') for x in lessons]
    require(ids == [f'U{n:02}' for n in range(1, 37)], 'Uygulama kimlikleri U01–U36 olmalı.')
    produced = {'brief.md', 'fixtures/atolye-kaynaklari.json'}
    for lesson in lessons:
        label = lesson.get('id', '?')
        for field in ('title', 'task', 'acceptance', 'inputs', 'outputs', 'prompt'):
            require(bool(lesson.get(field)), f'{label}: {field} eksik.')
        for path in lesson.get('inputs', []):
            available = path in produced or any(
                path.startswith(p) for p in produced if p.endswith('/')
            ) or (path.endswith('/') and any(p.startswith(path) for p in produced))
            require(available, f'{label}: girdi daha önce üretilmiyor: {path}')
        produced.update(lesson.get('outputs', []))
        prompt = root / lesson.get('prompt', '__missing__')
        require(prompt.is_file(), f'{label}: prompt dosyası yok.')
        if prompt.is_file():
            body = prompt.read_text(encoding='utf-8')
            for heading in ('## Girdiler', '## Üretilecek dosyalar', '## Üretim', '## Kontrol', '## Düzeltme', '## Tamamlanma kanıtı'):
                require(heading in body, f'{label}: {heading} eksik.')
            for path in lesson.get('inputs', []) + lesson.get('outputs', []):
                require(path in body, f'{label}: kayıt/prompt yolu uyuşmuyor: {path}')
        require(lesson.get('execution_status') == 'not_run', f'{label}: başlangıç paketinde koşu kanıtı yok.')

    chapters = coverage.get('chapters', [])
    expected = {f'C{v}-B{n:02}' for v, count in [(1, 17), (2, 14), (3, 14), (4, 15)] for n in range(1, count + 1)}
    expected.update(f'CC-B{n:02}' for n in range(1, 41))
    actual = [x.get('id') for x in chapters]
    require(len(actual) == len(set(actual)), 'Yinelenen kaynak bölüm kimliği.')
    require(set(actual) == expected, '100 kaynak bölümün kimlik kümesi eksik veya fazla.')
    require(coverage.get('full_text_audit_complete') is False, 'Başlangıç eşlemesi tam metin denetimi sayılmamalı.')
    for chapter in chapters:
        require(bool(chapter.get('lessons')), f"{chapter.get('id')}: uygulama eşlemesi yok.")
        require(set(chapter.get('lessons', [])) <= set(ids), f"{chapter.get('id')}: bilinmeyen uygulama.")
        require(bool(re.fullmatch('[0-9a-f]{64}', chapter.get('sha256', ''))), f"{chapter.get('id')}: kaynak özeti eksik.")

    for source in sources.get('sources', []):
        require(source.get('url', '').startswith('https://'), 'Kaynak URL biçimi geçersiz.')
        require(set(source.get('lessons', [])) <= set(ids), f"{source.get('id')}: bilinmeyen uygulama.")
    require(sources.get('accessed_on') == '2026-10-26', 'Kaynak erişim tarihi eksik.')

    skill_files = sorted(root.glob('skills/*/SKILL.md'))
    require(len(skill_files) == 2, 'İki skill giriş dosyası bekleniyor.')
    for path in skill_files:
        body = path.read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---\n', body, re.S)
        require(bool(match), f'{path.name}: YAML ön bilgisi yok.')
        if match:
            name = re.search(r'^name: (.+)$', match[1], re.M)
            desc = re.search(r'^description: (.+)$', match[1], re.M)
            require(bool(name) and name[1] == path.parent.name, f'{path}: ad/dizin uyuşmazlığı.')
            require(bool(name) and len(name[1]) <= 64 and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name[1])), f'{path}: skill adı geçersiz.')
            require(bool(desc) and 0 < len(desc[1]) <= 1024, f'{path}: açıklama eksik veya uzun.')
    require(len(skills.get('cases', [])) == 6, 'Altı skill deneme vakası bekleniyor.')
    for case in skills.get('cases', []):
        require(case.get('observed') is None, f"{case.get('id')}: gözlenmemiş sonuç doldurulmuş.")
        require((root / 'skills' / case.get('skill', '') / 'SKILL.md').is_file(), 'Vakanın skill dosyası yok.')

    for path in root.rglob('*.json'):
        try:
            json.loads(path.read_text(encoding='utf-8'))
        except ValueError as exc:
            errors.append(f'{path.relative_to(root)}: JSON bozuk: {exc}')
    for path in root.rglob('*.md'):
        body = path.read_text(encoding='utf-8')
        body = re.sub(r'```.*?```', '', body, flags=re.S)
        for target in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', body):
            if re.match(r'^(?:https?://|mailto:|#)', target):
                continue
            target = unquote(target.split('#', 1)[0])
            resolved = (path.parent / target).resolve()
            require(resolved.is_relative_to(root.resolve()), f'{path.relative_to(root)}: paket dışı bağlantı {target}')
            require(resolved.exists(), f'{path.relative_to(root)}: eksik bağlantı {target}')
        require('/Users/' not in body, f'{path.relative_to(root)}: kişisel mutlak yol var.')
    return errors, {'lessons': len(lessons), 'source_chapters': len(chapters), 'skills': len(skill_files), 'skill_cases': len(skills.get('cases', [])), 'sources': len(sources.get('sources', []))}


if __name__ == '__main__':
    package = Path(__file__).resolve().parents[1]
    try:
        problems, counts = validate(package)
    except (KeyError, TypeError, AttributeError) as exc:
        print(f'FAIL: beklenmeyen kayıt yapısı: {exc}', file=sys.stderr)
        raise SystemExit(1)
    if problems:
        print('\n'.join(f'FAIL: {error}' for error in problems), file=sys.stderr)
        raise SystemExit(1)
    print('PASS: ' + json.dumps(counts, ensure_ascii=False))
    print('Kapsam: paket yapısı. Model davranışı, uygulama kodu ve anlamsal kabul sınanmadı.')
