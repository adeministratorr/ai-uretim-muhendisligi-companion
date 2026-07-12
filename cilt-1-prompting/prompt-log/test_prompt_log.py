import pytest

from prompt_log import (
    DEFAULT_LOG,
    PromptVersionEntry,
    detect_score_regressions,
    detect_test_regressions,
    format_log_table,
    format_regression_report,
    validate_entry,
    validate_log,
)


def test_no_test_regression_across_ab_c():
    # 7.9'daki A -> B -> C geçişinde her sürüm bir öncekinde geçen testleri korur
    # (B, C'ye göre yalnızca dosya_15_zor'da geride kalır; ama bu A->B veya B->C
    # arasında bir *gerileme* değil, C'nin B'ye göre bir iyileşmesidir).
    stable = DEFAULT_LOG[:3]
    assert detect_test_regressions(stable) == ()


def test_detects_known_regression_from_v1_1_to_v2():
    regressions = detect_test_regressions(DEFAULT_LOG)
    ids = {(r.test_id, r.from_version, r.to_version) for r in regressions}
    assert ("dosya_15_zor", "v1.1", "v2") in ids
    # Bu tek dosyanın dışında beklenmedik başka bir gerileme olmamalı.
    assert len(regressions) == 1


def test_score_regression_respects_metric_specific_tolerance():
    regressions = detect_score_regressions(DEFAULT_LOG)
    dropped_metrics = {r.metric for r in regressions if r.to_version == "v2"}
    assert dropped_metrics == {"D", "E", "B"}
    # B sürümünden C sürümüne 98 -> 97 düşüşü (7.9'daki gürültü payı örneği)
    # 1.0 puanlık tolerans içinde kaldığı için gerileme sayılmamalı.
    b_to_c = [r for r in regressions if r.from_version == "B" and r.to_version == "C"]
    assert b_to_c == []


def test_score_regression_uses_smaller_tolerance_for_usability_metric():
    previous = PromptVersionEntry(
        version="x1",
        date="2026-01-01",
        change_summary="test",
        change_reason="test",
        test_set="test-30",
        model_version="m1",
        test_results={"dosya_01": True},
        scores={"K": 2.6},
        decision="Kabul edildi",
    )
    # K metriğinde 0,1 puanlık düşüş (0,15 toleransın altında) gerileme sayılmamalı.
    small_drop = PromptVersionEntry(
        version="x2",
        date="2026-01-02",
        change_summary="test",
        change_reason="test",
        test_set="test-30",
        model_version="m1",
        test_results={"dosya_01": True},
        scores={"K": 2.5},
        decision="Kabul edildi",
    )
    assert detect_score_regressions((previous, small_drop)) == ()

    # 0,3 puanlık düşüş toleransı aşar ve gerileme olarak işaretlenmeli.
    large_drop = PromptVersionEntry(
        version="x3",
        date="2026-01-02",
        change_summary="test",
        change_reason="test",
        test_set="test-30",
        model_version="m1",
        test_results={"dosya_01": True},
        scores={"K": 2.3},
        decision="Kabul edildi",
    )
    regressions = detect_score_regressions((previous, large_drop))
    assert len(regressions) == 1
    assert regressions[0].metric == "K"


def test_format_log_table_lists_every_version_and_uses_comma_decimal():
    table = format_log_table(DEFAULT_LOG)
    for entry in DEFAULT_LOG:
        assert entry.version in table
    assert "1,8" in table  # A sürümünün K puanı, Türkçe ondalık ayraçla


def test_format_regression_report_mentions_failing_test_id():
    test_regressions = detect_test_regressions(DEFAULT_LOG)
    score_regressions = detect_score_regressions(DEFAULT_LOG)
    report = format_regression_report(test_regressions, score_regressions)
    assert "dosya_15_zor" in report
    assert "TEST GERİLEMESİ" in report


def test_format_regression_report_empty_when_no_regressions():
    stable = DEFAULT_LOG[:3]
    report = format_regression_report(detect_test_regressions(stable), detect_score_regressions(stable))
    assert "tespit edilmedi" in report


def test_validate_entry_flags_missing_fields():
    broken = PromptVersionEntry(
        version="v3",
        date="2026-07-05",
        change_summary="",
        change_reason="test",
        test_set="test-30",
        model_version="m1",
        test_results={},
        scores={"Z": 10},
        decision="",
    )
    errors = validate_entry(broken)
    assert any("değişiklik özeti" in e for e in errors)
    assert any("test sonucu" in e for e in errors)
    assert any("Z" in e for e in errors)
    assert any("Karar" in e or "karar" in e for e in errors)


def test_validate_log_flags_duplicate_version_names():
    duplicated = DEFAULT_LOG[:2] + (DEFAULT_LOG[0],)
    errors = validate_log(duplicated)
    assert any("tekrar ediyor" in e for e in errors)


def test_default_log_is_internally_valid():
    assert validate_log(DEFAULT_LOG) == []
