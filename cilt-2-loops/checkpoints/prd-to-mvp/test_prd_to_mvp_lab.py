"""PRD'den MVP'ye araç zincirinin kabul ve ret durumları."""

from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path

from prd_to_mvp_lab import (
    REPRESENTATIVE_RECORDS,
    Shift,
    ShiftValidationError,
    add_shift,
    format_report,
    main,
    run_acceptance_scenarios,
    shifts_overlap,
    validate_workflow,
)


class BalancedHTMLParser(HTMLParser):
    """Tek dosyalık laboratuvarın temel etiket dengesini denetler."""

    VOID_ELEMENTS = frozenset({"meta", "input", "br", "hr", "img", "link"})

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag not in self.VOID_ELEMENTS:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        assert self.stack, f"Kapanış etiketi başlangıçsız: {tag}"
        assert self.stack.pop() == tag, f"Etiket sırası bozuk: {tag}"


def test_partial_overlap_is_rejected_with_structured_error():
    existing = (Shift("calisan-01", 9 * 60, 12 * 60),)

    try:
        add_shift(existing, Shift("calisan-01", 11 * 60, 13 * 60))
    except ShiftValidationError as error:
        assert error.detail.error == "shift_overlap"
        assert error.detail.field == "start_minute,end_minute"
        assert "başlangıç veya bitiş saatini değiştirin" in error.detail.message
        assert error.detail.as_dict()["expected"]
    else:
        raise AssertionError("Çakışan vardiya reddedilmeliydi")


def test_touching_boundaries_do_not_overlap():
    morning = Shift("calisan-01", 9 * 60, 12 * 60)
    afternoon = Shift("calisan-01", 12 * 60, 14 * 60)

    assert not shifts_overlap(morning, afternoon)
    assert add_shift((morning,), afternoon) == (morning, afternoon)


def test_different_employees_may_have_same_interval():
    first = Shift("calisan-01", 9 * 60, 12 * 60)
    second = Shift("calisan-02", 9 * 60, 12 * 60)

    assert not shifts_overlap(first, second)
    assert add_shift((first,), second) == (first, second)


def test_invalid_interval_identifies_end_field():
    try:
        add_shift((), Shift("calisan-01", 12 * 60, 11 * 60))
    except ShiftValidationError as error:
        assert error.detail.error == "invalid_interval"
        assert error.detail.field == "end_minute"
        assert error.detail.expected == "end_minute > start_minute"
    else:
        raise AssertionError("Geçersiz zaman aralığı reddedilmeliydi")


def test_representative_workflow_meets_acceptance_criteria():
    scenarios = run_acceptance_scenarios()
    report = validate_workflow(REPRESENTATIVE_RECORDS, scenarios)

    assert report.is_valid
    assert report.errors == ()
    assert report.stage_count == 3
    assert report.category_count == 3
    assert report.correction_count == 1
    assert report.passing_test_count == report.total_test_count == 3
    assert report.path_label == "GUI aracı → AI IDE → CLI ajan"


def test_single_category_may_run_all_three_stages():
    records = tuple(
        replace(record, tool_category="AI IDE", tool_name="Kullanılan tek AI IDE")
        for record in REPRESENTATIVE_RECORDS
    )

    report = validate_workflow(records, run_acceptance_scenarios())

    assert report.is_valid
    assert report.path_label == "tek kategoriyle üç aşama"
    assert report.category_count == 1


def test_two_category_path_is_rejected():
    records = (
        REPRESENTATIVE_RECORDS[0],
        replace(REPRESENTATIVE_RECORDS[1], tool_category="GUI aracı"),
        REPRESENTATIVE_RECORDS[2],
    )

    report = validate_workflow(records, run_acceptance_scenarios())

    assert not report.is_valid
    assert any("tek kategoriyle üç aşamayı" in error for error in report.errors)


def test_each_stage_must_be_recorded_once():
    report = validate_workflow(REPRESENTATIVE_RECORDS[:2], run_acceptance_scenarios())

    assert not report.is_valid
    assert "Eksik aşama: test." in report.errors


def test_at_least_one_output_must_be_corrected_or_rejected():
    records = tuple(
        replace(record, decision="kabul edildi") for record in REPRESENTATIVE_RECORDS
    )

    report = validate_workflow(records, run_acceptance_scenarios())

    assert not report.is_valid
    assert "En az bir araç çıktısı düzeltilmeli veya reddedilmelidir." in report.errors


def test_test_stage_cannot_pass_with_failed_or_too_few_tests():
    records = (
        *REPRESENTATIVE_RECORDS[:2],
        replace(REPRESENTATIVE_RECORDS[2], test_count=1, tests_passed=False),
    )

    report = validate_workflow(records, run_acceptance_scenarios())

    assert "Test aşamasında en az iki test çalıştırılmalıdır." in report.errors
    assert "Testler geçmeden MVP tamamlandı sayılamaz." in report.errors


def test_report_keeps_correction_and_test_evidence_visible():
    output = format_report(
        validate_workflow(REPRESENTATIVE_RECORDS, run_acceptance_scenarios())
    )

    assert "Düzeltilen veya reddedilen çıktı: 1" in output
    assert "Kabul testleri: 3/3 geçti" in output
    assert "Kabul kriteri karşılandı" in output


def test_main_returns_success_and_prints_structured_error(capsys):
    assert main() == 0
    output = capsys.readouterr().out
    assert "Kabul kriteri karşılandı" in output
    assert '"error": "shift_overlap"' in output
    assert '"field": "start_minute,end_minute"' in output


def test_html_is_balanced_and_contains_required_explanations_and_links():
    html_path = Path(__file__).with_name("prd_to_mvp_lab.html")
    html = html_path.read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)

    assert parser.stack == []
    assert "Kavram — Araç Zincirleme" in html
    assert "Temsilîlik Notu" in html
    assert 'last_verified: "2026-07"' in html
    assert "prefers-reduced-motion" in html
    assert "shift_overlap" in html
    assert (
        html.count("github.com/adeministratorr/ai-uretim-muhendisligi-companion") >= 3
    )
