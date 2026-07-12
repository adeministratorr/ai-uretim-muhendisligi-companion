from datetime import date

import pytest

from competency_matrix import (
    BASE_DIR,
    evaluate_team,
    level_rank,
    load_json,
    validate_library,
    validate_library_entry,
)


def _report(reports, area):
    return next(r for r in reports if r.area == area)


def test_level_rank_orders_levels_low_to_high():
    assert level_rank("farkındalık") < level_rank("temel_kullanım")
    assert level_rank("temel_kullanım") < level_rank("eleştirel_değerlendirme")
    assert level_rank("eleştirel_değerlendirme") < level_rank("sistematik_entegrasyon")


def test_level_rank_rejects_unknown_level():
    with pytest.raises(ValueError):
        level_rank("uzman")


def test_example_team_flags_missing_developer_skill_as_gap():
    team = load_json(BASE_DIR / "example_team.json")
    reports = evaluate_team(team)

    gap = _report(reports, "arac_secimi_ve_entegrasyon")
    assert gap.durum == "boşluk"
    assert gap.en_yuksek_seviye is None
    assert gap.yeterli_kisiler == ()


def test_example_team_flags_single_point_of_failure():
    team = load_json(BASE_DIR / "example_team.json")
    reports = evaluate_team(team)

    risk = _report(reports, "ders_materyali_hazirlama")
    assert risk.durum == "tek_nokta_riski"
    assert risk.yeterli_kisiler == ("Elif Turan",)


def test_example_team_area_with_two_qualified_members_is_sufficient():
    team = load_json(BASE_DIR / "example_team.json")
    reports = evaluate_team(team)

    sufficient = _report(reports, "rapor_ve_yazisma")
    assert sufficient.durum == "yeterli"
    assert len(sufficient.yeterli_kisiler) == 2


def test_empty_team_reports_every_area_as_gap():
    reports = evaluate_team([])
    assert all(report.is_gap for report in reports)


def test_valid_library_entry_passes():
    entry = {
        "baslik": "Örnek Kayıt",
        "sahip": "Elif Turan",
        "kullanim_alani": "Öğretmen - ders planı",
        "son_dogrulama_tarihi": "2026-03-15",
    }
    check = validate_library_entry(entry, reference_date=date(2026, 7, 1))
    assert check.passed


def test_missing_required_field_is_flagged():
    entry = {
        "baslik": "Örnek Kayıt",
        "sahip": "",
        "kullanim_alani": "Analist - dönem başarı eğilimi",
        "son_dogrulama_tarihi": "2026-05-01",
    }
    check = validate_library_entry(entry, reference_date=date(2026, 7, 1))
    assert not check.passed
    assert any("`sahip`" in issue for issue in check.issues)


def test_stale_date_is_flagged():
    entry = {
        "baslik": "Eski Kayıt",
        "sahip": "Barış Yıldız",
        "kullanim_alani": "Operasyon - veli bilgilendirme",
        "son_dogrulama_tarihi": "2024-01-10",
    }
    check = validate_library_entry(entry, reference_date=date(2026, 7, 1))
    assert not check.passed
    assert any("eski" in issue for issue in check.issues)


def test_invalid_date_format_is_flagged():
    entry = {
        "baslik": "Bozuk Tarihli Kayıt",
        "sahip": "Mert Şahin",
        "kullanim_alani": "Yönetici - rapor hazırlama",
        "son_dogrulama_tarihi": "31/07/2025",
    }
    check = validate_library_entry(entry, reference_date=date(2026, 7, 1))
    assert not check.passed
    assert any("geçerli bir tarih" in issue for issue in check.issues)


def test_example_library_mix_matches_expected_pass_fail_counts():
    library = load_json(BASE_DIR / "example_library.json")
    checks = validate_library(library, reference_date=date(2026, 7, 1))

    assert len(checks) == 4
    assert sum(1 for check in checks if check.passed) == 1
    assert sum(1 for check in checks if not check.passed) == 3
