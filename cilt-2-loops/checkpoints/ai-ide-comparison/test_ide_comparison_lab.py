"""Yapay zekâ IDE karşılaştırıcısının temel kabul ve ret durumları."""

from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path

import pytest

from ide_comparison_lab import (
    ACCEPTANCE_CRITERIA,
    REPRESENTATIVE_RUNS,
    TASK_PROMPT,
    summarize_comparison,
    validate_comparison,
)


class BalancedHTMLParser(HTMLParser):
    """Tek dosyalık laboratuvarın temel etiket dengesini denetler."""

    VOID_ELEMENTS = frozenset({"meta", "input", "br", "hr", "img", "link"})

    def __init__(self):
        super().__init__()
        self.stack: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID_ELEMENTS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        assert self.stack, f"Kapanış etiketi başlangıçsız: {tag}"
        assert self.stack.pop() == tag, f"Etiket sırası bozuk: {tag}"


def test_representative_runs_meet_acceptance_criteria():
    assert validate_comparison(TASK_PROMPT, ACCEPTANCE_CRITERIA, REPRESENTATIVE_RUNS) == []


def test_comparison_rejects_fewer_than_two_tools():
    errors = validate_comparison(TASK_PROMPT, ACCEPTANCE_CRITERIA, REPRESENTATIVE_RUNS[:1])
    assert "Karşılaştırma 2 veya 3 araç içermelidir." in errors


@pytest.mark.parametrize(
    ("task_prompt", "criteria", "expected"),
    [
        ("", ACCEPTANCE_CRITERIA, "Ortak görev tarifi boş bırakılamaz."),
        (TASK_PROMPT, ("Tek ölçüt",), "En az 2 ortak kabul ölçütü yazılmalıdır."),
        (
            TASK_PROMPT,
            ("Aynı ölçüt", "aynı ölçüt"),
            "Ortak kabul ölçütleri yinelenmemelidir.",
        ),
    ],
)
def test_comparison_rejects_incomplete_common_setup(task_prompt, criteria, expected):
    errors = validate_comparison(task_prompt, criteria, REPRESENTATIVE_RUNS)
    assert expected in errors


def test_comparison_rejects_duplicate_tool_names():
    duplicate = replace(REPRESENTATIVE_RUNS[1], tool_name="araç a")
    errors = validate_comparison(
        TASK_PROMPT,
        ACCEPTANCE_CRITERIA,
        (REPRESENTATIVE_RUNS[0], duplicate),
    )
    assert any("yineleniyor" in error for error in errors)


def test_comparison_rejects_a_nonboolean_initial_test_result():
    invalid = replace(REPRESENTATIVE_RUNS[0], initial_test_passed=1)
    errors = validate_comparison(
        TASK_PROMPT,
        ACCEPTANCE_CRITERIA,
        (invalid, REPRESENTATIVE_RUNS[1]),
    )
    assert any("ilk test sonucu" in error for error in errors)


def test_comparison_rejects_negative_correction_rounds():
    invalid = replace(REPRESENTATIVE_RUNS[0], correction_rounds=-1)
    errors = validate_comparison(
        TASK_PROMPT,
        ACCEPTANCE_CRITERIA,
        (invalid, REPRESENTATIVE_RUNS[1]),
    )
    assert any("düzeltme turu" in error for error in errors)


def test_comparison_rejects_readability_outside_scale():
    invalid = replace(REPRESENTATIVE_RUNS[0], diff_readability=6)
    errors = validate_comparison(
        TASK_PROMPT,
        ACCEPTANCE_CRITERIA,
        (invalid, REPRESENTATIVE_RUNS[1]),
    )
    assert any("diff okunabilirliği" in error for error in errors)


def test_comparison_rejects_an_empty_surprise_or_error():
    invalid = replace(REPRESENTATIVE_RUNS[0], surprise_or_error="  ")
    errors = validate_comparison(
        TASK_PROMPT,
        ACCEPTANCE_CRITERIA,
        (invalid, REPRESENTATIVE_RUNS[1]),
    )
    assert any("sürpriz veya hata" in error for error in errors)


def test_comparison_rejects_an_incomplete_standout_sentence():
    invalid = replace(REPRESENTATIVE_RUNS[0], standout_reason="Diff düzenliydi")
    errors = validate_comparison(
        TASK_PROMPT,
        ACCEPTANCE_CRITERIA,
        (invalid, REPRESENTATIVE_RUNS[1]),
    )
    assert any("tek ve tamamlanmış bir cümle" in error for error in errors)


def test_summary_keeps_metrics_separate():
    summary = summarize_comparison(TASK_PROMPT, ACCEPTANCE_CRITERIA, REPRESENTATIVE_RUNS)
    assert summary.initial_passes == ("Araç B",)
    assert summary.fewest_correction_rounds == 0
    assert summary.fewest_correction_tools == ("Araç B",)
    assert summary.highest_readability == 4
    assert summary.highest_readability_tools == ("Araç A",)


def test_html_has_required_blocks_links_and_balanced_tags():
    html = Path("ide_comparison_lab.html").read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)
    parser.close()

    assert parser.stack == []
    assert "Kavram — Aynı Görev, Ortak Kabul Ölçütü" in html
    assert "Temsilîlik Notu" in html
    assert html.count("https://github.com/adeministratorr/") == 3
    assert 'last_verified: "2026-07"' in html
