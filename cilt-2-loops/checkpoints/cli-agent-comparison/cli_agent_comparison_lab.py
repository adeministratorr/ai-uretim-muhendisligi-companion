"""Aynı hata düzeltme görevinin CLI ajan çıktıları için karşılaştırma kaydı üretir.

volume: 2
chapter: 06
book_section: "6.9 CLI Ajan Seçim Matrisi"
concepts:
  - CLI ajan
  - ortak görev tarifi
  - onay modu
  - diff karşılaştırması
objectives:
  - "LO-6.1"
  - "LO-6.2"
  - "LO-6.6"
last_verified: "2026-07"

Gömülü araç kayıtları temsilîdir; gerçek bir ürün karşılaştırması veya benchmark
olarak kullanılmamalıdır. Bu program yapıştırılan diff'i çalıştırmaz.
"""

from collections.abc import Sequence
from dataclasses import dataclass


MIN_RUNS = 1
MAX_RUNS = 3

APPROVAL_BEFORE_CHANGE = "değişiklik öncesi onay istedi"
APPROVAL_WITHOUT_ASKING = "onay almadan değiştirdi"
APPROVAL_DIFF_ONLY = "yalnızca diff sundu"
APPROVAL_BEHAVIORS = frozenset(
    {APPROVAL_BEFORE_CHANGE, APPROVAL_WITHOUT_ASKING, APPROVAL_DIFF_ONLY}
)

TEST_PASSED = "geçti"
TEST_FAILED = "geçmedi"
TEST_NOT_RUN = "çalıştırılmadı"
TEST_RESULTS = frozenset({TEST_PASSED, TEST_FAILED, TEST_NOT_RUN})

TASK_PROMPT = (
    "get_user_city fonksiyonunda, user sözlüğünde address anahtarı yoksa veya "
    "değeri boşsa (None) oluşan hatayı düzelt. Fonksiyon bu durumda None "
    "döndürmeli; mevcut davranış (adres varsa şehri döndürmek) değişmemeli. "
    "Yalnızca ilgili fonksiyona dokun."
)

STARTER_CODE = '''def get_user_city(user):
    return user["address"]["city"]'''

ACCEPTANCE_CRITERIA = (
    "Adres varsa şehir değeri döner.",
    "address anahtarı yoksa None döner.",
    "address değeri None ise None döner.",
    "Yalnızca get_user_city fonksiyonu değişir.",
)


@dataclass(frozen=True)
class AgentRun:
    """Bir CLI ajan denemesindeki gözlemleri tutar."""

    tool_name: str
    proposed_diff: str
    rationale: str
    suggested_test: str
    test_result: str
    approval_behavior: str
    scope_met: bool


@dataclass(frozen=True)
class ComparisonSummary:
    """Doğrulanmış kayıtların puanlamasız sayısal özetini tutar."""

    tool_count: int
    suggested_test_count: int
    scope_met_count: int
    passed_test_count: int


REPRESENTATIVE_RUNS = (
    AgentRun(
        tool_name="Araç A",
        proposed_diff='''@@
 def get_user_city(user):
-    return user["address"]["city"]
+    address = user.get("address")
+    return address.get("city") if address else None''',
        rationale=(
            "Adres bulunmadığında iç içe sözlük erişimini durdurur ve beklenen None "
            "değerini döndürür."
        ),
        suggested_test=(
            "address anahtarı olmayan ve address değeri None olan iki durum sınanmalıdır."
        ),
        test_result=TEST_PASSED,
        approval_behavior=APPROVAL_BEFORE_CHANGE,
        scope_met=True,
    ),
    AgentRun(
        tool_name="Araç B",
        proposed_diff='''@@
 def get_user_city(user):
-    return user["address"]["city"]
+    return (user.get("address") or {}).get("city")''',
        rationale=(
            "Eksik veya None olan adresi boş sözlüğe çevirerek şehir erişimini güvenli "
            "tutar."
        ),
        suggested_test=(
            "Geçerli adres, eksik address ve None address durumları birlikte sınanmalıdır."
        ),
        test_result=TEST_PASSED,
        approval_behavior=APPROVAL_DIFF_ONLY,
        scope_met=True,
    ),
)

