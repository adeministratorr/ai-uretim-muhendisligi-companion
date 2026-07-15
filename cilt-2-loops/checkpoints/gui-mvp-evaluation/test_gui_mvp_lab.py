"""GUI araçla MVP deneyi kaydının temel kabul ve ret durumları."""

from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path

import pytest

from gui_mvp_lab import (
    REPRESENTATIVE_EXPERIMENT,
    summarize_experiment,
    validate_experiment,
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


def test_representative_experiment_meets_acceptance_criteria():
    assert validate_experiment(REPRESENTATIVE_EXPERIMENT) == []


@pytest.mark.parametrize(
    ("idea_sentences", "expected"),
    [
        (
            REPRESENTATIVE_EXPERIMENT.idea_sentences[:2],
            "MVP fikri 3 veya 4 cümleyle tarif edilmelidir.",
        ),
        (
            (*REPRESENTATIVE_EXPERIMENT.idea_sentences, "Beşinci cümle."),
            "MVP fikri 3 veya 4 cümleyle tarif edilmelidir.",
        ),
        (
            ("Eksik noktalı cümle", *REPRESENTATIVE_EXPERIMENT.idea_sentences[1:]),
            "MVP tarifindeki her satır tek ve tamamlanmış bir cümle olmalıdır.",
        ),
    ],
)
def test_experiment_rejects_invalid_idea_description(idea_sentences, expected):
    invalid = replace(REPRESENTATIVE_EXPERIMENT, idea_sentences=idea_sentences)
    assert expected in validate_experiment(invalid)


def test_experiment_accepts_early_finish_when_quota_is_reached():
    quota_stop = replace(REPRESENTATIVE_EXPERIMENT, elapsed_minutes=18, quota_reached=True)
    assert validate_experiment(quota_stop) == []
    assert summarize_experiment(quota_stop).ended_by_quota is True


def test_experiment_rejects_early_finish_without_quota():
    invalid = replace(REPRESENTATIVE_EXPERIMENT, elapsed_minutes=18)
    errors = validate_experiment(invalid)
    assert "45 dakikadan önce biten deneyde kota sınırı işaretlenmelidir." in errors


@pytest.mark.parametrize("elapsed_minutes", [0, 46, 12.5])
def test_experiment_rejects_invalid_duration(elapsed_minutes):
    invalid = replace(REPRESENTATIVE_EXPERIMENT, elapsed_minutes=elapsed_minutes)
    assert any("süre" in error for error in validate_experiment(invalid))


@pytest.mark.parametrize(
    ("field_name", "value", "expected_fragment"),
    [
        ("automatic_steps", (), "otomatik tamamlanan adım"),
        ("intervention_points", (), "müdahale noktası"),
    ],
)
def test_experiment_rejects_missing_observation_lists(
    field_name, value, expected_fragment
):
    invalid = replace(REPRESENTATIVE_EXPERIMENT, **{field_name: value})
    assert any(expected_fragment in error for error in validate_experiment(invalid))


def test_experiment_rejects_observation_in_both_lists():
    duplicated = REPRESENTATIVE_EXPERIMENT.automatic_steps[0]
    invalid = replace(REPRESENTATIVE_EXPERIMENT, intervention_points=(duplicated,))
    errors = validate_experiment(invalid)
    assert "Aynı gözlem hem otomatik adım hem müdahale noktası olamaz." in errors


def test_experiment_rejects_unknown_change_result():
    invalid = replace(REPRESENTATIVE_EXPERIMENT, change_result="belli değil")
    assert any("değişiklik sonucu" in error for error in validate_experiment(invalid))


@pytest.mark.parametrize(
    ("field_name", "value", "expected_fragment"),
    [
        ("change_request", "Eksik noktalama", "değişiklik isteği"),
        ("review_note", "", "inceleme notu"),
        ("attention_point", "İki cümle. Olmamalı.", "Dikkat noktası"),
    ],
)
def test_experiment_rejects_incomplete_sentence_fields(
    field_name, value, expected_fragment
):
    invalid = replace(REPRESENTATIVE_EXPERIMENT, **{field_name: value})
    assert any(expected_fragment in error for error in validate_experiment(invalid))


def test_summary_counts_observations_without_combining_them_into_a_score():
    summary = summarize_experiment(REPRESENTATIVE_EXPERIMENT)
    assert summary.automatic_step_count == 2
    assert summary.intervention_point_count == 1
    assert summary.ended_by_quota is False


def test_html_has_required_blocks_links_and_balanced_tags():
    html = Path(__file__).with_name("gui_mvp_lab.html").read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)
    parser.close()

    assert parser.stack == []
    assert "Kavram — Zaman Kutusu ve Müdahale Kaydı" in html
    assert "Temsilîlik Notu" in html
    assert html.count("https://github.com/adeministratorr/") == 3
    assert 'last_verified: "2026-07"' in html
