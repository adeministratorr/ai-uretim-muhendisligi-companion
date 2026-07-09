from model_selection_lab import TaskProfile, decide


def test_sensitive_data_vetoes_general_chat_interface():
    decision = decide(
        TaskProfile(
            name="Gizli musteri verisi",
            task_type="summarization",
            sensitive_data=True,
            commercial_use=True,
        )
    )

    assert decision.deployment == "yerel_oncelikli"
    assert "ucretsiz_genel_sohbet_arayuzu" in decision.vetoes
    assert "veri_saklama_log_telemetri_kontrolu" in decision.checks


def test_multi_step_analysis_uses_reasoning_mode():
    decision = decide(
        TaskProfile(
            name="Tedarikci risk analizi",
            task_type="multi_step_analysis",
        )
    )

    assert decision.mode == "akil_yurutme"


def test_simple_classification_stays_standard_for_latency():
    decision = decide(
        TaskProfile(
            name="E-posta kategorileme",
            task_type="classification",
            latency_sensitive=True,
            budget_sensitive=True,
        )
    )

    assert decision.mode == "standart"
    assert "gecikme_olcumu" in decision.checks
    assert "hacim_ve_birim_maliyet_kontrolu" in decision.checks


def test_web_search_and_rag_are_separate_tooling_needs():
    decision = decide(
        TaskProfile(
            name="Guncel haber ve ic prosedur cevabi",
            task_type="simple_generation",
            needs_current_info=True,
            needs_internal_sources=True,
            needs_citations=True,
        )
    )

    assert "web_aramasi" in decision.required_tooling
    assert "rag_belge_arama" in decision.required_tooling
    assert "kaynak_gosterebilen_arac" in decision.required_tooling


def test_action_requires_agentic_tool_and_human_review():
    decision = decide(
        TaskProfile(
            name="Kod dosyasinda degisiklik",
            task_type="coding_change",
            needs_action=True,
        )
    )

    assert decision.layer == "arac"
    assert "ajan_tabanli_arac_diff_ve_test_onayi" in decision.required_tooling
    assert "insan_diff_review_ve_test" in decision.checks
