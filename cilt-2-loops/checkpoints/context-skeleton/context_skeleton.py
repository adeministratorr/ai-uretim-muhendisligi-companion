"""Laravel + Flutter projesi için context iskeletini doğrulayan laboratuvar.

volume: 2
chapter: 03
book_section: "3.11-3.17 Context'i Yazılı Hâle Getirme ve Proje Hafızası"
concepts:
  - codified context
  - PRD
  - TASKS.md
  - hot memory
  - cold memory
objectives:
  - "LO-3.4"
  - "LO-3.5"
last_verified: "2026-07"

Örnek içerik temsilîdir; gerçek kişi, kurum veya üretim verisi içermez.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path


REQUIRED_DOCUMENTS = ("PRD.md", "TASKS.md", "CLAUDE.md", "rules.md")
DOCUMENT_HEADINGS = {
    "PRD.md": "PRD Taslağı",
    "TASKS.md": "Görevler",
    "CLAUDE.md": "Proje Context'i",
    "rules.md": "Proje Kuralları",
}
MIN_ITEMS_PER_DOCUMENT = 3
MIN_MEMORY_LABELS = 4
ALLOWED_LAYERS = frozenset({"hot", "cold"})

EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
CREDENTIAL_PATTERN = re.compile(
    r"\b(?:api[_ -]?key|secret|token|password|şifre|parola)\b"
    r"\s*[:=]\s*[`'\"]?[^\s`'\"]{4,}",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class MemoryLabel:
    """Bir proje bilgisinin hafıza katmanını ve gerekçesini tutar."""

    statement: str
    layer: str
    reason: str


SAMPLE_DOCUMENTS: dict[str, tuple[str, ...]] = {
    "PRD.md": (
        "Amaç: Küçük kliniklerde randevu oluşturma ve iptal akışını tek yerde toplamak.",
        "Hedef kullanıcı: Randevu takibini yürüten klinik çalışanları.",
        "Kapsam: Randevu oluşturma, listeleme ve iptal etme.",
        "Kapsam dışı: Ödeme ve sigorta işlemleri.",
    ),
    "TASKS.md": (
        "Randevu oluşturma API uç noktasını yaz (Laravel).",
        "Randevu listesi ekranını oluştur (Flutter).",
        "Geçerli ve geçersiz tarih girişleri için test yaz.",
        "İptal akışını insan incelemesinden geçir.",
    ),
    "CLAUDE.md": (
        "Backend Laravel, mobil istemci Flutter ile yazılır.",
        "Veritabanı PostgreSQL'dir.",
        "Test komutları: `php artisan test` ve `flutter test`.",
        "Değişken ve fonksiyon adları İngilizce, kullanıcı metinleri Türkçedir.",
    ),
    "rules.md": (
        "Yeni bir doğrulama kütüphanesi ekleme; mevcut kuralları kullan.",
        "İş mantığını controller içine yerleştirme.",
        "Test silme veya assertion zayıflatma.",
        "Görev kapsamı dışındaki dosyaları değiştirme.",
    ),
}

SAMPLE_MEMORY_LABELS = (
    MemoryLabel(
        "Backend Laravel, mobil istemci Flutter ile yazılır.",
        "hot",
        "Teknoloji yığını her geliştirme görevinde doğrudan kullanılır.",
    ),
    MemoryLabel(
        "Test komutları",
        "hot",
        "Doğrulama komutları her kod değişikliğinde gerekir.",
    ),
    MemoryLabel(
        "Randevu oluşturma API görevi",
        "hot",
        "Aktif görev yeni oturumun başlangıç noktasını belirler.",
    ),
    MemoryLabel(
        "Yeni doğrulama kütüphanesi eklememe kuralı",
        "hot",
        "Kural her ilgili değişiklikte mimari sapmayı önler.",
    ),
    MemoryLabel(
        "Ödeme akışının neden kapsam dışı bırakıldığına ilişkin ayrıntılı karar notu",
        "cold",
        "Karar geçmişi yalnız kapsam yeniden tartışıldığında gerekir.",
    ),
)


def _sensitive_data_error(text: str) -> str | None:
    """Metindeki açık e-posta veya secret atamasını adlandırır."""

    if EMAIL_PATTERN.search(text):
        return "e-posta adresi"
    if CREDENTIAL_PATTERN.search(text):
        return "gizli bilgi ataması"
    return None


def validate_context_skeleton(
    documents: Mapping[str, Sequence[str]],
    memory_labels: Sequence[MemoryLabel],
) -> list[str]:
    """Context iskeletini laboratuvarın açık kabul ölçütlerine göre doğrular."""

    errors: list[str] = []
    text_fields: list[tuple[str, str]] = []

    for document_name in REQUIRED_DOCUMENTS:
        if document_name not in documents:
            errors.append(f"{document_name} dosyası eksik.")
            continue

        items = [item.strip() for item in documents[document_name] if item.strip()]
        if len(items) < MIN_ITEMS_PER_DOCUMENT:
            errors.append(
                f"{document_name} en az {MIN_ITEMS_PER_DOCUMENT} madde içermelidir."
            )
        text_fields.extend((document_name, item) for item in items)

    if len(memory_labels) < MIN_MEMORY_LABELS:
        errors.append(f"En az {MIN_MEMORY_LABELS} madde hot/cold olarak etiketlenmelidir.")

    seen_statements: set[str] = set()
    for number, label in enumerate(memory_labels, start=1):
        statement = label.statement.strip()
        layer = label.layer.strip().casefold()
        reason = label.reason.strip()

        if not statement:
            errors.append(f"{number}. hafıza maddesi boş bırakılamaz.")
        elif statement.casefold() in seen_statements:
            errors.append(f'{number}. hafıza maddesi yineleniyor: "{statement}".')
        else:
            seen_statements.add(statement.casefold())

        if layer not in ALLOWED_LAYERS:
            errors.append(f"{number}. hafıza maddesi hot veya cold olarak etiketlenmelidir.")
        if len(reason.split()) < 4 or not reason.endswith((".", "?", "!")):
            errors.append(f"{number}. hafıza maddesi kısa bir gerekçe cümlesi taşımalıdır.")

        text_fields.append((f"{number}. hafıza maddesi", statement))
        text_fields.append((f"{number}. hafıza gerekçesi", reason))

    for source, text in text_fields:
        sensitive_kind = _sensitive_data_error(text)
        if sensitive_kind:
            errors.append(f"{source} {sensitive_kind} içeriyor; örnek veri kullanın.")

    return errors


def render_document(document_name: str, items: Sequence[str]) -> str:
    """Bir context belgesini Markdown olarak üretir."""

    heading = DOCUMENT_HEADINGS[document_name]
    prefix = "- [ ] " if document_name == "TASKS.md" else "- "
    lines = [f"# {heading}", "", *(f"{prefix}{item.strip()}" for item in items)]
    return "\n".join(lines) + "\n"


def render_memory_map(memory_labels: Sequence[MemoryLabel]) -> str:
    """Hot/cold etiketlerini gerekçeleriyle Markdown tabloya dönüştürür."""

    lines = [
        "# Hafıza Haritası",
        "",
        "| Bilgi | Katman | Gerekçe |",
        "|---|---|---|",
    ]
    lines.extend(
        f"| {label.statement} | {label.layer} | {label.reason} |"
        for label in memory_labels
    )
    return "\n".join(lines) + "\n"


def build_output_files(
    documents: Mapping[str, Sequence[str]],
    memory_labels: Sequence[MemoryLabel],
) -> dict[str, str]:
    """Doğrulanmış iskelet için yazılacak dosyaları hazırlar."""

    errors = validate_context_skeleton(documents, memory_labels)
    if errors:
        raise ValueError("İskelet üretilemedi: " + " ".join(errors))

    output = {
        name: render_document(name, documents[name]) for name in REQUIRED_DOCUMENTS
    }
    output["MEMORY_MAP.md"] = render_memory_map(memory_labels)
    return output


def write_context_skeleton(
    target: Path,
    documents: Mapping[str, Sequence[str]] = SAMPLE_DOCUMENTS,
    memory_labels: Sequence[MemoryLabel] = SAMPLE_MEMORY_LABELS,
) -> tuple[Path, ...]:
    """İskeleti boş bir hedefe yazar; var olan dosyaların üzerine yazmaz."""

    output_files = build_output_files(documents, memory_labels)
    conflicts = [target / name for name in output_files if (target / name).exists()]
    if conflicts:
        conflict_names = ", ".join(path.name for path in conflicts)
        raise FileExistsError(f"Var olan dosyaların üzerine yazılmadı: {conflict_names}")

    target.mkdir(parents=True, exist_ok=True)
    written_paths: list[Path] = []
    for name, content in output_files.items():
        path = target / name
        path.write_text(content, encoding="utf-8")
        written_paths.append(path)
    return tuple(written_paths)


def summary_lines(
    documents: Mapping[str, Sequence[str]], memory_labels: Sequence[MemoryLabel]
) -> tuple[str, str, str]:
    """Başarılı doğrulamanın kısa terminal özetini üretir."""

    item_count = sum(len([item for item in items if item.strip()]) for items in documents.values())
    layer_counts = Counter(label.layer.casefold() for label in memory_labels)
    return (
        f"Context İskeleti — {len(REQUIRED_DOCUMENTS)} dosya / {item_count} madde",
        "Hafıza Etiketleri — "
        f"{len(memory_labels)} madde (hot={layer_counts['hot']}, cold={layer_counts['cold']})",
        "Kabul kriteri karşılandı: Context iskeleti doğrulandı.",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Temsilî iskeleti doğrular ve istenirse dosyaları hedef klasöre yazar."""

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--output",
        type=Path,
        help="Doğrulanmış örnek dosyaların yazılacağı klasör.",
    )
    args = parser.parse_args(argv)

    errors = validate_context_skeleton(SAMPLE_DOCUMENTS, SAMPLE_MEMORY_LABELS)
    if errors:
        print("Kabul kriteri karşılanmadı:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    for line in summary_lines(SAMPLE_DOCUMENTS, SAMPLE_MEMORY_LABELS):
        print(line)

    if args.output:
        try:
            written = write_context_skeleton(args.output)
        except (FileExistsError, OSError, ValueError) as error:
            print(f"Dosyalar yazılamadı: {error}", file=sys.stderr)
            return 2
        print(f"İskelet yazıldı: {args.output} ({len(written)} dosya)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
