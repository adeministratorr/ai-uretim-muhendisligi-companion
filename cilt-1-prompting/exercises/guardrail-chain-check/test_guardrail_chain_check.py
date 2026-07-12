from guardrail_chain_check import (
    BASE_DIR,
    GuardrailLayer,
    RiskLevel,
    ToolDefinition,
    audit_tool_chain,
    format_report,
    load_tool_chain,
)


def test_incident_chain_flags_missing_human_approval_on_critical_tool():
    tools = load_tool_chain(BASE_DIR / "example_incident.json")
    report = audit_tool_chain(tools)

    assert not report.is_compliant
    assert len(report.critical_gaps) == 1
    assert report.critical_gaps[0].tool_name == "Yetki yükseltme / yönetici erişimi verme"
    assert GuardrailLayer.INSAN_ONAYI in report.critical_gaps[0].missing_layers


def test_fixed_chain_is_fully_compliant():
    tools = load_tool_chain(BASE_DIR / "example_fixed.json")
    report = audit_tool_chain(tools)

    assert report.is_compliant
    assert report.compliant_count == len(report.results)
    assert not report.critical_gaps


def test_low_risk_tool_requires_only_input_review():
    tool = ToolDefinition(
        name="Bilgi bankasında arama",
        risk_level=RiskLevel.DUSUK,
        configured_layers=frozenset({GuardrailLayer.GIRDI_DENETIMI}),
    )
    report = audit_tool_chain([tool])

    assert report.is_compliant


def test_medium_risk_tool_missing_output_validation_is_flagged_but_not_critical():
    tool = ToolDefinition(
        name="Destek kaydı oluşturma/güncelleme",
        risk_level=RiskLevel.ORTA,
        configured_layers=frozenset({GuardrailLayer.GIRDI_DENETIMI}),
    )
    report = audit_tool_chain([tool])

    assert not report.is_compliant
    assert not report.critical_gaps
    assert GuardrailLayer.CIKTI_DOGRULAMA in report.results[0].missing_layers


def test_critical_tool_with_all_layers_has_no_missing_layers():
    tool = ToolDefinition(
        name="Yetki yükseltme / yönetici erişimi verme",
        risk_level=RiskLevel.KRITIK,
        configured_layers=frozenset(
            {GuardrailLayer.GIRDI_DENETIMI, GuardrailLayer.CIKTI_DOGRULAMA, GuardrailLayer.INSAN_ONAYI}
        ),
    )
    report = audit_tool_chain([tool])

    assert report.is_compliant
    assert report.results[0].is_critical_gap is False


def test_format_report_marks_critical_gap_as_high_priority():
    tools = load_tool_chain(BASE_DIR / "example_incident.json")
    report = audit_tool_chain(tools)
    text = format_report(report)

    assert "[YÜKSEK ÖNCELİKLİ]" in text
    assert "insan onayı" in text
