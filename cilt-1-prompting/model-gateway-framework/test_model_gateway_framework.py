from model_gateway_framework import OrganizationProfile, evaluate_need


def test_single_provider_does_not_need_gateway():
    assessment = evaluate_need(
        OrganizationProfile(
            name="Hukuk burosu",
            provider_count=1,
            sensitive_data_requires_local=True,
        )
    )

    assert assessment.verdict == "dogrudan_api_yeterli"
    assert assessment.signal_count == 0


def test_multiple_providers_with_no_tracking_and_manual_switching_recommends_gateway():
    assessment = evaluate_need(
        OrganizationProfile(
            name="Tekstil atolyesi",
            provider_count=2,
            has_cost_tracking=False,
            has_fallback_provider=False,
            has_central_routing=False,
            switches_provider_by_task=True,
        )
    )

    assert assessment.verdict == "gateway_onerilir"
    assert assessment.signal_count >= 3


def test_multiple_providers_with_everything_already_in_place_needs_no_gateway():
    assessment = evaluate_need(
        OrganizationProfile(
            name="Kucuk ekip",
            provider_count=2,
            has_cost_tracking=True,
            has_fallback_provider=True,
            has_central_routing=True,
            switches_provider_by_task=False,
        )
    )

    assert assessment.verdict == "dogrudan_api_yeterli"
    assert assessment.signal_count == 0


def test_partial_gaps_land_in_middle_verdict():
    assessment = evaluate_need(
        OrganizationProfile(
            name="Orta olcekli ekip",
            provider_count=2,
            has_cost_tracking=True,
            has_fallback_provider=False,
            has_central_routing=True,
            switches_provider_by_task=False,
        )
    )

    assert assessment.verdict == "gateway_degerlendirilebilir"
    assert assessment.signal_count == 1


def test_sensitive_data_adds_local_execution_caution():
    assessment = evaluate_need(
        OrganizationProfile(
            name="Deniz'in toplami",
            provider_count=3,
            sensitive_data_requires_local=True,
        )
    )

    assert any("cikarim adimi" in caution for caution in assessment.cautions)


def test_reasons_always_mention_provider_count_when_two_or_more():
    assessment = evaluate_need(
        OrganizationProfile(name="Dil kursu", provider_count=2)
    )

    assert "saglayici/model kullaniliyor" in assessment.reasons[0]
