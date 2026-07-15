"""GUI araçla yürütülen 45 dakikalık MVP deneyinin kaydını doğrular.

volume: 2
chapter: 05
book_section: "5.8 GUI Araç Seçim Matrisi"
concepts:
  - GUI coding agent
  - MVP prototipleme
  - müdahale noktası
  - teknik borç
objectives:
  - "LO-5.1"
  - "LO-5.2"
  - "LO-5.3"
  - "LO-5.4"
  - "LO-5.5"
  - "LO-5.6"
last_verified: "2026-07"

Gömülü kayıt temsilîdir; gerçek bir ürün karşılaştırması veya benchmark değildir.
"""

from collections.abc import Sequence
from dataclasses import dataclass


MIN_IDEA_SENTENCES = 3
MAX_IDEA_SENTENCES = 4
TIMEBOX_MINUTES = 45
CHANGE_RESULTS = frozenset({"uygulandı", "kısmen uygulandı", "uygulanmadı"})
CODE_REVIEW_STATUSES = frozenset({"incelendi", "erişilemedi", "incelenmedi"})


@dataclass(frozen=True)
class MvpExperiment:
    """Bir GUI araç denemesindeki karar ve gözlemleri tutar."""

    tool_name: str
    idea_sentences: tuple[str, ...]
    elapsed_minutes: int
    quota_reached: bool
    automatic_steps: tuple[str, ...]
    intervention_points: tuple[str, ...]
    change_request: str
    change_result: str
    code_review_status: str
    review_note: str
    attention_point: str


@dataclass(frozen=True)
class ExperimentSummary:
    """Doğrulanmış deney kaydının sayısal özetini tutar."""

    automatic_step_count: int
    intervention_point_count: int
    ended_by_quota: bool


REPRESENTATIVE_EXPERIMENT = MvpExperiment(
    tool_name="Örnek Araç",
    idea_sentences=(
        "Küçük bir işletme ürünlerini tek ekranda izlemek istiyor.",
        "Kullanıcı ürün adı, adet ve fiyat girebilmeli.",
        "Her hesap yalnızca kendi ürünlerini görebilmeli.",
        "İlk sürümde ödeme ve fatura özelliği bulunmamalı.",
    ),
    elapsed_minutes=45,
    quota_reached=False,
    automatic_steps=(
        "Giriş ve ürün listesi ekranlarını oluşturdu",
        "Ürün ekleme formunu önizlemede çalıştırdı",
    ),
    intervention_points=(
        "Negatif stok adedini engelleyen doğrulama ayrıca istendi",
    ),
    change_request="Ürün formuna negatif adet kontrolü ekle.",
    change_result="uygulandı",
    code_review_status="incelendi",
    review_note="Üretilen dosyalarda hesap ayrımı ve gizli anahtar kullanımı gözden geçirildi.",
    attention_point=(
        "Hesap ayrımını yalnızca önizlemeden değil, kod ve veri kurallarından da "
        "doğrulamak gerekir."
    ),
)


def _is_single_sentence(text: str) -> bool:
    """Metnin tek bir tamamlanmış cümle olup olmadığını denetler."""

    stripped = text.strip()
    if not stripped or stripped[-1] not in ".?!":
        return False
    return sum(stripped.count(mark) for mark in ".?!") == 1


def _clean_items(items: Sequence[str]) -> list[str]:
    """Liste alanlarını çevre boşluklarından arındırır."""

    return [item.strip() for item in items]


def _list_errors(items: Sequence[str], label: str) -> list[str]:
    """Gözlem listesindeki boş ve yinelenen maddeleri bulur."""

    cleaned = _clean_items(items)
    errors: list[str] = []
    if not cleaned or any(not item for item in cleaned):
        errors.append(f"En az bir {label} yazılmalıdır; boş madde bırakılamaz.")
    folded = [item.casefold() for item in cleaned if item]
    if len(folded) != len(set(folded)):
        errors.append(f"{label.capitalize()} yinelenmemelidir.")
    return errors


