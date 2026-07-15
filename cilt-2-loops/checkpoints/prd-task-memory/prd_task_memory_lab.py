"""PRD, TASKS.md ve DECISIONS.md dosyalarını ortak ölçütlerle doğrular.

volume: 2
chapter: 08
book_section: "8.2-8.6 PRD, 8.10 Kabul Kriterleri, 8.11-8.13 TASKS.md ve 8.15 Decision Log"
concepts:
  - PRD
  - EARS benzeri kabul kriteri
  - görev parçalama
  - decision log
objectives:
  - "LO-8.2"
  - "LO-8.4"
  - "LO-8.5"
  - "LO-8.6"
last_verified: "2026-07"

Gömülü Vardiya belgeleri kurgusaldır. Doğrulayıcı belge yapısını denetler; ürün
kararlarının doğruluğunu veya görevin gerçekten tamamlandığını kanıtlamaz.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
from typing import Sequence


REQUIRED_PRD_SECTIONS = (
    "Amaç",
    "Hedef Kullanıcı",
    "Kapsam",
    "Teknik Kısıtlar",
    "Out-of-Scope",
    "Başarı Kriterleri",
)

SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TASK_PATTERN = re.compile(r"^\s*-\s+\[([ xX~])\]\s+(.+?)\s*$")
EARS_PATTERN = re.compile(r"\b\w+m(?:alı|eli)(?:dır|dir)?\b", re.IGNORECASE)


REPRESENTATIVE_PRD = """# Vardiya — İzin Talebi PRD

## Amaç

Çalışanın izin talebini kayıt altına alarak vardiya planındaki çakışmaları görünür kılmak.

## Hedef Kullanıcı

Vardiyalı çalışan ve izin taleplerini görüntüleyen küçük işletme sahibi.

## Kapsam

- Vardiyalı çalışan olarak, belirli bir tarih için izin talebi oluşturabilmek istiyorum ki işletme sahibi planlamayı buna göre yapabilsin.
- Küçük işletme sahibi olarak, açık izin taleplerini listeleyebilmek istiyorum ki vardiya planındaki çakışmaları görebileyim.

## Teknik Kısıtlar

- Mevcut kimlik doğrulama sistemi kullanılacak.
- Yeni paket veya mikroservis eklenmeyecek.

## Out-of-Scope

- İzin talebini onaylama veya reddetme akışı bu çalışmaya dahil değildir.

## Başarı Kriterleri

- Ne zaman bir çalışan geçmiş bir tarih için talep oluşturursa, sistem hata göstermeli ve talebi kaydetmemelidir.
- Ne zaman geçerli bir talep kaydedilirse, sistem bu talebi işletme sahibinin listesinde göstermelidir.
"""


REPRESENTATIVE_TASKS = """# TASKS.md

- [x] İzin talebi veri modelini tanımla — doğrulama: `test_leave_request_schema`
- [x] Talep oluşturma uç noktasını ekle — doğrulama: `test_create_leave_request`
- [~] Talep listeleme uç noktasını ekle
- [ ] Geçmiş tarih denetimini uygula
- [ ] API davranış testlerini tamamla
"""


REPRESENTATIVE_DECISIONS = """# DECISIONS.md

