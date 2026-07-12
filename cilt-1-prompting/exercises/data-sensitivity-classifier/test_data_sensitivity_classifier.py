import pytest

from data_sensitivity_classifier import (
    DEMO_CASES,
    classify_data,
    format_classification,
)


def test_genel_bilgi_dogrudan_gonderilebilir():
    result = classify_data("7. sınıf fen bilgisi müfredatının bu haftaki konusu fotosentez.")

    assert result.category == "dogrudan"
    assert result.category_label == "Doğrudan gönderilebilir"
    assert result.gonderilebilir
    assert result.masking_suggestions == ()


def test_hassas_veri_hic_gonderilemez():
    result = classify_data(
        "Öğrencinin rehberlik görüşme notu: ailede boşanma süreci yaşanıyor."
    )

    assert result.category == "hic_gonderilemez"
    assert not result.gonderilebilir
    assert "rehberlik görüşme notu" in result.sensitive_matches
    assert result.masking_suggestions == ()


def test_kurum_ici_bilgi_hic_gonderilemez():
    result = classify_data(
        "Okulun bir sonraki dönem bütçe taslağı ve öğretmenlerin performans "
        "değerlendirme notları."
    )

    assert result.category == "hic_gonderilemez"
    assert "bütçe taslağı" in result.institutional_matches


def test_kisisel_veri_anonimlestirerek_ve_maskeleme_onerisi_uretir():
    result = classify_data(
        "Ayşe Yılmaz'ın bu dönem matematik notu 72; veli telefon numarası 0532 xxx xx xx."
    )

    assert result.category == "anonimlestirerek"
    assert result.masking_suggestions  # en az bir öneri üretilmeli
    assert any("telefon" in suggestion.casefold() for suggestion in result.masking_suggestions)
    assert result.reidentification_warning is None


def test_kendine_ozgu_ayrinti_yeniden_kimliklendirme_uyarisi_verir():
    result = classify_data(
        "Öğrencinin ad soyad bilgisi ve son sınav notu birlikte paylaşılacak; "
        "üstelik bu öğrenci geçen ay bölgesel bir yarışmayı kazanan tek öğrenci."
    )

    assert result.category == "anonimlestirerek"
    assert result.reidentification_warning is not None
    assert "yeniden kimliklendirme" in result.reidentification_warning


def test_hassas_ve_kurum_ici_birlikte_gorulunce_ikisi_de_raporlanir():
    result = classify_data(
        "Bir personelin disiplin dosyası ve okulun henüz yayımlanmamış sınav sorusu "
        "birlikte paylaşılacak."
    )

    assert result.category == "hic_gonderilemez"
    assert result.sensitive_matches
    assert result.institutional_matches


def test_bos_aciklama_hata_verir():
    with pytest.raises(ValueError):
        classify_data("   ")


def test_demo_cases_cover_all_three_categories():
    categories = {classify_data(case).category for case in DEMO_CASES}

    assert categories == {"dogrudan", "anonimlestirerek", "hic_gonderilemez"}


def test_format_classification_includes_karar_ve_gerekce():
    description = "7. sınıf fen bilgisi müfredatının bu haftaki konusu fotosentez."
    result = classify_data(description)

    text = format_classification(description, result)

    assert "Doğrudan gönderilebilir" in text
    assert "Gerekçe" in text
