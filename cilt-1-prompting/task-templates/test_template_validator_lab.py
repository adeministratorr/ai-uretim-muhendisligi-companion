from template_validator_lab import (
    ANALIST_EKSIK_DOLU,
    ANALIST_TAM_DOLU,
    ANALIST_TEMPLATE,
    GELISTIRICI_TAM_DOLU,
    OGRETMEN_EKSIK_DOLU,
    OGRETMEN_TAM_DOLU,
    OGRETMEN_TEMPLATE,
    find_variables,
    parse_fields,
    validate_template,
)


def test_find_variables_detects_all_brackets_in_order():
    text = "Amaç: [konu] için [sınıf seviyesi] metni indirge."
    assert find_variables(text) == ("konu", "sınıf seviyesi")


def test_parse_fields_splits_five_required_fields():
    fields = parse_fields(OGRETMEN_TEMPLATE.template)
    assert set(fields) == {"Amaç", "Hedef Kitle", "Kaynak", "Format", "Sınır"}
    assert fields["Kaynak"] == "yalnızca [orijinal_metin]"


def test_raw_ek_c_template_is_never_ready():
    # Ek C'deki ham şablon (hiç doldurulmamış) her zaman "hazır değil" olmalı;
    # beş alanın hepsi köşeli parantezli değişken içeriyor.
    report = validate_template(OGRETMEN_TEMPLATE.template, template_name="Öğretmen — ham")
    assert report.is_ready is False
    assert "konu" in report.unfilled_variables
    assert not report.missing_fields  # etiketlerin hepsi mevcut, yalnızca içerik boş değil


def test_ogretmen_eksik_dolu_flags_unfilled_variable_and_empty_field():
    report = validate_template(OGRETMEN_EKSIK_DOLU, template_name="Öğretmen — eksik")
    assert report.is_ready is False
    assert report.unfilled_variables == ("yaş grubu",)
    assert report.empty_fields == ("Sınır",)
    assert not report.missing_fields


def test_analist_eksik_dolu_flags_missing_field_and_unfilled_variable():
    report = validate_template(ANALIST_EKSIK_DOLU, template_name="Analist — eksik")
    assert report.is_ready is False
    assert report.missing_fields == ("Sınır",)
    assert "veri_dosyasi" in report.unfilled_variables


def test_fully_filled_templates_are_ready():
    for text, name in (
        (OGRETMEN_TAM_DOLU, "Öğretmen — tam"),
        (ANALIST_TAM_DOLU, "Analist — tam"),
        (GELISTIRICI_TAM_DOLU, "Geliştirici — tam"),
    ):
        report = validate_template(text, template_name=name)
        assert report.is_ready is True, f"{name} hazır olmalıydı: {report}"
        assert not report.missing_fields
        assert not report.empty_fields
        assert not report.unfilled_variables


def test_analist_template_uses_two_of_five_ek_c_personas_as_example_data():
    # Görev şartı: en az iki persona (Öğretmen/Analist burada kullanılıyor).
    assert OGRETMEN_TEMPLATE.persona == "Öğretmen"
    assert ANALIST_TEMPLATE.persona == "Analist"
