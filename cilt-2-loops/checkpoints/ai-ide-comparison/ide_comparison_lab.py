"""Aynı görevin birden fazla AI IDE'deki sonuçlarını karşılaştırır.

volume: 2
chapter: 04
book_section: "4.9 AI IDE Seçim Matrisi"
concepts:
  - AI IDE
  - ortak görev tarifi
  - diff okunabilirliği
  - insan karar noktası
objectives:
  - "LO-4.4"
  - "LO-4.5"
  - "LO-4.6"
last_verified: "2026-07"

Gömülü araç kayıtları temsilîdir; gerçek bir ürün karşılaştırması veya benchmark
olarak kullanılmamalıdır.
"""

from collections.abc import Sequence
from dataclasses import dataclass


MIN_RUNS = 2
MAX_RUNS = 3
MIN_ACCEPTANCE_CRITERIA = 2


@dataclass(frozen=True)
class ToolRun:
    """Bir araç denemesindeki gözlemleri tutar."""

    tool_name: str
    initial_test_passed: bool
    correction_rounds: int
    diff_readability: int
    surprise_or_error: str
    standout_reason: str


@dataclass(frozen=True)
class ComparisonSummary:
    """Doğrulanmış araç kayıtlarının ayrı ölçütlerdeki özetini tutar."""

    initial_passes: tuple[str, ...]
    fewest_correction_rounds: int
    fewest_correction_tools: tuple[str, ...]
    highest_readability: int
    highest_readability_tools: tuple[str, ...]


TASK_PROMPT = (
    "Kayıt formundaki telefon alanına yerel ve uluslararası biçimleri kabul eden "
    "doğrulama ekle; geçersiz girişte Türkçe hata mesajı göster."
)

ACCEPTANCE_CRITERIA = (
    "Geçerli yerel telefon numarası kabul edilir.",
    "Geçerli uluslararası telefon numarası kabul edilir.",
    "Hatalı giriş Türkçe bir uyarıyla reddedilir.",
)

REPRESENTATIVE_RUNS = (
    ToolRun(
        tool_name="Araç A",
        initial_test_passed=False,
        correction_rounds=1,
        diff_readability=4,
        surprise_or_error="Uluslararası biçim için ek test gerekti.",
        standout_reason="Çok dosyalı değişikliği tek diff içinde düzenli sundu.",
    ),
    ToolRun(
        tool_name="Araç B",
        initial_test_passed=True,
        correction_rounds=0,
        diff_readability=3,
        surprise_or_error="Hata mesajının dilini elle gözden geçirmek gerekti.",
        standout_reason="İlk taslak ortak kabul testlerini ek düzeltme olmadan geçti.",
    ),
)


def _is_single_sentence(text: str) -> bool:
    """Metnin tek bir tamamlanmış cümle biçiminde olup olmadığını denetler."""

    stripped = text.strip()
    if not stripped or stripped[-1] not in ".?!":
        return False
    return sum(stripped.count(mark) for mark in ".?!") == 1


