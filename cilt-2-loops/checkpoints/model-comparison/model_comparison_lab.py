"""Aynı refactor görevinin model çıktıları için karşılaştırma kaydı üretir.

volume: 2
chapter: 07
book_section: "7.10 Kod Benchmark'larının Sınırları"
concepts:
  - ortak görev tarifi
  - model karşılaştırması
  - bağlam penceresi
  - insan denetimi
objectives:
  - "LO-7.1"
  - "LO-7.2"
  - "LO-7.3"
  - "LO-7.5"
  - "LO-7.6"
last_verified: "2026-07"

Gömülü deneme kayıtları temsilîdir; gerçek bir model karşılaştırması veya benchmark
olarak kullanılmamalıdır. Bu program yapıştırılan diff'i çalıştırmaz.
"""

from collections.abc import Sequence
from dataclasses import dataclass


MIN_RUNS = 2
MAX_RUNS = 3

TEST_PASSED = "geçti"
TEST_FAILED = "geçmedi"
TEST_NOT_RUN = "çalıştırılmadı"
TEST_RESULTS = frozenset({TEST_PASSED, TEST_FAILED, TEST_NOT_RUN})

TASK_PROMPT = (
    "normalize_labels fonksiyonunu okunabilirliği artıracak biçimde yeniden düzenle. "
    "Fonksiyonun adı ve parametresi değişmeyecek; mevcut davranış testleri geçecek, "
    "yeni bağımlılık eklenmeyecek ve yalnızca ilgili fonksiyona dokunulacak."
)

STARTER_CODE = '''def normalize_labels(labels):
    normalized = []
    for label in labels:
        cleaned = label.strip().casefold()
        if cleaned:
            if cleaned not in normalized:
                normalized.append(cleaned)
    return normalized'''

ACCEPTANCE_CRITERIA = (
    "Boşluklar temizlenir ve etiketler küçük harfe çevrilir.",
    "Boş ve yinelenen etiketler sonuçtan çıkarılır.",
    "İlk görülme sırası korunur.",
    "normalize_labels(labels) arayüzü değişmez.",
    "Yeni bağımlılık eklenmez ve yalnızca hedef fonksiyon değişir.",
)


@dataclass(frozen=True)
class ModelRun:
    """Bir model veya model katmanı denemesindeki gözlemleri tutar."""

    run_label: str
    proposed_diff: str
    test_result: str
    changed_file_count: int
    interface_preserved: bool
    readability_score: int
    readability_note: str
    call_count: int
    context_fit: bool
    observation: str


@dataclass(frozen=True)
class ComparisonSummary:
    """Doğrulanmış kayıtların puanlamasız sayısal özetini tutar."""

    run_count: int
    passed_test_count: int
    interface_preserved_count: int
    context_fit_count: int


REPRESENTATIVE_RUNS = (
    ModelRun(
        run_label="Deneme A",
        proposed_diff='''@@
 def normalize_labels(labels):
-    normalized = []
-    for label in labels:
-        cleaned = label.strip().casefold()
-        if cleaned:
-            if cleaned not in normalized:
-                normalized.append(cleaned)
-    return normalized
+    cleaned = (label.strip().casefold() for label in labels)
+    return list(dict.fromkeys(label for label in cleaned if label))''',
        test_result=TEST_PASSED,
        changed_file_count=1,
        interface_preserved=True,
        readability_score=4,
        readability_note=(
            "Tekrarlanan koşulları kaldırıyor; iç içe üreteç ifadesi ilk okumada "
            "dikkat gerektiriyor."
        ),
        call_count=2,
        context_fit=True,
        observation=(
            "Çözüm kısa ve testleri geçiyor; ancak üreteç ifadesi ekipteki yeni "
            "geliştiriciler için açıklama gerektirebilir."
        ),
    ),
    ModelRun(
        run_label="Deneme B",
        proposed_diff='''@@
 def normalize_labels(labels):
     normalized = []
+    seen = set()
     for label in labels:
         cleaned = label.strip().casefold()
-        if cleaned:
-            if cleaned not in normalized:
-                normalized.append(cleaned)
+        if cleaned and cleaned not in seen:
+            seen.add(cleaned)
+            normalized.append(cleaned)
     return normalized''',
        test_result=TEST_PASSED,
        changed_file_count=1,
        interface_preserved=True,
        readability_score=5,
        readability_note=(
            "Tek koşul ve açık bir seen kümesi kullandığı için veri akışı kolay izleniyor."
        ),
        call_count=3,
        context_fit=True,
        observation=(
            "Çözüm birkaç satır daha uzun; buna karşılık yinelenen etiket denetimini "
            "açıkça gösteriyor."
        ),
    ),
)

DECISION_NOTE = (
    "Deneme B'yi seçtim; testler geçti, dışa açık arayüz korundu ve okunabilirlik "
    "notu daha güçlüydü. İki denemede de bağlam yeterliydi; Deneme A daha az çağrı "
    "kullansa da bu fark tek başına kararı belirlemedi."
)


def _is_complete_text(text: str, minimum_words: int = 5) -> bool:
    """Metnin yeterli uzunlukta ve tamamlanmış olup olmadığını denetler."""

    stripped = text.strip()
    return (
        len(stripped.split()) >= minimum_words
        and bool(stripped)
        and stripped[-1] in ".?!"
    )