| Tarih | Karar | Gerekçe |
|---|---|---|
| 2026-06-24 | Bildirimler yalnızca e-posta ile gönderilecek | Push bildirimi altyapısı bu aşamada gereksiz maliyet getiriyor. |
| 2026-07-02 | İzin onayı ayrı bir modülde ele alınacak | Onay süreci farklı roller gerektiriyor ve bu özelliğin kapsamını büyütüyor. |
"""


@dataclass(frozen=True)
class ValidationReport:
    """Belge üçlüsünün sayısal özetini ve bulunan sorunları taşır."""

    prd_section_count: int
    user_story_count: int
    task_count: int
    completed_task_count: int
    decision_count: int
    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        """Hiç hata yoksa kabul kriterinin karşılandığını bildirir."""

        return not self.errors


def _extract_sections(markdown: str) -> dict[str, str]:
    """İkinci düzey Markdown başlıklarını içerikleriyle eşleştirir."""

    matches = list(SECTION_PATTERN.finditer(markdown))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        sections[match.group(1).strip().casefold()] = markdown[start:end].strip()
    return sections


def _bullet_lines(text: str) -> list[str]:
    """Bir bölümdeki dolu Markdown liste maddelerini döndürür."""

    return [
        line.strip()[2:].strip()
        for line in text.splitlines()
        if line.strip().startswith("- ") and line.strip()[2:].strip()
    ]


def _validate_prd(prd: str) -> tuple[list[str], int, int]:
    """PRD başlıklarını, user story'leri ve kabul kriterini denetler."""

    errors: list[str] = []
    sections = _extract_sections(prd)
    present_count = 0
    for heading in REQUIRED_PRD_SECTIONS:
        content = sections.get(heading.casefold())
        if content is None:
            errors.append(f'PRD bölümünde "{heading}" başlığı eksik.')
        elif not content.strip():
            errors.append(f'PRD bölümünde "{heading}" başlığı boş bırakılamaz.')
        else:
            present_count += 1

    scope = sections.get("kapsam", "")
    user_stories = [
        item
        for item in _bullet_lines(scope)
        if " olarak" in item.casefold() and "istiyorum ki" in item.casefold()
    ]
    if len(user_stories) < 2:
        errors.append(
            "PRD Kapsam bölümü, rolü ve sonucu yazılmış en az iki user story içermelidir."
        )

    out_of_scope = _bullet_lines(sections.get("out-of-scope", ""))
    if not out_of_scope:
        errors.append("PRD Out-of-Scope bölümü en az bir açık liste maddesi içermelidir.")

    acceptance_items = _bullet_lines(sections.get("başarı kriterleri", ""))
    has_ears_criterion = any(
        (item.casefold().startswith("ne zaman ") or item.casefold().startswith("eğer "))
        and "sistem" in item.casefold()
        and EARS_PATTERN.search(item)
        for item in acceptance_items
    )
    if not has_ears_criterion:
        errors.append(
            "Başarı Kriterleri, koşulu ve sistem davranışını yazan en az bir EARS benzeri madde içermelidir."
        )

    return errors, present_count, len(user_stories)