APPROVAL_MODE_NOTE = (
    "Araç A değişiklik öncesinde onay istedi; Araç B yalnızca diff sunduğu için dosya "
    "yazma onayı gerektirmedi."
)


def _is_complete_text(text: str, minimum_words: int = 4) -> bool:
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
    return len(lines) >= 2 and "get_user_city" in diff and has_addition


def validate_comparison(
    runs: Sequence[AgentRun],
    approval_mode_note: str,
) -> list[str]:
    """Kayıtları laboratuvarın açık kabul ölçütlerine göre doğrular."""

    errors: list[str] = []
    if not MIN_RUNS <= len(runs) <= MAX_RUNS:
        errors.append(f"Karşılaştırma {MIN_RUNS}-{MAX_RUNS} araç içermelidir.")

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

        if not _looks_like_target_diff(run.proposed_diff):
            errors.append(
                f"{label} diff'i get_user_city fonksiyonunu ve bir ekleme satırını "
                "göstermelidir."
            )
        if not _is_complete_text(run.rationale):
            errors.append(f"{label} gerekçesi tamamlanmış bir cümle olmalıdır.")
        if run.suggested_test.strip() and not _is_complete_text(run.suggested_test):
            errors.append(
                f"{label} test önerisi yazıldıysa tamamlanmış bir cümle olmalıdır."
            )
        if run.test_result not in TEST_RESULTS:
            errors.append(f"{label} test sonucu geçerli seçeneklerden biri olmalıdır.")
        if run.approval_behavior not in APPROVAL_BEHAVIORS:
            errors.append(f"{label} onay davranışı geçerli seçeneklerden biri olmalıdır.")
        if type(run.scope_met) is not bool:
            errors.append(f"{label} kapsam sonucu evet/hayır olarak seçilmelidir.")

    if "onay" not in approval_mode_note.casefold() or not _is_complete_text(
        approval_mode_note,
        minimum_words=6,
    ):
        errors.append(
            "Onay modu notu, gözlemin onay kavramıyla ilişkisini tamamlanmış bir "
            "cümleyle açıklamalıdır."
        )
    return errors


def summarize_comparison(
    runs: Sequence[AgentRun],
    approval_mode_note: str,
) -> ComparisonSummary:
    """Kabul ölçütlerini geçen kayıtlar için puanlamasız bir özet üretir."""

    errors = validate_comparison(runs, approval_mode_note)
    if errors:
        raise ValueError("Özet üretilemedi: " + " ".join(errors))

    return ComparisonSummary(
        tool_count=len(runs),
        suggested_test_count=sum(bool(run.suggested_test.strip()) for run in runs),
        scope_met_count=sum(run.scope_met for run in runs),
        passed_test_count=sum(run.test_result == TEST_PASSED for run in runs),
    )


def main() -> int:
    """Temsilî kayıtları doğrular ve özeti terminale yazar."""

    errors = validate_comparison(REPRESENTATIVE_RUNS, APPROVAL_MODE_NOTE)
    if errors:
        print("Kabul kriteri karşılanmadı:")
        for error in errors:
            print(f"- {error}")
        return 1

    summary = summarize_comparison(REPRESENTATIVE_RUNS, APPROVAL_MODE_NOTE)
    print(f"CLI Ajan Karşılaştırması — {summary.tool_count} araç")
    for run in REPRESENTATIVE_RUNS:
        scope = "uygun" if run.scope_met else "aşıldı"
        test_suggestion = "var" if run.suggested_test.strip() else "yok"
        print(
            f"{run.tool_name}: test={run.test_result}, kapsam={scope}, "
            f"onay={run.approval_behavior}, test önerisi={test_suggestion}"
        )
    print(
        f"Test öneren araç: {summary.suggested_test_count}/{summary.tool_count}"
    )
    print(
        "Hedef fonksiyonla sınırlı kalan diff: "
        f"{summary.scope_met_count}/{summary.tool_count}"
    )
    print(f"Onay modu notu: {APPROVAL_MODE_NOTE}")
    print("Kabul kriteri karşılandı: Karşılaştırma kaydı tamam.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
