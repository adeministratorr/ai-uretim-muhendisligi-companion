"""Bir proje rule dosyasını Bölüm 9'un kabul ölçütleriyle doğrular.

volume: 2
chapter: 09
book_section: "9.12-9.15 İzin Kuralları, Compiled Enforcement ve Takım Kuralları"
concepts:
  - rule dosyası
  - permission rule
  - compiled enforcement
  - PR devre kesici
objectives:
  - "LO-9.4"
  - "LO-9.5"
  - "LO-9.6"
last_verified: "2026-07"

Gömülü Vardiya metni temsilîdir. Doğrulayıcı dosya yapısını denetler; bir aracın
kuralları gerçekten uyguladığını veya CI ayarının zorunlu olduğunu kanıtlamaz.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
from typing import Sequence


REQUIRED_SECTIONS = (
    "Proje Özeti",
    "Yasak İşlemler",
    "Zorunlu Doğrulama Adımları",
    "PR Devre Kesici",
)
MIN_FORBIDDEN_RULES = 3
MIN_VALIDATION_RULES = 3
MIN_BREAKER_RULES = 1
ALLOWED_TAGS = {
    "Yasak İşlemler": frozenset({"directive", "deny"}),
    "Zorunlu Doğrulama Adımları": frozenset({"directive", "compiled"}),
    "PR Devre Kesici": frozenset({"pr-stop"}),
}
CONDITION_WORDS = ("eğer ", "değişirse", "olursa", "başarısızsa", "içeriyorsa")

SECTION_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
BULLET_PATTERN = re.compile(r"^\s*-\s+(.+?)\s*$")
TAG_PATTERN = re.compile(r"^\[(?P<tag>[a-z-]+)\]\s+(?P<text>.+)$", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
CREDENTIAL_PATTERN = re.compile(
    r"\b(?:api[_ -]?key|secret|token|password|şifre|parola)\b"
    r"\s*[:=]\s*[`'\"]?[^\s`'\"]{4,}",
    re.IGNORECASE,
)


REPRESENTATIVE_RULE_FILE = """# AGENTS.md — Vardiya

## Proje Özeti

- Yığın: Laravel API ve React admin paneli kullanılır.
- Mimari: Bildirimler mevcut EmailService üzerinden gönderilir; iş mantığı servis katmanında tutulur.

## Yasak İşlemler

- [deny] `.env` dosyasını okuma veya içeriğini çıktıya yazma.
- [directive] Yeni bir e-posta sağlayıcısı ya da bildirim paketi ekleme.
- [directive] Test silme, assertion zayıflatma veya güvenlik denetimini kapatma.

## Zorunlu Doğrulama Adımları

- [compiled] Backend değişikliğinden sonra `php artisan test` komutunu çalıştır.
- [compiled] Admin paneli değişikliğinden sonra `npm test` komutunu çalıştır.
- [directive] Sonucu sunmadan önce diff'i kapsam ve hassas veri açısından incele.

## PR Devre Kesici

