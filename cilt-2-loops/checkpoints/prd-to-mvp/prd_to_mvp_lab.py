"""PRD'den çalışan MVP'ye giden araç zincirleme kaydını doğrular.

volume: 2
chapter: 11
book_section: "11.1 Sıfırdan MVP Geliştirme"
concepts:
  - araç zincirleme
  - kabul kriteri
  - insan denetimi
  - yapılandırılmış hata
objectives:
  - "LO-11.1"
  - "LO-11.3"
  - "LO-11.5"
last_verified: "2026-07"

Gömülü kayıt ve süreler temsilîdir. Bu dosya GUI aracı, AI IDE veya CLI ajan
çalıştırmaz; bu araçlarda yapılan denemenin kanıt kaydını denetler.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Sequence


REQUIRED_STAGES = ("iskelet", "derinleştirme", "test")
EXPECTED_CATEGORY_BY_STAGE = {
    "iskelet": "GUI aracı",
    "derinleştirme": "AI IDE",
    "test": "CLI ajan",
}
ALLOWED_CATEGORIES = frozenset(EXPECTED_CATEGORY_BY_STAGE.values())
ALLOWED_DECISIONS = frozenset({"kabul edildi", "düzeltildi", "reddedildi"})


@dataclass(frozen=True)
class Shift:
    """Dakika cinsinden başlangıç ve bitişi olan temsilî vardiya."""

    employee_id: str
    start_minute: int
    end_minute: int


@dataclass(frozen=True)
class ErrorDetail:
    """Bir ajanın sonraki adımı çıkarabileceği yapılandırılmış hata."""

    error: str
    field: str
    message: str
    expected: str

    def as_dict(self) -> dict[str, str]:
        """Hata ayrıntısını JSON'a uygun sözlüğe çevirir."""

        return {
            "error": self.error,
            "field": self.field,
            "message": self.message,
            "expected": self.expected,
        }


class ShiftValidationError(ValueError):
    """Vardiya kabul kriteri karşılanmadığında ayrıntılı hata taşır."""

    def __init__(self, detail: ErrorDetail) -> None:
        super().__init__(detail.message)
        self.detail = detail


@dataclass(frozen=True)
class StageRecord:
    """Araç zincirindeki bir aşamanın görevi, kanıtı ve insan kararını taşır."""

    stage: str
    tool_category: str
    tool_name: str
    task: str
    duration_minutes: int
    observation: str
    decision: str
    output_verified: bool
    test_count: int = 0
    tests_passed: bool | None = None


@dataclass(frozen=True)
class ScenarioResult:
    """MVP kabul kriterini sınayan tek bir senaryonun sonucunu taşır."""

    name: str
    passed: bool
    evidence: str


@dataclass(frozen=True)
class WorkflowReport:
    """Aşama kaydının ve kabul senaryolarının ortak doğrulama özeti."""

    stage_count: int
    category_count: int
    correction_count: int
    passing_test_count: int
    total_test_count: int
    path_label: str
    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        """Kayıt ve testlerde eksik yoksa doğru döndürür."""

        return not self.errors


REPRESENTATIVE_RECORDS = (
    StageRecord(
        stage="iskelet",
        tool_category="GUI aracı",
        tool_name="Kullanılan GUI aracı",
        task="Vardiya ekleme formunu ve haftalık liste iskeletini kurmak",
        duration_minutes=18,
        observation="İskelet çalıştı ancak çakışan iki vardiyayı kabul etti.",
        decision="düzeltildi",
        output_verified=True,
    ),
    StageRecord(
        stage="derinleştirme",
        tool_category="AI IDE",
        tool_name="Kullanılan AI IDE",
        task="PRD'deki vardiya çakışması kuralını uygulamak",
        duration_minutes=22,
        observation="Kısmi örtüşme reddedildi, uç uca vardiyalar kabul edildi.",
        decision="kabul edildi",
        output_verified=True,
    ),
    StageRecord(
        stage="test",
        tool_category="CLI ajan",
        tool_name="Kullanılan CLI ajan",
        task="Geçerli, çakışan ve sınır vardiya senaryolarını sınamak",
        duration_minutes=7,
        observation="Üç kabul senaryosu çalıştı ve üçü de geçti.",
        decision="kabul edildi",
        output_verified=True,
        test_count=3,
        tests_passed=True,
    ),
)


def _normalized(value: str) -> str:
    """Metni karşılaştırma için boşluk ve harf farklarından arındırır."""

    return re.sub(r"\s+", " ", value.strip()).casefold()