def validate_experiment(experiment: MvpExperiment) -> list[str]:
    """Deney kaydını laboratuvarın açık kabul ölçütlerine göre doğrular."""

    errors: list[str] = []
    if not experiment.tool_name.strip():
        errors.append("Araç adı boş bırakılamaz.")

    idea_sentences = _clean_items(experiment.idea_sentences)
    if not MIN_IDEA_SENTENCES <= len(idea_sentences) <= MAX_IDEA_SENTENCES:
        errors.append("MVP fikri 3 veya 4 cümleyle tarif edilmelidir.")
    elif any(not _is_single_sentence(sentence) for sentence in idea_sentences):
        errors.append("MVP tarifindeki her satır tek ve tamamlanmış bir cümle olmalıdır.")

    if type(experiment.elapsed_minutes) is not int:
        errors.append("Geçen süre tam sayı olarak yazılmalıdır.")
    elif not 1 <= experiment.elapsed_minutes <= TIMEBOX_MINUTES:
        errors.append("Geçen süre 1-45 dakika aralığında olmalıdır.")
    elif experiment.elapsed_minutes < TIMEBOX_MINUTES and not experiment.quota_reached:
        errors.append("45 dakikadan önce biten deneyde kota sınırı işaretlenmelidir.")
    if type(experiment.quota_reached) is not bool:
        errors.append("Kota durumu evet/hayır olarak seçilmelidir.")

    errors.extend(_list_errors(experiment.automatic_steps, "otomatik tamamlanan adım"))
    errors.extend(_list_errors(experiment.intervention_points, "müdahale noktası"))

    automatic = {item.casefold() for item in _clean_items(experiment.automatic_steps) if item}
    interventions = {
        item.casefold() for item in _clean_items(experiment.intervention_points) if item
    }
    if automatic & interventions:
        errors.append("Aynı gözlem hem otomatik adım hem müdahale noktası olamaz.")

    if not _is_single_sentence(experiment.change_request):
        errors.append("Küçük değişiklik isteği tek ve tamamlanmış bir cümle olmalıdır.")
    if experiment.change_result not in CHANGE_RESULTS:
        errors.append("Küçük değişiklik sonucu geçerli seçeneklerden biri olmalıdır.")
    if experiment.code_review_status not in CODE_REVIEW_STATUSES:
        errors.append("Kod inceleme durumu geçerli seçeneklerden biri olmalıdır.")
    if not _is_single_sentence(experiment.review_note):
        errors.append("Kod inceleme notu tek ve tamamlanmış bir cümle olmalıdır.")
    if not _is_single_sentence(experiment.attention_point):
        errors.append("Dikkat noktası tek ve tamamlanmış bir cümle olmalıdır.")

    return errors


def summarize_experiment(experiment: MvpExperiment) -> ExperimentSummary:
    """Kabul ölçütlerini geçen kayıt için kısa bir özet üretir."""

    errors = validate_experiment(experiment)
    if errors:
        raise ValueError("Özet üretilemedi: " + " ".join(errors))
    return ExperimentSummary(
        automatic_step_count=len(experiment.automatic_steps),
        intervention_point_count=len(experiment.intervention_points),
        ended_by_quota=(
            experiment.quota_reached and experiment.elapsed_minutes < TIMEBOX_MINUTES
        ),
    )


def main() -> int:
    """Temsilî kaydı doğrular ve deney özetini terminale yazar."""

    errors = validate_experiment(REPRESENTATIVE_EXPERIMENT)
    if errors:
        print("Kabul kriteri karşılanmadı:")
        for error in errors:
            print(f"- {error}")
        return 1

    summary = summarize_experiment(REPRESENTATIVE_EXPERIMENT)
    print(
        "GUI Araçla MVP Deneyi — "
        f"{REPRESENTATIVE_EXPERIMENT.tool_name} / "
        f"{REPRESENTATIVE_EXPERIMENT.elapsed_minutes} dakika"
    )
    print(f"Otomatik tamamlanan adım: {summary.automatic_step_count}")
    print(f"Müdahale gereken nokta: {summary.intervention_point_count}")
    print(f"Küçük değişiklik sonucu: {REPRESENTATIVE_EXPERIMENT.change_result}")
    print(f"Kod inceleme durumu: {REPRESENTATIVE_EXPERIMENT.code_review_status}")
    print(f"Dikkat noktası: {REPRESENTATIVE_EXPERIMENT.attention_point}")
    print("Kabul kriteri karşılandı: Deney kaydı tamam.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
