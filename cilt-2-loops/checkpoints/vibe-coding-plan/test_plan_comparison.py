"""Plan karşılaştırma doğrulayıcısının temel kabul ve ret durumları."""

from dataclasses import replace

import pytest

from plan_comparison import (
    HUMAN_APPROVAL,
    MISE_EN_PLACE,
    TRADITIONAL_PLAN,
    VERIFICATION,
    VIBE_CODING_PLAN,
    summarize_comparison,
    validate_comparison,
    validate_plan,
)


def test_representative_plans_meet_acceptance_criteria():
    assert validate_comparison(TRADITIONAL_PLAN, VIBE_CODING_PLAN) == []


def test_plan_rejects_fewer_than_five_steps():
    errors = validate_plan("Geleneksel", TRADITIONAL_PLAN[:4])
    assert "Geleneksel planı 5-8 adım içermelidir." in errors


def test_plan_rejects_an_empty_step():
    incomplete = (replace(TRADITIONAL_PLAN[0], description=""),) + TRADITIONAL_PLAN[1:]
    errors = validate_plan("Geleneksel", incomplete)
    assert "Geleneksel planının 1. adımı boş bırakılamaz." in errors


def test_plan_rejects_a_nonpositive_time_estimate():
    invalid = (replace(TRADITIONAL_PLAN[0], minutes=0),) + TRADITIONAL_PLAN[1:]
    errors = validate_plan("Geleneksel", invalid)
    assert any("süre 0'dan büyük olmalıdır" in error for error in errors)


def test_plan_rejects_an_unknown_uncertainty_level():
    invalid = (replace(TRADITIONAL_PLAN[0], uncertainty=4),) + TRADITIONAL_PLAN[1:]
    errors = validate_plan("Geleneksel", invalid)
    assert any("belirsizlik 1, 2 veya 3 olmalıdır" in error for error in errors)


@pytest.mark.parametrize(
    ("marker", "label"),
    [
        (MISE_EN_PLACE, "mise en place"),
        (VERIFICATION, "doğrulama"),
        (HUMAN_APPROVAL, "insan onayı"),
    ],
)
def test_vibe_plan_rejects_a_missing_required_marker(marker, label):
    incomplete = tuple(
        replace(step, markers=step.markers - {marker}) for step in VIBE_CODING_PLAN
    )
    errors = validate_comparison(TRADITIONAL_PLAN, incomplete)
    assert f"Vibe coding planında en az bir {label} adımı olmalıdır." in errors


def test_summary_reports_time_uncertainty_and_marker_counts():
    summary = summarize_comparison(TRADITIONAL_PLAN, VIBE_CODING_PLAN)
    assert summary.traditional_minutes == 95
    assert summary.vibe_minutes == 50
    assert summary.traditional_uncertainty == 2.0
    assert summary.vibe_uncertainty == 1.6
    assert summary.marker_counts == {
        MISE_EN_PLACE: 1,
        VERIFICATION: 1,
        HUMAN_APPROVAL: 1,
    }