def _validate_tasks(tasks: str) -> tuple[list[str], int, int]:
    """Görev sayısını, durum işaretlerini ve doğrulama notlarını denetler."""

    errors: list[str] = []
    parsed_tasks: list[tuple[str, str]] = []
    malformed_lines: list[str] = []

    for line in tasks.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- ["):
            continue
        match = TASK_PATTERN.match(line)
        if match is None:
            malformed_lines.append(stripped)
        else:
            parsed_tasks.append((match.group(1).casefold(), match.group(2).strip()))

    if malformed_lines:
        errors.append(
            "TASKS.md yalnızca [ ], [~] veya [x] durum işaretlerini kullanmalıdır."
        )
    if len(parsed_tasks) < 5:
        errors.append("TASKS.md en az beş durumlu görev içermelidir.")

    normalized_descriptions = [description.casefold() for _, description in parsed_tasks]
    if len(normalized_descriptions) != len(set(normalized_descriptions)):
        errors.append("TASKS.md aynı görev satırını birden fazla kez içermemelidir.")

    completed = [description for status, description in parsed_tasks if status == "x"]
    for description in completed:
        verification = description.casefold().partition("doğrulama:")
        if not verification[1] or not verification[2].strip():
            errors.append(
                f'Tamamlanan görev doğrulama notu taşımalıdır: "{description}"'
            )

    return errors, len(parsed_tasks), len(completed)


def _table_cells(line: str) -> list[str]:
    """Bir Markdown tablo satırını hücrelerine ayırır."""

    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _validate_decisions(decisions: str) -> tuple[list[str], int]:
    """Karar tablosunun başlığını, tarihlerini ve gerekçelerini denetler."""

    errors: list[str] = []
    table_lines = [line for line in decisions.splitlines() if line.strip().startswith("|")]
    header_index: int | None = None
    for index, line in enumerate(table_lines):
        cells = [cell.casefold() for cell in _table_cells(line)]
        if cells == ["tarih", "karar", "gerekçe"]:
            header_index = index
            break

    if header_index is None:
        errors.append("DECISIONS.md, Tarih | Karar | Gerekçe başlıklı bir tablo içermelidir.")
        return errors, 0

    rows: list[list[str]] = []
    for line in table_lines[header_index + 1 :]:
        cells = _table_cells(line)
        if all(cell and set(cell) <= {"-", ":"} for cell in cells):
            continue
        if len(cells) == 3:
            rows.append(cells)

    if len(rows) < 2:
        errors.append("DECISIONS.md en az iki karar kaydı içermelidir.")

    for row_number, (date_text, decision, reason) in enumerate(rows, start=1):
        try:
            date.fromisoformat(date_text)
        except ValueError:
            errors.append(
                f"DECISIONS.md {row_number}. karar tarihi YYYY-AA-GG biçiminde olmalıdır."
            )
        if len(decision.split()) < 3:
            errors.append(f"DECISIONS.md {row_number}. karar açıklaması çok kısa.")
        if len(reason.split()) < 5:
            errors.append(f"DECISIONS.md {row_number}. karar gerekçesi çok kısa.")

    return errors, len(rows)


def validate_documents(prd: str, tasks: str, decisions: str) -> ValidationReport:
    """Üç belgeyi bölümün ortak kabul kriterlerine göre doğrular."""

    prd_errors, prd_section_count, user_story_count = _validate_prd(prd)
    task_errors, task_count, completed_task_count = _validate_tasks(tasks)
    decision_errors, decision_count = _validate_decisions(decisions)
    return ValidationReport(
        prd_section_count=prd_section_count,
        user_story_count=user_story_count,
        task_count=task_count,
        completed_task_count=completed_task_count,
        decision_count=decision_count,
        errors=tuple(prd_errors + task_errors + decision_errors),
    )


def format_report(report: ValidationReport) -> str:
    """Doğrulama sonucunu terminalde okunacak kısa bir özete çevirir."""

    lines = [
        "PRD ve Proje Hafızası — doğrulama",
        f"PRD bölümü: {report.prd_section_count}/{len(REQUIRED_PRD_SECTIONS)}",
        f"User story: {report.user_story_count}",
        (
            f"TASKS.md görevi: {report.task_count} "
            f"(tamamlandı: {report.completed_task_count})"
        ),
        f"DECISIONS.md kararı: {report.decision_count}",
    ]
    if report.is_valid:
        lines.append("Kabul kriteri karşılandı: Belge üçlüsü yapısal denetimden geçti.")
    else:
        lines.append("Kabul kriteri karşılanmadı:")
        lines.extend(f"- {error}" for error in report.errors)
    return "\n".join(lines)


def _read_documents(paths: Sequence[str]) -> tuple[str, str, str]:
    """Komut satırında verilen üç UTF-8 Markdown dosyasını okur."""

    prd_path, tasks_path, decisions_path = paths
    return (
        Path(prd_path).read_text(encoding="utf-8"),
        Path(tasks_path).read_text(encoding="utf-8"),
        Path(decisions_path).read_text(encoding="utf-8"),
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Gömülü örneği veya kullanıcı tarafından verilen üç dosyayı doğrular."""

    parser = argparse.ArgumentParser(
        description="PRD.md, TASKS.md ve DECISIONS.md dosyalarını doğrular."
    )
    parser.add_argument("documents", nargs="*", metavar="DOSYA")
    args = parser.parse_args(argv)

    if len(args.documents) not in (0, 3):
        parser.error(
            "ya hiç dosya vermeyin ya da PRD.md TASKS.md DECISIONS.md "
            "sırasını kullanın"
        )

    if args.documents:
        try:
            prd, tasks, decisions = _read_documents(args.documents)
        except OSError as error:
            parser.error(f"dosya okunamadı: {error}")
    else:
        prd, tasks, decisions = (
            REPRESENTATIVE_PRD,
            REPRESENTATIVE_TASKS,
            REPRESENTATIVE_DECISIONS,
        )

    report = validate_documents(prd, tasks, decisions)
    print(format_report(report))
    return 0 if report.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
