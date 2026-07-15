"""Model çıktısı karşılaştırıcısının temel kabul ve ret durumları."""

from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path

import pytest

from model_comparison_lab import (
    DECISION_NOTE,
    REPRESENTATIVE_RUNS,
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
    assert validate_comparison(REPRESENTATIVE_RUNS, DECISION_NOTE) == []


@pytest.mark.parametrize("runs", [REPRESENTATIVE_RUNS[:1], REPRESENTATIVE_RUNS * 2])
def test_comparison_rejects_run_count_outside_range(runs):
    errors = validate_comparison(runs, DECISION_NOTE)
    assert "Karşılaştırma 2-3 deneme içermelidir." in errors


def test_comparison_rejects_duplicate_run_labels():
    duplicate = replace(REPRESENTATIVE_RUNS[1], run_label="deneme a")
    errors = validate_comparison((REPRESENTATIVE_RUNS[0], duplicate), DECISION_NOTE)
    assert any("yineleniyor" in error for error in errors)


def test_comparison_rejects_empty_run_label():
    invalid = replace(REPRESENTATIVE_RUNS[0], run_label="  ")
    errors = validate_comparison((invalid, REPRESENTATIVE_RUNS[1]), DECISION_NOTE)
    assert "1. deneme etiketi boş bırakılamaz." in errors


@pytest.mark.parametrize(
    "proposed_diff",
    [
        "+ return labels",
        "def normalize_labels(labels):\n    return labels",
    ],
)
def test_comparison_rejects_diff_without_target_and_addition(proposed_diff):
    invalid = replace(REPRESENTATIVE_RUNS[0], proposed_diff=proposed_diff)
    errors = validate_comparison((invalid, REPRESENTATIVE_RUNS[1]), DECISION_NOTE)
    assert any("normalize_labels" in error and "ekleme" in error for error in errors)


def test_comparison_rejects_unknown_test_result():
    invalid = replace(REPRESENTATIVE_RUNS[0], test_result="belirsiz")
    errors = validate_comparison((invalid, REPRESENTATIVE_RUNS[1]), DECISION_NOTE)
    assert any("test sonucu" in error for error in errors)


@pytest.mark.parametrize("changed_file_count", [0, 21, True])
def test_comparison_rejects_invalid_changed_file_count(changed_file_count):
    invalid = replace(REPRESENTATIVE_RUNS[0], changed_file_count=changed_file_count)
    errors = validate_comparison((invalid, REPRESENTATIVE_RUNS[1]), DECISION_NOTE)
    assert any("değişen dosya sayısı" in error for error in errors)


@pytest.mark.parametrize("field", ["interface_preserved", "context_fit"])
def test_comparison_rejects_nonboolean_results(field):
    invalid = replace(REPRESENTATIVE_RUNS[0], **{field: 1})
    errors = validate_comparison((invalid, REPRESENTATIVE_RUNS[1]), DECISION_NOTE)
    assert any("evet/hayır" in error for error in errors)


@pytest.mark.parametrize("readability_score", [0, 6, True])
def test_comparison_rejects_invalid_readability_score(readability_score):
    invalid = replace(REPRESENTATIVE_RUNS[0], readability_score=readability_score)
    errors = validate_comparison((invalid, REPRESENTATIVE_RUNS[1]), DECISION_NOTE)
    assert any("okunabilirlik puanı" in error for error in errors)


@pytest.mark.parametrize("call_count", [0, 101, True])
def test_comparison_rejects_invalid_call_count(call_count):
    invalid = replace(REPRESENTATIVE_RUNS[0], call_count=call_count)
    errors = validate_comparison((invalid, REPRESENTATIVE_RUNS[1]), DECISION_NOTE)
    assert any("çağrı sayısı" in error for error in errors)


@pytest.mark.parametrize("field", ["readability_note", "observation"])
def test_comparison_rejects_incomplete_explanation(field):
    invalid = replace(REPRESENTATIVE_RUNS[0], **{field: "Kısa bir not"})
    errors = validate_comparison((invalid, REPRESENTATIVE_RUNS[1]), DECISION_NOTE)
    assert any("tamamlanmış bir cümle" in error for error in errors)


@pytest.mark.parametrize("missing_term", ["test", "arayüz", "okunabilir", "çağrı", "bağlam"])
def test_decision_note_requires_all_observation_terms(missing_term):
    invalid_note = DECISION_NOTE.replace(missing_term, "ölçüt", 1)
    errors = validate_comparison(REPRESENTATIVE_RUNS, invalid_note)
    assert any("Karar notu" in error for error in errors)


def test_decision_note_requires_selected_run_label():
    invalid_note = DECISION_NOTE.replace("Deneme B", "İkinci çıktı")
    errors = validate_comparison(REPRESENTATIVE_RUNS, invalid_note)
    assert "Karar notu tercih edilen deneme etiketini belirtmelidir." in errors


def test_summary_counts_without_ranking_runs():
    summary = summarize_comparison(REPRESENTATIVE_RUNS, DECISION_NOTE)
    assert summary.run_count == 2
    assert summary.passed_test_count == 2
    assert summary.interface_preserved_count == 2
    assert summary.context_fit_count == 2


def test_html_has_required_blocks_links_and_balanced_tags():
    html_path = Path(__file__).with_name("model_comparison_lab.html")
    html = html_path.read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)
    parser.close()

    assert parser.stack == []
    assert "Kavram — Aynı Görev, Ortak Ölçüt" in html
    assert "Temsilîlik Notu" in html
    assert "normalize_labels" in html
    assert html.count("https://github.com/adeministratorr/") == 3
    assert 'last_verified: "2026-07"' in html