def validate_comparison(
    task_prompt: str,
    acceptance_criteria: Sequence[str],
    runs: Sequence[ToolRun],
) -> list[str]:
    """Karşılaştırmayı laboratuvarın açık kabul ölçütlerine göre doğrular."""

    errors: list[str] = []
    if not task_prompt.strip():
        errors.append("Ortak görev tarifi boş bırakılamaz.")

    cleaned_criteria = [criterion.strip() for criterion in acceptance_criteria]
    nonempty_criteria = [criterion for criterion in cleaned_criteria if criterion]
    if len(nonempty_criteria) < MIN_ACCEPTANCE_CRITERIA:
        errors.append(
            f"En az {MIN_ACCEPTANCE_CRITERIA} ortak kabul ölçütü yazılmalıdır."
        )
    folded_criteria = [criterion.casefold() for criterion in nonempty_criteria]
    if len(folded_criteria) != len(set(folded_criteria)):
        errors.append("Ortak kabul ölçütleri yinelenmemelidir.")

    if not MIN_RUNS <= len(runs) <= MAX_RUNS:
        errors.append(f"Karşılaştırma {MIN_RUNS} veya {MAX_RUNS} araç içermelidir.")

    seen_names: set[str] = set()
    for run_number, run in enumerate(runs, start=1):
        label = f"{run_number}. araç"
        tool_name = run.tool_name.strip()
        if not tool_name:
            errors.append(f"{label} adı boş bırakılamaz.")
        elif tool_name.casefold() in seen_names:
            errors.append(f'{label} adı "{tool_name}" yineleniyor.')
        else:
            seen_names.add(tool_name.casefold())

        if type(run.initial_test_passed) is not bool:
            errors.append(f"{label} için ilk test sonucu geçti/geçmedi olarak seçilmelidir.")
        if type(run.correction_rounds) is not int or run.correction_rounds < 0:
            errors.append(f"{label} düzeltme turu 0 veya daha büyük bir tam sayı olmalıdır.")
        if type(run.diff_readability) is not int or not 1 <= run.diff_readability <= 5:
            errors.append(f"{label} diff okunabilirliği 1-5 aralığında olmalıdır.")
        if not run.surprise_or_error.strip():
            errors.append(f"{label} için bir sürpriz veya hata yazılmalıdır.")
        if not _is_single_sentence(run.standout_reason):
            errors.append(
                f"{label} için öne çıkan özellik tek ve tamamlanmış bir cümle olmalıdır."
            )

    return errors


def summarize_comparison(
    task_prompt: str,
    acceptance_criteria: Sequence[str],
    runs: Sequence[ToolRun],
) -> ComparisonSummary:
    """Kabul ölçütlerini geçen kayıtlar için ayrı ölçütlerin özetini üretir."""

    errors = validate_comparison(task_prompt, acceptance_criteria, runs)
    if errors:
        raise ValueError("Özet üretilemedi: " + " ".join(errors))

    fewest_rounds = min(run.correction_rounds for run in runs)
    highest_readability = max(run.diff_readability for run in runs)
    return ComparisonSummary(
        initial_passes=tuple(run.tool_name for run in runs if run.initial_test_passed),
        fewest_correction_rounds=fewest_rounds,
        fewest_correction_tools=tuple(
            run.tool_name for run in runs if run.correction_rounds == fewest_rounds
        ),
        highest_readability=highest_readability,
        highest_readability_tools=tuple(
            run.tool_name for run in runs if run.diff_readability == highest_readability
        ),
    )


def main() -> int:
    """Temsilî kayıtları doğrular ve karşılaştırmayı terminale yazar."""

    errors = validate_comparison(TASK_PROMPT, ACCEPTANCE_CRITERIA, REPRESENTATIVE_RUNS)
    if errors:
        print("Kabul kriteri karşılanmadı:")
        for error in errors:
            print(f"- {error}")
        return 1

    summary = summarize_comparison(TASK_PROMPT, ACCEPTANCE_CRITERIA, REPRESENTATIVE_RUNS)
    print(
        "AI IDE Karşılaştırması — "
        f"{len(REPRESENTATIVE_RUNS)} araç / {len(ACCEPTANCE_CRITERIA)} ortak kabul ölçütü"
    )
    for run in REPRESENTATIVE_RUNS:
        initial_result = "geçti" if run.initial_test_passed else "geçmedi"
        print(
            f"{run.tool_name}: ilk test={initial_result}, "
            f"düzeltme turu={run.correction_rounds}, "
            f"diff okunabilirliği={run.diff_readability}/5"
        )
    print(
        "En az düzeltme turu: "
        f"{', '.join(summary.fewest_correction_tools)} "
        f"({summary.fewest_correction_rounds})"
    )
    print(
        "En yüksek diff okunabilirliği: "
        f"{', '.join(summary.highest_readability_tools)} "
        f"({summary.highest_readability}/5)"
    )
    print("Kabul kriteri karşılandı: Karşılaştırma kaydı tamam.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
