import pytest

from ticket_classification_lab import (
    build_few_shot_prompt,
    build_zero_shot_prompt,
    classify_ticket_locally,
    parse_json_object,
    validate_ticket_output,
)


def test_zero_shot_prompt_does_not_include_examples():
    prompt = build_zero_shot_prompt("Kargom gelmedi.")

    assert "Örnek" not in prompt
    assert "kategori ve aciliyete göre" in prompt


def test_few_shot_prompt_contains_examples_counter_examples_and_schema():
    prompt = build_few_shot_prompt("Kargom gelmedi.")

    assert prompt.count("Etiket: Kategori") == 7
    assert "Karşı örnek 1" in prompt
    assert "Çıktı yalnızca tek satırlık JSON nesnesi olsun" in prompt
    assert "baskın konuyu esas al" in prompt


def test_local_classifier_handles_contrast_pair():
    payment_status = classify_ticket_locally("Param ne zaman iade edilecek?")
    new_return = classify_ticket_locally(
        "Ürünü iade etmek istiyorum, süreç nasıl işliyor?"
    )

    assert payment_status["kategori"] == "Fatura"
    assert new_return["kategori"] == "İade"


def test_mixed_ticket_output_matches_schema():
    payload = classify_ticket_locally(
        "Kargom gelmedi, ayrıca yanlış ürün gönderilmiş, "
        "hem iade hem yeni gönderim istiyorum."
    )

    assert payload["kategori"] == "İade"
    assert payload["aciliyet"] == "Normal"
    assert validate_ticket_output(payload) == []


def test_parse_json_object_rejects_explanatory_text():
    with pytest.raises(ValueError, match="JSON nesnesi"):
        parse_json_object('Açıklama: {"kategori": "İade"}')


def test_schema_validation_rejects_unknown_category_and_apology_opening():
    errors = validate_ticket_output(
        {
            "kategori": "Kargo",
            "aciliyet": "Normal",
            "ozet": "Kargo gecikmesi bildirildi.",
            "onerilen_ilk_cumle": "Üzgünüz, talebinizi inceliyoruz.",
        }
    )

    assert "kategori alanı izin verilen değerlerden biri olmalıdır." in errors
    assert "onerilen_ilk_cumle özür kalıbı içermemelidir." in errors
