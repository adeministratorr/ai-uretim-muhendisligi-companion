import pytest

from prompt_anatomy_lab import (
    audit_recipe,
    example_values,
    find_unresolved_variables,
    good_recipe,
    is_checkable_criterion,
    render_recipe,
    rival_comparison_recipe,
    weak_recipe,
)


def test_weak_recipe_is_zayif_and_missing_core_parts():
    audit = audit_recipe(weak_recipe())

    assert audit.level == "zayıf"
    assert "persona" in audit.missing_parts
    assert "context" in audit.missing_parts
    assert "acceptance_criteria" in audit.missing_parts


def test_good_recipe_is_not_professional_without_context_and_constraints():
    audit = audit_recipe(good_recipe())

    assert audit.level == "iyi"
    assert "task" in audit.present_parts
    assert "output_format" in audit.present_parts
    assert "constraints" in audit.missing_parts


def test_professional_recipe_has_all_required_parts():
    audit = audit_recipe(rival_comparison_recipe())

    assert audit.level == "profesyonel"
    assert audit.missing_parts == ()
    assert audit.acceptance_ready is True


def test_render_recipe_rejects_missing_variable():
    values = example_values()
    values.pop("veri_kaynağı")

    with pytest.raises(ValueError, match="veri_kaynağı"):
        render_recipe(rival_comparison_recipe(), values)


def test_render_recipe_fills_all_variables():
    rendered = render_recipe(rival_comparison_recipe(), example_values())

    assert find_unresolved_variables(rendered) == ()
    assert "Şirketimiz" in rendered
    assert "veri mevcut değil" in rendered


def test_checkable_criterion_rejects_vague_goal():
    assert is_checkable_criterion("Her satırda en az bir kaynaklı veri bulunmalı.")
    assert not is_checkable_criterion("Çıktı iyi ve etkileyici olsun.")
