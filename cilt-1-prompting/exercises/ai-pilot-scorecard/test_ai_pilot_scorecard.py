from ai_pilot_scorecard import (
    BASE_DIR,
    evaluate_pilot,
    load_json,
    summarize_cases,
)


def test_example_pilot_passes():
    pilot = load_json(BASE_DIR / "example_pilot.json")
    scorecard = evaluate_pilot(pilot)
    assert scorecard.passed
    assert scorecard.completed_checks == scorecard.total_checks


def test_empty_template_is_not_accepted_as_finished_pilot():
    pilot = load_json(BASE_DIR / "pilot_template.json")
    scorecard = evaluate_pilot(pilot)
    assert not scorecard.passed
    assert any("`hedef`" in issue for issue in scorecard.issues)
    assert any("zaman_kazanci" in issue for issue in scorecard.issues)


def test_sensitive_data_requires_control():
    pilot = load_json(BASE_DIR / "example_pilot.json")
    pilot["veri_riski"] = "Bu pilot müşteri kişisel verisi ve banka bilgisi kullanır."

    scorecard = evaluate_pilot(pilot)

    assert not scorecard.passed
    assert any("hassas veri" in issue for issue in scorecard.issues)


def test_decision_criteria_requires_retreat_path():
    pilot = load_json(BASE_DIR / "example_pilot.json")
    pilot["pilot_sonrasi_karar_kriteri"] = "Sonuçlar iyileşirse devam ederiz."

    scorecard = evaluate_pilot(pilot)

    assert not scorecard.passed
    assert any("en az iki karar yolu" in issue for issue in scorecard.issues)


def test_case_table_keeps_verification_status_visible():
    cases = load_json(BASE_DIR / "case_table.json")

    assert len(cases) == 10
    assert all(case["dogrulama_durumu"] == "beklemede" for case in cases)
    assert summarize_cases(cases) == "Vaka satırı: 10 | Kaynak doğrulaması bekleyen: 10"
