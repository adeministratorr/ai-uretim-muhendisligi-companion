"""Sorumluluk matrisi doğrulayıcısının temel kabul ve ret durumları."""

from dataclasses import replace

from responsibility_matrix import MatrixRow, SAMPLE_ROWS, validate_matrix


def test_representative_matrix_meets_acceptance_criteria():
    assert validate_matrix(SAMPLE_ROWS) == []


def test_matrix_rejects_fewer_than_five_tasks():
    errors = validate_matrix(SAMPLE_ROWS[:4])
    assert "Matris 5-8 görev içermelidir." in errors


def test_matrix_rejects_more_than_eight_tasks():
    extra_rows = tuple(
        replace(SAMPLE_ROWS[0], task=f"Ek görev {index}") for index in range(3)
    )
    errors = validate_matrix(SAMPLE_ROWS + extra_rows)
    assert "Matris 5-8 görev içermelidir." in errors


def test_matrix_rejects_an_empty_responsibility_field():
    incomplete = (replace(SAMPLE_ROWS[0], done_together=""),) + SAMPLE_ROWS[1:]
    errors = validate_matrix(incomplete)
    assert "1. satırda 'Birlikte yürütülen' alanı boş bırakılamaz." in errors


def test_matrix_rejects_reason_that_is_not_a_sentence():
    incomplete = (replace(SAMPLE_ROWS[0], reason="Mimari risk"),) + SAMPLE_ROWS[1:]
    errors = validate_matrix(incomplete)
    assert any("en az üç kelimelik bir cümle" in error for error in errors)


def test_matrix_rejects_duplicate_tasks_case_insensitively():
    duplicate = (
        SAMPLE_ROWS[0],
        replace(SAMPLE_ROWS[1], task=SAMPLE_ROWS[0].task.upper()),
    ) + SAMPLE_ROWS[2:]
    errors = validate_matrix(duplicate)
    assert any("görevi yineleniyor" in error for error in errors)