def _validate_shift(shift: Shift) -> None:
    """Vardiya alanlarını açık hata ayrıntılarıyla doğrular."""

    if not shift.employee_id.strip():
        raise ShiftValidationError(
            ErrorDetail(
                error="missing_field",
                field="employee_id",
                message="Çalışan kimliği boş bırakılamaz.",
                expected="Boş olmayan bir çalışan kimliği",
            )
        )
    if not 0 <= shift.start_minute < 24 * 60:
        raise ShiftValidationError(
            ErrorDetail(
                error="invalid_field",
                field="start_minute",
                message="Başlangıç dakikası gün sınırları içinde olmalıdır.",
                expected="0 ile 1439 arasında tam sayı",
            )
        )
    if not 0 < shift.end_minute <= 24 * 60:
        raise ShiftValidationError(
            ErrorDetail(
                error="invalid_field",
                field="end_minute",
                message="Bitiş dakikası gün sınırları içinde olmalıdır.",
                expected="1 ile 1440 arasında tam sayı",
            )
        )
    if shift.start_minute >= shift.end_minute:
        raise ShiftValidationError(
            ErrorDetail(
                error="invalid_interval",
                field="end_minute",
                message="Bitiş, başlangıçtan sonra olmalıdır.",
                expected="end_minute > start_minute",
            )
        )


def shifts_overlap(left: Shift, right: Shift) -> bool:
    """Aynı çalışanın yarı açık iki zaman aralığı örtüşüyorsa doğru döndürür."""

    _validate_shift(left)
    _validate_shift(right)
    if left.employee_id != right.employee_id:
        return False
    return left.start_minute < right.end_minute and right.start_minute < left.end_minute


def add_shift(existing: Sequence[Shift], candidate: Shift) -> tuple[Shift, ...]:
    """Çakışmayan vardiyayı ekler; çakışmada makinece ayrıştırılabilir hata verir."""

    _validate_shift(candidate)
    for current in existing:
        if shifts_overlap(current, candidate):
            raise ShiftValidationError(
                ErrorDetail(
                    error="shift_overlap",
                    field="start_minute,end_minute",
                    message=(
                        "Aynı çalışana çakışan iki vardiya atanamaz; "
                        "başlangıç veya bitiş saatini değiştirin."
                    ),
                    expected="Mevcut vardiyalarla örtüşmeyen zaman aralığı",
                )
            )
    return (*existing, candidate)


def run_acceptance_scenarios() -> tuple[ScenarioResult, ...]:
    """PRD'deki çakışma kuralını üç somut senaryoyla sınar."""

    base = Shift("calisan-01", 9 * 60, 12 * 60)
    results: list[ScenarioResult] = []

    try:
        add_shift((base,), Shift("calisan-01", 13 * 60, 15 * 60))
    except ShiftValidationError as error:
        results.append(ScenarioResult("Çakışmayan vardiya", False, str(error)))
    else:
        results.append(
            ScenarioResult(
                "Çakışmayan vardiya", True, "13.00-15.00 vardiyası kabul edildi."
            )
        )

    try:
        add_shift((base,), Shift("calisan-01", 11 * 60, 13 * 60))
    except ShiftValidationError as error:
        results.append(
            ScenarioResult(
                "Kısmi çakışma",
                error.detail.error == "shift_overlap",
                f"Hata kodu: {error.detail.error}",
            )
        )
    else:
        results.append(
            ScenarioResult("Kısmi çakışma", False, "Çakışan vardiya kabul edildi.")
        )

    try:
        add_shift((base,), Shift("calisan-01", 12 * 60, 14 * 60))
    except ShiftValidationError as error:
        results.append(ScenarioResult("Sınır değeri", False, str(error)))
    else:
        results.append(
            ScenarioResult("Sınır değeri", True, "12.00-14.00 vardiyası kabul edildi.")
        )

    return tuple(results)


