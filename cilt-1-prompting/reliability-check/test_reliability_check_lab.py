import pytest

from reliability_check_lab import (
    Claim,
    EvidenceTier,
    audit_claim,
    audit_claims,
    EXAMPLE_CLAIMS,
)


def test_empty_claim_text_rejected():
    with pytest.raises(ValueError):
        Claim(text="   ")


def test_verifiable_source_without_name_is_error():
    claim = Claim(
        text="Şirketin geliri geçen yıl arttı",
        evidence_tier=EvidenceTier.VERIFIABLE_SOURCE,
        source_name="",
    )
    audit = audit_claim(claim)
    assert audit.status == "hata"
    assert not audit.ok


def test_critical_claim_on_own_knowledge_is_warning_not_error():
    claim = Claim(
        text="Bu ilaç etkileşimi güvenlidir",
        is_critical=True,
        evidence_tier=EvidenceTier.OWN_KNOWLEDGE,
    )
    audit = audit_claim(claim)
    assert audit.status == "uyari"
    assert not audit.ok


def test_critical_claim_with_unverified_named_source_is_warning():
    claim = Claim(
        text="Yetkili bu artışın teşvik programından kaynaklandığını söyledi",
        is_critical=True,
        evidence_tier=EvidenceTier.PRIMARY_SOURCE,
        source_name="İlgili yetkilinin açıklaması",
        verified_by_user=False,
    )
    audit = audit_claim(claim)
    assert audit.status == "uyari"


def test_fully_verified_critical_claim_is_ready():
    claim = Claim(
        text="Mahkeme kararı davayı reddetti",
        is_critical=True,
        evidence_tier=EvidenceTier.PRIMARY_SOURCE,
        source_name="Mahkeme kararının kendisi",
        verified_by_user=True,
    )
    audit = audit_claim(claim)
    assert audit.status == "hazir"
    assert audit.ok


def test_non_critical_general_knowledge_is_ready():
    claim = Claim(
        text="Su deniz seviyesinde 100 santigrat derecede kaynar",
        is_critical=False,
        evidence_tier=EvidenceTier.GENERAL_KNOWLEDGE,
    )
    audit = audit_claim(claim)
    assert audit.status == "hazir"


def test_audit_claims_requires_at_least_one_claim():
    with pytest.raises(ValueError):
        audit_claims([])


def test_report_summary_counts_errors_and_warnings():
    report = audit_claims(EXAMPLE_CLAIMS)
    assert len(report.audits) == 4
    assert report.warning_count == 2
    assert report.error_count == 0
    assert not report.ready_to_publish
    assert "Uyarı: 2" in report.summary()


def test_evidence_tier_rank_order_is_ascending_strength():
    weak = Claim(text="A", evidence_tier=EvidenceTier.OWN_KNOWLEDGE)
    strong = Claim(
        text="B",
        evidence_tier=EvidenceTier.PRIMARY_SOURCE,
        source_name="Kaynak",
        is_critical=True,
        verified_by_user=True,
    )
    weak_audit = audit_claim(weak)
    strong_audit = audit_claim(strong)
    assert weak_audit.status in ("hazir", "uyari")
    assert strong_audit.status == "hazir"
