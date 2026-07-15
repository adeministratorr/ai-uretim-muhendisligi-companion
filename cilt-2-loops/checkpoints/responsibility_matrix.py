"""Sorumluluk matrisi kabul kriterlerini denetleyen saf Python laboratuvarı.

volume: 2
chapter: 01
book_section: "1.9 Bu Kitabın Kullanım Yöntemi"
concepts:
  - Sorumluluk Matrisi
  - insan denetimi
  - onay noktası
objectives:
  - "LO-1.6"
last_verified: "2026-07"

Örnek veriler temsilîdir; gerçek bir ekip veya üretim sistemi anlatılmaz.
"""

from collections.abc import Sequence
from dataclasses import dataclass
import re


MIN_TASKS = 5
MAX_TASKS = 8


@dataclass(frozen=True)
class MatrixRow:
    """Tek bir geliştirme görevinin sorumluluk dağılımı."""

    task: str
    delegated_to_ai: str
    kept_by_developer: str
    done_together: str
    reason: str


SAMPLE_ROWS = (
    MatrixRow(
        task="Özellik geliştirme",
        delegated_to_ai="İlk kod taslağını oluşturur.",
        kept_by_developer="Mimari kararı verir.",
        done_together="Kabul kriterlerini netleştirir.",
        reason="Mimari karar ürünün sonraki değişikliklerini doğrudan etkiler.",
    ),
    MatrixRow(
        task="Kod inceleme",
        delegated_to_ai="Olası riskli satırları işaretler.",
        kept_by_developer="Diff'i okuyup onaylar.",
        done_together="Değişiklik gerekçesini değerlendirir.",
        reason="Kodun son sorumluluğu değişikliği onaylayan geliştiricide kalır.",
    ),
    MatrixRow(
        task="Test yazımı",
        delegated_to_ai="Test taslağı önerir.",
        kept_by_developer="Kritik senaryoları seçer.",
        done_together="Kapsam boşluklarını gözden geçirir.",
        reason="Kritik senaryolar iş kurallarını ve hata etkisini bilmeyi gerektirir.",
    ),
    MatrixRow(
        task="Hata ayıklama",
        delegated_to_ai="Hata nedenleri için hipotez üretir.",
        kept_by_developer="Kanıtı doğrular.",
        done_together="En küçük yeniden üretim adımını kurar.",
        reason="Bir hipotezin ikna edici görünmesi doğru olduğunu kanıtlamaz.",
    ),
    MatrixRow(
        task="Dokümantasyon",
        delegated_to_ai="İlk açıklama taslağını yazar.",
        kept_by_developer="İçerik doğruluğunu denetler.",
        done_together="Terimleri ve örnekleri gözden geçirir.",
        reason="Yanlış bir açıklama doğru kodun hatalı kullanılmasına yol açabilir.",
    ),
    MatrixRow(
        task="Üretime alma kararı",
        delegated_to_ai="Kontrol listesindeki bulguları özetler.",
        kept_by_developer="Son onayı verir.",
        done_together="Test ve diff sonuçlarını inceler.",
        reason="Üretim etkisi geri alma maliyeti ve kullanıcı riski taşır.",
    ),
)


def _is_sentence(value: str) -> bool:
    """Değerin kısa bir gerekçe değil, tamamlanmış bir cümle olduğunu denetler."""

    words = re.findall(r"\S+", value.strip())
    return len(words) >= 3 and bool(re.search(r"[.!?]$", value.strip()))


def validate_matrix(rows: Sequence[MatrixRow]) -> list[str]:
    """Matrisi bölümdeki kabul kriterlerine göre doğrular."""

    errors: list[str] = []
    if not MIN_TASKS <= len(rows) <= MAX_TASKS:
        errors.append(f"Matris {MIN_TASKS}-{MAX_TASKS} görev içermelidir.")

    seen_tasks: set[str] = set()
    fields = (
        ("delegated_to_ai", "Yapay zekâya devredilen"),
        ("kept_by_developer", "Geliştiricide kalan"),
        ("done_together", "Birlikte yürütülen"),
    )

    for row_number, row in enumerate(rows, start=1):
        task = row.task.strip()
        if not task:
            errors.append(f"{row_number}. satırda görev adı boş bırakılamaz.")
        elif task.casefold() in seen_tasks:
            errors.append(f'{row_number}. satırdaki "{task}" görevi yineleniyor.')
        else:
            seen_tasks.add(task.casefold())

        for field_name, label in fields:
            if not getattr(row, field_name).strip():
                errors.append(f"{row_number}. satırda '{label}' alanı boş bırakılamaz.")

        if not _is_sentence(row.reason):
            errors.append(
                f"{row_number}. satırdaki insan denetimi gerekçesi en az üç kelimelik "
                "bir cümle olmalıdır."
            )

    return errors


def main() -> int:
    """Temsilî matrisi doğrular ve sonucu terminale yazar."""

    print(f"Sorumluluk Matrisi — {len(SAMPLE_ROWS)} görev")
    errors = validate_matrix(SAMPLE_ROWS)
    if errors:
        print("Kabul kriteri karşılanmadı:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Kabul kriteri karşılandı: "
        f"{len(SAMPLE_ROWS)} görevin sorumluluk alanları ve gerekçeleri tamam."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