def validate_workflow(
    records: Sequence[StageRecord],
    scenario_results: Sequence[ScenarioResult],
) -> WorkflowReport:
    """Araç zinciri kaydını bölümün iki erişim yoluna göre doğrular."""

    errors: list[str] = []
    normalized_stages = [_normalized(record.stage) for record in records]
    expected_stages = {_normalized(stage) for stage in REQUIRED_STAGES}

    missing_stages = sorted(expected_stages - set(normalized_stages))
    unexpected_stages = sorted(set(normalized_stages) - expected_stages)
    if missing_stages:
        errors.append("Eksik aşama: " + ", ".join(missing_stages) + ".")
    if unexpected_stages:
        errors.append("Kapsam dışı aşama: " + ", ".join(unexpected_stages) + ".")
    if len(records) != len(REQUIRED_STAGES) or len(set(normalized_stages)) != len(
        records
    ):
        errors.append(
            "İskelet, derinleştirme ve test aşamaları birer kez kaydedilmelidir."
        )

    category_by_stage: dict[str, str] = {}
    for number, record in enumerate(records, start=1):
        stage = _normalized(record.stage)
        category = record.tool_category.strip()
        category_by_stage[stage] = category
        label = record.stage.strip() or f"{number}. kayıt"

        if category not in ALLOWED_CATEGORIES:
            errors.append(f"{label}: araç kategorisi tanınmıyor.")
        required_text_fields = {
            "araç adı": record.tool_name,
            "görev": record.task,
            "gözlem": record.observation,
        }
        for field_name, value in required_text_fields.items():
            if not value.strip():
                errors.append(f"{label}: {field_name} boş bırakılamaz.")
        if record.observation.strip() and len(record.observation.split()) < 5:
            errors.append(f"{label}: gözlem, sonucu somut biçimde açıklamalıdır.")
        if not 1 <= record.duration_minutes <= 240:
            errors.append(f"{label}: süre 1-240 dakika arasında olmalıdır.")
        if record.decision not in ALLOWED_DECISIONS:
            errors.append(
                f"{label}: insan kararı kabul, düzeltme veya ret içermelidir."
            )
        if not record.output_verified:
            errors.append(f"{label}: aşama çıktısı incelenip doğrulanmalıdır.")

        if stage == "test":
            if record.test_count < 2:
                errors.append("Test aşamasında en az iki test çalıştırılmalıdır.")
            if record.tests_passed is not True:
                errors.append("Testler geçmeden MVP tamamlandı sayılamaz.")

    categories = {record.tool_category.strip() for record in records}
    if len(categories) == 1:
        path_label = "tek kategoriyle üç aşama"
    elif len(categories) == 3:
        path_label = "GUI aracı → AI IDE → CLI ajan"
        for stage, expected_category in EXPECTED_CATEGORY_BY_STAGE.items():
            if category_by_stage.get(_normalized(stage)) != expected_category:
                errors.append(
                    f"{stage} aşaması üç kategorili yolda {expected_category} ile yürütülmelidir."
                )
    else:
        path_label = "eksik araç yolu"
        errors.append(
            "Araç yolu ya tek kategoriyle üç aşamayı ya da üç kategorinin tamamını içermelidir."
        )

    correction_count = sum(
        record.decision in {"düzeltildi", "reddedildi"} for record in records
    )
    if correction_count == 0:
        errors.append("En az bir araç çıktısı düzeltilmeli veya reddedilmelidir.")

    passing_test_count = sum(result.passed for result in scenario_results)
    if len(scenario_results) < 2:
        errors.append("Kabul kriteri en az iki senaryoyla sınanmalıdır.")
    if passing_test_count != len(scenario_results):
        errors.append("Kabul senaryolarının tamamı geçmelidir.")

    return WorkflowReport(
        stage_count=len(set(normalized_stages) & expected_stages),
        category_count=len(categories & ALLOWED_CATEGORIES),
        correction_count=correction_count,
        passing_test_count=passing_test_count,
        total_test_count=len(scenario_results),
        path_label=path_label,
        errors=tuple(dict.fromkeys(errors)),
    )


def format_report(report: WorkflowReport) -> str:
    """Doğrulama sonucunu terminalde okunacak kısa özete çevirir."""

    lines = [
        "PRD'den MVP'ye Araç Zincirleme Kaydı",
        "PRD kabul kriteri: Aynı çalışana çakışan iki vardiya atanamaz.",
        f"Aşama kaydı: {report.stage_count}/3",
        f"Araç yolu: {report.path_label}",
        f"Düzeltilen veya reddedilen çıktı: {report.correction_count}",
        f"Kabul testleri: {report.passing_test_count}/{report.total_test_count} geçti",
    ]
    if report.is_valid:
        lines.append(
            "Kabul kriteri karşılandı: Üç aşama kaydedildi, bir çıktı düzeltildi ve testler geçti."
        )
    else:
        lines.append("Kabul kriteri karşılanmadı:")
        lines.extend(f"- {error}" for error in report.errors)
    return "\n".join(lines)


def main() -> int:
    """Temsilî araç zincirini doğrular ve yapılandırılmış hata örneğini gösterir."""

    scenarios = run_acceptance_scenarios()
    report = validate_workflow(REPRESENTATIVE_RECORDS, scenarios)
    print(format_report(report))

    try:
        add_shift(
            (Shift("calisan-01", 9 * 60, 12 * 60),),
            Shift("calisan-01", 11 * 60, 13 * 60),
        )
    except ShiftValidationError as error:
        print("Örnek hata gövdesi:")
        print(json.dumps(error.detail.as_dict(), ensure_ascii=False, indent=2))

    return 0 if report.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