def _looks_like_target_diff(diff: str) -> bool:
    """Diff'in hedef fonksiyonu ve en az bir ekleme satırını gösterdiğini denetler."""

    lines = [line for line in diff.splitlines() if line.strip()]
    has_addition = any(line.startswith("+") and not line.startswith("+++") for line in lines)
    return len(lines) >= 3 and "normalize_labels" in diff and has_addition


def validate_comparison(
    runs: Sequence[ModelRun],
    decision_note: str,
) -> list[str]:
    """Kayıtları laboratuvarın açık kabul ölçütlerine göre doğrular."""

    errors: list[str] = []
    if not MIN_RUNS <= len(runs) <= MAX_RUNS:
        errors.append(f"Karşılaştırma {MIN_RUNS}-{MAX_RUNS} deneme içermelidir.")

    seen_labels: set[str] = set()
    for run_number, run in enumerate(runs, start=1):
        label = f"{run_number}. deneme"
        run_label = run.run_label.strip()
        if not run_label:
            errors.append(f"{label} etiketi boş bırakılamaz.")
        elif run_label.casefold() in seen_labels:
            errors.append(f'{label} etiketi "{run_label}" yineleniyor.')
        else:
            seen_labels.add(run_label.casefold())

        if not _looks_like_target_diff(run.proposed_diff):
            errors.append(
                f"{label} diff'i normalize_labels fonksiyonunu ve bir ekleme "
                "satırını göstermelidir."
            )
        if run.test_result not in TEST_RESULTS:
            errors.append(f"{label} test sonucu geçerli seçeneklerden biri olmalıdır.")
        if type(run.changed_file_count) is not int or not 1 <= run.changed_file_count <= 20:
            errors.append(f"{label} değişen dosya sayısı 1-20 arasında olmalıdır.")
        if type(run.interface_preserved) is not bool:
            errors.append(f"{label} arayüz sonucu evet/hayır olarak seçilmelidir.")
        if type(run.readability_score) is not int or not 1 <= run.readability_score <= 5:
            errors.append(f"{label} okunabilirlik puanı 1-5 arasında olmalıdır.")
        if not _is_complete_text(run.readability_note):
            errors.append(
                f"{label} okunabilirlik notu tamamlanmış bir cümle olmalıdır."
            )
        if type(run.call_count) is not int or not 1 <= run.call_count <= 100:
            errors.append(f"{label} çağrı sayısı 1-100 arasında olmalıdır.")
        if type(run.context_fit) is not bool:
            errors.append(f"{label} bağlam sonucu evet/hayır olarak seçilmelidir.")
        if not _is_complete_text(run.observation, minimum_words=6):
            errors.append(f"{label} gözlemi tamamlanmış bir cümle olmalıdır.")

    normalized_note = decision_note.casefold()
    required_terms = ("test", "arayüz", "okunabilir", "çağrı", "bağlam")
    if not _is_complete_text(decision_note, minimum_words=18) or any(
        term not in normalized_note for term in required_terms
    ):
        errors.append(
            "Karar notu test, arayüz, okunabilirlik, çağrı ve bağlam gözlemlerini "
            "tamamlanmış cümlelerle açıklamalıdır."
        )
    elif runs and not any(
        normalized_note.startswith(run.run_label.casefold()) for run in runs
    ):
        errors.append("Karar notu tercih edilen deneme etiketini belirtmelidir.")
    return errors


def summarize_comparison(
    runs: Sequence[ModelRun],
    decision_note: str,
) -> ComparisonSummary:
    """Kabul ölçütlerini geçen kayıtlar için puanlamasız bir özet üretir."""

    errors = validate_comparison(runs, decision_note)
    if errors:
        raise ValueError("Özet üretilemedi: " + " ".join(errors))

    return ComparisonSummary(
        run_count=len(runs),
        passed_test_count=sum(run.test_result == TEST_PASSED for run in runs),
        interface_preserved_count=sum(run.interface_preserved for run in runs),
        context_fit_count=sum(run.context_fit for run in runs),
    )


def main() -> int:
    """Temsilî kayıtları doğrular ve özeti terminale yazar."""

    errors = validate_comparison(REPRESENTATIVE_RUNS, DECISION_NOTE)
    if errors:
        print("Kabul kriteri karşılanmadı:")
        for error in errors:
            print(f"- {error}")
        return 1

    summary = summarize_comparison(REPRESENTATIVE_RUNS, DECISION_NOTE)
    print(f"Model Çıktısı Karşılaştırması — {summary.run_count} deneme")
    for run in REPRESENTATIVE_RUNS:
        interface = "korundu" if run.interface_preserved else "değişti"
        context = "yeterli" if run.context_fit else "yetersiz"
        print(
            f"{run.run_label}: test={run.test_result}, dosya={run.changed_file_count}, "
            f"arayüz={interface}, okunabilirlik={run.readability_score}/5, "
            f"çağrı={run.call_count}, bağlam={context}"
        )
    print(f"Testleri geçen deneme: {summary.passed_test_count}/{summary.run_count}")
    print(
        "Arayüzü koruyan deneme: "
        f"{summary.interface_preserved_count}/{summary.run_count}"
    )
    print(f"Bağlamı yeterli deneme: {summary.context_fit_count}/{summary.run_count}")
    print(f"Karar notu: {DECISION_NOTE}")
    print("Kabul kriteri karşılandı: Karşılaştırma kaydı tamam.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
