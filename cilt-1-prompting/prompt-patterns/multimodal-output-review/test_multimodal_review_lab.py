from multimodal_review_lab import (
    MultimodalReviewTask,
    audit_response,
    extract_sections,
    render_review_prompt,
    reviewable_response,
    weak_response,
)


def test_render_prompt_requires_four_sections_without_reference():
    prompt = render_review_prompt(
        MultimodalReviewTask(
            source_kind="ekran görüntüsü",
            question="Hata mesajını değerlendir.",
            context="MES ekranı.",
        )
    )

    assert "## Betimleme" in prompt
    assert "## Yorum" in prompt
    assert "## Varsayım Listesi" in prompt
    assert "## Gizlilik ve Telif Kontrolü" in prompt
    assert "olası neden uydurma" in prompt


def test_render_prompt_uses_reference_when_present():
    prompt = render_review_prompt(
        MultimodalReviewTask(
            source_kind="PDF kesiti",
            question="Parti numarasını bul.",
            context="Tedarikçi sertifikası.",
            reference_document="Ekli sertifikanın tablo bölümü",
        )
    )

    assert "Ekli sertifikanın tablo bölümü" in prompt
    assert "olası neden uydurma" not in prompt


def test_extract_sections_finds_required_headings():
    sections = extract_sections(reviewable_response())

    assert set(sections) == {"description", "interpretation", "assumptions", "privacy"}
    assert "E-204" in sections["description"]


def test_weak_response_is_not_ready():
    audit = audit_response(weak_response())

    assert audit.ready is False
    assert "assumptions" in audit.missing_sections
    assert "privacy" in audit.missing_sections
    assert audit.description_clean is False
    assert audit.reference_guard_ready is False


def test_reviewable_response_passes_without_reference():
    audit = audit_response(reviewable_response())

    assert audit.ready is True
    assert audit.missing_sections == ()
    assert audit.assumption_count == 3
    assert audit.assumptions_with_verification == 3


def test_reference_provided_allows_grounded_interpretation_without_guard_phrase():
    response = """## Betimleme
Tabloda parti numarası P-42 ve çekme mukavemeti 510 MPa olarak yazıyor.

## Yorum
Ekli sertifika tablosuna göre P-42 satırındaki değer 510 MPa olarak okunuyor.

## Varsayım Listesi
- Satırın P-42 partisine ait olduğunu varsaydım; ham veri tablosundan doğrula.
- Birimin MPa olduğunu varsaydım; sertifika başlığını kontrol et.

## Gizlilik ve Telif Kontrolü
Tedarikçi çizimi veya kişi bilgisi yoksa risk yok notu yazılabilir.
"""

    audit = audit_response(response, reference_provided=True)

    assert audit.ready is True
    assert audit.reference_guard_ready is True
