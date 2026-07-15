"""Geleneksel plan ile vibe coding planını karşılaştıran saf Python laboratuvarı.

volume: 2
chapter: 02
book_section: "2.9 İterasyon Döngüsü"
concepts:
  - vibe coding
  - mise en place
  - insan onay noktası
  - verification-driven development
objectives:
  - "LO-2.3"
  - "LO-2.6"
last_verified: "2026-07"

Örnek adımlar ve süreler temsilîdir; gerçek bir ekip ölçümü anlatılmaz.
"""

from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass


MIN_STEPS = 5
MAX_STEPS = 8
MISE_EN_PLACE = "mise_en_place"
VERIFICATION = "verification"
HUMAN_APPROVAL = "human_approval"
ALLOWED_MARKERS = frozenset({MISE_EN_PLACE, VERIFICATION, HUMAN_APPROVAL})
MARKER_LABELS = {
    MISE_EN_PLACE: "mise en place",
    VERIFICATION: "doğrulama",
    HUMAN_APPROVAL: "insan onayı",
}


@dataclass(frozen=True)
class PlanStep:
    """Bir plan adımını, tahminini ve denetim işaretlerini tutar."""

    description: str
    minutes: int
    uncertainty: int
    markers: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ComparisonSummary:
    """Doğrulanmış iki planın karşılaştırma özetini tutar."""

    traditional_minutes: int
    vibe_minutes: int
    traditional_uncertainty: float
    vibe_uncertainty: float
    marker_counts: Counter[str]


TRADITIONAL_PLAN = (
    PlanStep("Form kütüphanesinin doğrulama arayüzünü incele.", 15, 2),
    PlanStep("Telefon kurallarını ve regex kalıbını yaz.", 25, 3),
    PlanStep("Hata mesajlarını forma ekle.", 15, 1),
    PlanStep("Doğrulamayı kayıt akışına bağla.", 20, 2),
    PlanStep("Geçerli ve geçersiz numaraları tarayıcıda dene.", 20, 2),
)

VIBE_CODING_PLAN = (
    PlanStep(
        "Dosyayı, desteklenen biçimleri ve kısıtları hazırla.",
        10,
        2,
        frozenset({MISE_EN_PLACE}),
    ),
    PlanStep("Görevi ve kabul ölçütlerini ajana tarif et.", 5, 2),
    PlanStep(
        "Üretilen diff'i ve ajanın varsayımlarını incele.",
        10,
        2,
        frozenset({HUMAN_APPROVAL}),
    ),
    PlanStep(
        "Geçerli ve geçersiz numaralarla testleri çalıştır.",
        15,
        1,
        frozenset({VERIFICATION}),
    ),
    PlanStep("Eksik kenar durumunu düzelttir ve kararı belgeye işle.", 10, 1),
)


def validate_plan(
    plan_name: str,
    steps: Sequence[PlanStep],
    required_markers: frozenset[str] = frozenset(),
) -> list[str]:
    """Bir planı laboratuvarın açık kabul ölçütlerine göre doğrular."""

    errors: list[str] = []
    if not MIN_STEPS <= len(steps) <= MAX_STEPS:
        errors.append(f"{plan_name} planı {MIN_STEPS}-{MAX_STEPS} adım içermelidir.")

    seen_descriptions: set[str] = set()
    present_markers: set[str] = set()
    for step_number, step in enumerate(steps, start=1):
        description = step.description.strip()
        if not description:
            errors.append(f"{plan_name} planının {step_number}. adımı boş bırakılamaz.")
        elif description.casefold() in seen_descriptions:
            errors.append(
                f'{plan_name} planının {step_number}. adımındaki "{description}" '
                "açıklaması yineleniyor."
            )
        else:
            seen_descriptions.add(description.casefold())

        if step.minutes <= 0:
            errors.append(
                f"{plan_name} planının {step_number}. adımında süre "
                "0'dan büyük olmalıdır."
            )
        if step.uncertainty not in {1, 2, 3}:
            errors.append(
                f"{plan_name} planının {step_number}. adımında belirsizlik "
                "1, 2 veya 3 olmalıdır."
            )

        unknown_markers = step.markers - ALLOWED_MARKERS
        if unknown_markers:
            errors.append(
                f"{plan_name} planının {step_number}. adımında tanımsız denetim "
                "işareti var."
            )
        present_markers.update(step.markers & ALLOWED_MARKERS)

    for marker in sorted(required_markers - present_markers):
        errors.append(f"{plan_name} planında en az bir {MARKER_LABELS[marker]} adımı olmalıdır.")

    return errors


def validate_comparison(
    traditional_steps: Sequence[PlanStep], vibe_steps: Sequence[PlanStep]
) -> list[str]:
    """İki planı, vibe coding denetim işaretleriyle birlikte doğrular."""

    return validate_plan("Geleneksel", traditional_steps) + validate_plan(
        "Vibe coding",
        vibe_steps,
        required_markers=ALLOWED_MARKERS,
    )


def summarize_comparison(
    traditional_steps: Sequence[PlanStep], vibe_steps: Sequence[PlanStep]
) -> ComparisonSummary:
    """Kabul ölçütlerini geçen iki plan için sayısal bir özet üretir."""

    errors = validate_comparison(traditional_steps, vibe_steps)
    if errors:
        raise ValueError("Özet üretilemedi: " + " ".join(errors))

    marker_counts = Counter(
        marker for step in vibe_steps for marker in step.markers if marker in ALLOWED_MARKERS
    )
    return ComparisonSummary(
        traditional_minutes=sum(step.minutes for step in traditional_steps),
        vibe_minutes=sum(step.minutes for step in vibe_steps),
        traditional_uncertainty=round(
            sum(step.uncertainty for step in traditional_steps) / len(traditional_steps), 1
        ),
        vibe_uncertainty=round(
            sum(step.uncertainty for step in vibe_steps) / len(vibe_steps), 1
        ),
        marker_counts=marker_counts,
    )


def main() -> int:
    """Temsilî planları doğrular ve karşılaştırmayı terminale yazar."""

    errors = validate_comparison(TRADITIONAL_PLAN, VIBE_CODING_PLAN)
    if errors:
        print("Kabul kriteri karşılanmadı:")
        for error in errors:
            print(f"- {error}")
        return 1

    summary = summarize_comparison(TRADITIONAL_PLAN, VIBE_CODING_PLAN)
    print(
        "Plan Karşılaştırması — Geleneksel: "
        f"{len(TRADITIONAL_PLAN)} adım / {summary.traditional_minutes} dakika"
    )
    print(
        "Plan Karşılaştırması — Vibe coding: "
        f"{len(VIBE_CODING_PLAN)} adım / {summary.vibe_minutes} dakika"
    )
    print(
        "Vibe coding denetim işaretleri: "
        f"mise en place={summary.marker_counts[MISE_EN_PLACE]}, "
        f"doğrulama={summary.marker_counts[VERIFICATION]}, "
        f"insan onayı={summary.marker_counts[HUMAN_APPROVAL]}"
    )
    print("Kabul kriteri karşılandı: İki plan da karşılaştırmaya hazır.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
