"""Cilt 1 Bolum 2 icin model/mod/arac secimi karar laboratuvari.

Gercek model cagrisi yapmaz, fiyat veya benchmark iddiasi uretmez. Bolum 2'deki
bes soruluk karar cercevesini deterministik bir kontrol listesine cevirir.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class TaskProfile:
    name: str
    task_type: str
    needs_current_info: bool = False
    needs_internal_sources: bool = False
    needs_citations: bool = False
    needs_action: bool = False
    sensitive_data: bool = False
    commercial_use: bool = False
    latency_sensitive: bool = False
    budget_sensitive: bool = False
    turkish_quality_required: bool = True


@dataclass(frozen=True)
class Decision:
    scenario: str
    layer: str
    mode: str
    ecosystem: str
    deployment: str
    required_tooling: tuple[str, ...]
    vetoes: tuple[str, ...]
    checks: tuple[str, ...]
    rationale: tuple[str, ...]


REASONING_TASKS = {"multi_step_analysis", "coding_change", "contract_review"}
SIMPLE_TASKS = {"classification", "simple_generation", "summarization"}


def choose_mode(profile: TaskProfile) -> tuple[str, str]:
    if profile.task_type in REASONING_TASKS:
        return (
            "akil_yurutme",
            "Cok adimli analiz veya kod degisikligi ek dusunme butcesi gerektirir.",
        )
    if profile.task_type in SIMPLE_TASKS:
        return (
            "standart",
            "Basit siniflandirma, ozetleme veya kisa uretim icin hiz/maliyet onceliklidir.",
        )
    return (
        "standart",
        "Gorev turu net degilse once standart modla kucuk bir test seti denenir.",
    )


def choose_layer(profile: TaskProfile) -> tuple[str, str]:
    if profile.needs_action:
        return (
            "arac",
            "Dosya degistirme, kod calistirma veya islem yapma gereksinimi arac katmanini belirleyici yapar.",
        )
    if profile.needs_current_info or profile.needs_internal_sources or profile.needs_citations:
        return (
            "arac_model",
            "Kaynak, web arama veya RAG gereksinimi modelin etrafindaki arac katmanina baglidir.",
        )
    if profile.sensitive_data:
        return (
            "model_dagitim",
            "Hassas veri icin belirleyici soru modelin nerede calistigi ve verinin nereye gittigidir.",
        )
    return (
        "arac",
        "Kullanicinin isini hizli cozen sohbet veya API arayuzu belirleyici katmandir.",
    )


def choose_ecosystem(profile: TaskProfile) -> tuple[str, str, tuple[str, ...]]:
    if profile.sensitive_data:
        return (
            "acik_agirlikli_yerel_veya_sik_sozlesmeli_kurumsal_api",
            "yerel_oncelikli",
            ("ucretsiz_genel_sohbet_arayuzu",),
        )
    if profile.needs_action:
        return (
            "arac_izinlerine_gore_kapali_veya_acik",
            "aracin_izole_ortami_ve_onay_akisi",
            (),
        )
    return (
        "kapali_api_veya_sohbet_araci_yeterli_olabilir",
        "bulut_api_kabul_edilebilir",
        (),
    )


def collect_tooling(profile: TaskProfile) -> tuple[str, ...]:
    tooling: list[str] = []
    if profile.needs_current_info:
        tooling.append("web_aramasi")
    if profile.needs_internal_sources:
        tooling.append("rag_belge_arama")
    if profile.needs_citations:
        tooling.append("kaynak_gosterebilen_arac")
    if profile.needs_action:
        tooling.append("ajan_tabanli_arac_diff_ve_test_onayi")
    if not tooling:
        tooling.append("sohbet_veya_api_yeterli_olabilir")
    return tuple(tooling)


def collect_checks(profile: TaskProfile) -> tuple[str, ...]:
    checks = ["kendi_3_10_ornek_mini_test_seti"]
    if profile.sensitive_data:
        checks.extend(["veri_saklama_log_telemetri_kontrolu", "gizlilik_sozlesmesi_kontrolu"])
    if profile.commercial_use:
        checks.append("lisans_ve_ticari_kullanim_kontrolu")
    if profile.latency_sensitive:
        checks.append("gecikme_olcumu")
    if profile.budget_sensitive:
        checks.append("hacim_ve_birim_maliyet_kontrolu")
    if profile.turkish_quality_required:
        checks.append("turkce_orneklerle_kalite_kontrolu")
    if profile.needs_action:
        checks.append("insan_diff_review_ve_test")
    return tuple(checks)


def decide(profile: TaskProfile) -> Decision:
    mode, mode_reason = choose_mode(profile)
    layer, layer_reason = choose_layer(profile)
    ecosystem, deployment, vetoes = choose_ecosystem(profile)
    tooling = collect_tooling(profile)
    checks = collect_checks(profile)

    return Decision(
        scenario=profile.name,
        layer=layer,
        mode=mode,
        ecosystem=ecosystem,
        deployment=deployment,
        required_tooling=tooling,
        vetoes=vetoes,
        checks=checks,
        rationale=(layer_reason, mode_reason),
    )


def format_decision(decision: Decision) -> str:
    lines = [
        f"== {decision.scenario} ==",
        f"Katman: {decision.layer}",
        f"Mod: {decision.mode}",
        f"Ekosistem: {decision.ecosystem}",
        f"Dagitim: {decision.deployment}",
        "Arac gereksinimi: " + ", ".join(decision.required_tooling),
        "Veto: " + (", ".join(decision.vetoes) if decision.vetoes else "yok"),
        "Kontroller: " + ", ".join(decision.checks),
        "Gerekce: " + " ".join(decision.rationale),
    ]
    return "\n".join(lines)


def demo_profiles() -> tuple[TaskProfile, ...]:
    return (
        TaskProfile(
            name="Gunluk sohbet ve ozet",
            task_type="simple_generation",
            latency_sensitive=True,
            budget_sensitive=True,
        ),
        TaskProfile(
            name="Kod tabaninda hata duzeltme",
            task_type="coding_change",
            needs_action=True,
            needs_internal_sources=True,
            commercial_use=True,
        ),
        TaskProfile(
            name="Gizli muhasebe verisi ozeti",
            task_type="summarization",
            sensitive_data=True,
            commercial_use=True,
        ),
    )


def demo() -> None:
    for profile in demo_profiles():
        print(format_decision(decide(profile)))
        print()


if __name__ == "__main__":
    demo()
