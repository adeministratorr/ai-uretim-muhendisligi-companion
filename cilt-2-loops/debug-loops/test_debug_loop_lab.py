"""Minimal repro, güvenli düzeltme ve HTML eşleniği için regresyon testleri."""

from html.parser import HTMLParser
from pathlib import Path

from debug_loop_lab import (
    Schedule,
    Shift,
    add_shift_to_schedule,
    build_debug_report,
    format_report,
    run_fixed_scenario,
    run_minimal_repro,
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


def test_minimal_repro_proves_shared_default_list() -> None:
    evidence = run_minimal_repro()

    assert evidence.expected_second == ("B",)
    assert evidence.actual_first == ("A", "B")
    assert evidence.actual_second == ("A", "B")
    assert evidence.shares_same_list


def test_fixed_function_keeps_default_lists_separate() -> None:
    first, second = run_fixed_scenario()

    assert first == ("A",)
    assert second == ("B",)


def test_fixed_function_preserves_supplied_empty_list() -> None:
    supplied: list[Shift] = []
    schedule = Schedule("Dış liste kullanan plan")

    result = add_shift_to_schedule(schedule, Shift("A"), supplied)

    assert result is schedule
    assert schedule.shifts is supplied
    assert [shift.shift_id for shift in supplied] == ["A"]


def test_debug_report_records_two_commits_and_regression_note() -> None:
    report = build_debug_report()
    output = format_report(report)

    assert report.fix_is_valid
    assert report.regression_passed == report.regression_total == 3
    assert output.count("Commit 1:") == 1
    assert output.count("Commit 2:") == 1
    assert "Commit 3:" not in output
    assert "Regression: 3/3 kontrol geçti." in output


def test_html_is_balanced_and_contains_required_lab_context() -> None:
    html_path = Path(__file__).with_name("debug_loop_lab.html")
    html = html_path.read_text(encoding="utf-8")
    parser = BalancedHTMLParser()

    parser.feed(html)
    parser.close()

    assert parser.stack == []
    assert '<html lang="tr">' in html
    assert "volume: 2" in html
    assert "chapter: 12" in html
    assert 'last_verified: "2026-07"' in html
    assert "Açıkla, hipotez kur, kanıt göster" in html
    assert "Senaryo temsilîdir" in html


def test_html_links_to_python_readme_and_repository() -> None:
    html = Path(__file__).with_name("debug_loop_lab.html").read_text(encoding="utf-8")
    repository = "https://github.com/adeministratorr/ai-uretim-muhendisligi-companion"

    assert f'{repository}/blob/main/cilt-2-loops/debug-loops/debug_loop_lab.py' in html
    assert f'{repository}/tree/main/cilt-2-loops/debug-loops' in html
    assert f'href="{repository}"' in html