- [pr-stop] Eğer `auth/` altındaki bir dosya değişirse ve PR açıklaması gerekçe içermiyorsa PR durur.
"""


@dataclass(frozen=True)
class TaggedRule:
    """Bir kuralın denetim katmanını ve metnini taşır."""

    tag: str
    text: str


@dataclass(frozen=True)
class ValidationReport:
    """Rule dosyasının sayısal özetini ve bulunan sorunları taşır."""

    summary_count: int
    forbidden_count: int
    validation_count: int
    breaker_count: int
    deny_count: int
    compiled_count: int
    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        """Hiç hata yoksa kabul ölçütlerinin karşılandığını bildirir."""

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


def _bullet_items(text: str) -> list[str]:
    """Bir bölümdeki dolu Markdown liste maddelerini döndürür."""

    items: list[str] = []
    for line in text.splitlines():
        match = BULLET_PATTERN.match(line)
        if match and match.group(1).strip():
            items.append(match.group(1).strip())
    return items


def _parse_tagged_rules(
    section_name: str, items: Sequence[str]
) -> tuple[list[TaggedRule], list[str]]:
    """Liste maddelerindeki katman etiketlerini ayrıştırır."""

    allowed = ALLOWED_TAGS[section_name]
    parsed: list[TaggedRule] = []
    errors: list[str] = []
    for number, item in enumerate(items, start=1):
        match = TAG_PATTERN.match(item)
        if match is None:
            errors.append(
                f"{section_name} {number}. maddesi katman etiketiyle başlamalıdır."
            )
            continue

        tag = match.group("tag").casefold()
        text = match.group("text").strip()
        if tag not in allowed:
            expected = ", ".join(f"[{value}]" for value in sorted(allowed))
            errors.append(
                f"{section_name} {number}. maddesi şu etiketlerden birini kullanmalıdır: "
                f"{expected}."
            )
        if len(text.split()) < 5:
            errors.append(f"{section_name} {number}. maddesi somut bir davranış yazmalıdır.")
        parsed.append(TaggedRule(tag=tag, text=text))
    return parsed, errors


def _sensitive_data_kind(text: str) -> str | None:
    """Açık e-posta veya gizli bilgi atamasını adlandırır."""

    if EMAIL_PATTERN.search(text):
        return "e-posta adresi"
    if CREDENTIAL_PATTERN.search(text):
        return "gizli bilgi ataması"
    return None


def validate_rule_file(markdown: str) -> ValidationReport:
    """Bir rule dosyasını laboratuvarın açık kabul ölçütlerine göre doğrular."""

    errors: list[str] = []
    sections = _extract_sections(markdown)
    for heading in REQUIRED_SECTIONS:
        key = heading.casefold()
        if key not in sections:
            errors.append(f'"{heading}" başlığı eksik.')
        elif not sections[key].strip():
            errors.append(f'"{heading}" bölümü boş bırakılamaz.')

    summary_items = _bullet_items(sections.get("Proje Özeti".casefold(), ""))
    if not 2 <= len(summary_items) <= 3:
        errors.append("Proje Özeti, 2-3 dolu liste maddesi içermelidir.")
    summary_text = " ".join(summary_items).casefold()
    if summary_items and not any(word in summary_text for word in ("yığın", "teknoloji")):
        errors.append("Proje Özeti teknoloji yığınını açıkça belirtmelidir.")
    if summary_items and "mimari" not in summary_text:
        errors.append("Proje Özeti temel mimari kararı açıkça belirtmelidir.")

    forbidden_items = _bullet_items(sections.get("Yasak İşlemler".casefold(), ""))
    validation_items = _bullet_items(
        sections.get("Zorunlu Doğrulama Adımları".casefold(), "")
    )
    breaker_items = _bullet_items(sections.get("PR Devre Kesici".casefold(), ""))

    if len(forbidden_items) < MIN_FORBIDDEN_RULES:
        errors.append(f"Yasak İşlemler en az {MIN_FORBIDDEN_RULES} madde içermelidir.")
    if len(validation_items) < MIN_VALIDATION_RULES:
        errors.append(
            "Zorunlu Doğrulama Adımları en az "
            f"{MIN_VALIDATION_RULES} madde içermelidir."
        )
    if len(breaker_items) < MIN_BREAKER_RULES:
        errors.append(f"PR Devre Kesici en az {MIN_BREAKER_RULES} madde içermelidir.")

    forbidden, forbidden_errors = _parse_tagged_rules(
        "Yasak İşlemler", forbidden_items
    )
    validations, validation_errors = _parse_tagged_rules(
        "Zorunlu Doğrulama Adımları", validation_items
    )
    breakers, breaker_errors = _parse_tagged_rules("PR Devre Kesici", breaker_items)
    errors.extend(forbidden_errors + validation_errors + breaker_errors)

    deny_count = sum(rule.tag == "deny" for rule in forbidden)
    compiled_count = sum(rule.tag == "compiled" for rule in validations)
    if forbidden_items and deny_count == 0:
        errors.append("En az bir yasak işlem [deny] katmanına bağlanmalıdır.")
    if validation_items and compiled_count == 0:
        errors.append("En az bir doğrulama adımı [compiled] katmanına bağlanmalıdır.")

    for number, rule in enumerate(breakers, start=1):
        normalized = rule.text.casefold()
        if not any(word in normalized for word in CONDITION_WORDS):
            errors.append(
                f"PR Devre Kesici {number}. maddesi durma koşulunu açıkça yazmalıdır."
            )
        if "dur" not in normalized:
            errors.append(
                f"PR Devre Kesici {number}. maddesi PR'ın duracağını belirtmelidir."
            )

    all_rules = [*forbidden, *validations, *breakers]
    normalized_rules = [re.sub(r"\s+", " ", rule.text.casefold()).strip() for rule in all_rules]
    if len(normalized_rules) != len(set(normalized_rules)):
        errors.append("Aynı davranış kuralı birden fazla bölümde yinelenmemelidir.")

    sensitive_fields = [*summary_items, *(rule.text for rule in all_rules)]
    for text in sensitive_fields:
        sensitive_kind = _sensitive_data_kind(text)
        if sensitive_kind:
            errors.append(f"Rule dosyası {sensitive_kind} içeriyor; örnek veri kullanın.")
            break

    return ValidationReport(
        summary_count=len(summary_items),
        forbidden_count=len(forbidden_items),
        validation_count=len(validation_items),
        breaker_count=len(breaker_items),
        deny_count=deny_count,
        compiled_count=compiled_count,
        errors=tuple(errors),
    )


def format_report(report: ValidationReport) -> str:
    """Doğrulama sonucunu terminalde okunacak kısa bir özete çevirir."""

    lines = [
        "Rule Dosyası Denetimi",
        f"Proje özeti: {report.summary_count} madde",
        f"Yasak işlem: {report.forbidden_count} ([deny]: {report.deny_count})",
        (
            "Doğrulama adımı: "
            f"{report.validation_count} ([compiled]: {report.compiled_count})"
        ),
        f"PR devre kesici: {report.breaker_count}",
    ]
    if report.is_valid:
        lines.append("Kabul kriteri karşılandı: Rule dosyası yapısal denetimden geçti.")
    else:
        lines.append("Kabul kriteri karşılanmadı:")
        lines.extend(f"- {error}" for error in report.errors)
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """Gömülü örneği veya verilen UTF-8 Markdown dosyasını doğrular."""

    parser = argparse.ArgumentParser(
        description="Bir AGENTS.md, CLAUDE.md veya rules dosyasını doğrular."
    )
    parser.add_argument("rule_file", nargs="?", type=Path, metavar="RULE_DOSYASI")
    args = parser.parse_args(argv)

    if args.rule_file:
        try:
            markdown = args.rule_file.read_text(encoding="utf-8")
        except OSError as error:
            parser.error(f"dosya okunamadı: {error}")
    else:
        markdown = REPRESENTATIVE_RULE_FILE

    report = validate_rule_file(markdown)
    print(format_report(report))
    return 0 if report.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
