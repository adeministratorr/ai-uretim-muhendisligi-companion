"""CLI ajan karşılaştırıcısının temel kabul ve ret durumları."""

from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path

import pytest

from cli_agent_comparison_lab import (
    APPROVAL_BEFORE_CHANGE,
    APPROVAL_MODE_NOTE,
    REPRESENTATIVE_RUNS,
    TEST_NOT_RUN,
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
    assert validate_comparison(REPRESENTATIVE_RUNS, APPROVAL_MODE_NOTE) == []


def test_single_tool_record_is_accepted():
    assert validate_comparison(REPRESENTATIVE_RUNS[:1], APPROVAL_MODE_NOTE) == []


@pytest.mark.parametrize("runs", [(), REPRESENTATIVE_RUNS * 2])
def test_comparison_rejects_tool_count_outside_range(runs):
    errors = validate_comparison(runs, APPROVAL_MODE_NOTE)
    assert "Karşılaştırma 1-3 araç içermelidir." in errors


def test_comparison_rejects_duplicate_tool_names():
    duplicate = replace(REPRESENTATIVE_RUNS[1], tool_name="araç a")
    errors = validate_comparison((REPRESENTATIVE_RUNS[0], duplicate), APPROVAL_MODE_NOTE)
    assert any("yineleniyor" in error for error in errors)


def test_comparison_rejects_empty_tool_name():
    invalid = replace(REPRESENTATIVE_RUNS[0], tool_name="  ")
    errors = validate_comparison((invalid,), APPROVAL_MODE_NOTE)
    assert "1. araç adı boş bırakılamaz." in errors


@pytest.mark.parametrize(
    "proposed_diff",
    [
        "+ return None",
        "def get_user_city(user):\n    return None",
    ],
)
def test_comparison_rejects_diff_without_target_and_addition(proposed_diff):
    invalid = replace(REPRESENTATIVE_RUNS[0], proposed_diff=proposed_diff)
    errors = validate_comparison((invalid,), APPROVAL_MODE_NOTE)
    assert any("get_user_city" in error and "ekleme satırını" in error for error in errors)


def test_comparison_rejects_incomplete_rationale():
    invalid = replace(REPRESENTATIVE_RUNS[0], rationale="Adres erişimini düzeltir")
    errors = validate_comparison((invalid,), APPROVAL_MODE_NOTE)
    assert "1. araç gerekçesi tamamlanmış bir cümle olmalıdır." in errors


def test_empty_test_suggestion_is_allowed():
    valid = replace(
        REPRESENTATIVE_RUNS[0],
        suggested_test="",
        test_result=TEST_NOT_RUN,
    )
    assert validate_comparison((valid,), APPROVAL_MODE_NOTE) == []


def test_comparison_rejects_incomplete_test_suggestion():
    invalid = replace(REPRESENTATIVE_RUNS[0], suggested_test="Eksik adres testi")
    errors = validate_comparison((invalid,), APPROVAL_MODE_NOTE)
    assert any("test önerisi" in error for error in errors)


def test_comparison_rejects_unknown_test_result():
    invalid = replace(REPRESENTATIVE_RUNS[0], test_result="belirsiz")
    errors = validate_comparison((invalid,), APPROVAL_MODE_NOTE)
    assert any("test sonucu" in error for error in errors)


def test_comparison_rejects_unknown_approval_behavior():
    invalid = replace(REPRESENTATIVE_RUNS[0], approval_behavior="bazen sordu")
    errors = validate_comparison((invalid,), APPROVAL_MODE_NOTE)
    assert any("onay davranışı" in error for error in errors)


def test_comparison_rejects_nonboolean_scope_result():
    invalid = replace(REPRESENTATIVE_RUNS[0], scope_met=1)
    errors = validate_comparison((invalid,), APPROVAL_MODE_NOTE)
    assert any("kapsam sonucu" in error for error in errors)


def test_comparison_requires_approval_mode_relation():
    errors = validate_comparison(
        REPRESENTATIVE_RUNS,
        "İki aracın davranışı birbirinden farklıydı.",
    )
    assert any("Onay modu notu" in error for error in errors)


def test_summary_counts_without_ranking_tools():
    summary = summarize_comparison(REPRESENTATIVE_RUNS, APPROVAL_MODE_NOTE)
    assert summary.tool_count == 2
    assert summary.suggested_test_count == 2
    assert summary.scope_met_count == 2
    assert summary.passed_test_count == 2


def test_public_approval_label_stays_stable():
    assert APPROVAL_BEFORE_CHANGE == "değişiklik öncesi onay istedi"


def test_html_has_required_blocks_links_and_balanced_tags():
    html_path = Path(__file__).with_name("cli_agent_comparison_lab.html")
    html = html_path.read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)
    parser.close()

    assert parser.stack == []
    assert "Kavram — Aynı Görev, Farklı Onay Davranışı" in html
    assert "Temsilîlik Notu" in html
    assert "get_user_city" in html
    assert html.count("https://github.com/adeministratorr/") == 3
    assert 'last_verified: "2026-07"' in html
