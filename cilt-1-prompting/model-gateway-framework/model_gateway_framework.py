"""Cilt 1 Bolum 17.5 icin model gateway ihtiyac cercevesi laboratuvari.

Gercek bir model veya saglayici cagirmaz; model/arac adi, fiyat ya da benchmark
iddiasi uretmez. Bolum 17.5'teki KAVRAM kutusunun mantigini ("model gateway,
birden fazla saglayiciyi tek bir ortak noktadan cagirmayi saglayan ara katmandir;
hangi saglayicinin kullanilacagina o karar verir, kullanimi ve maliyeti de tek
yerden kaydeder") deterministik bir kontrol listesine cevirir.

Bu laboratuvar bir kurumun mevcut durumunu (kac farkli saglayici/model
kullaniliyor, maliyet izleme var mi, yedek saglayici var mi, tek noktadan
yonlendirme var mi) girdi olarak alir ve "gateway'e ihtiyaciniz var mi" sorusuna
kanita dayali, gerekceli bir cevap uretir. Sadece saglayici sayisina bakmaz:
iki saglayici kullanilsa bile maliyet izleme, yonlendirme ve yedekleme zaten
elde tutuluyorsa gateway katmani su an icin gereksiz ek karmasiklik olarak
degerlendirilir.
"""
from dataclasses import dataclass

# 2+ saglayici olmadan gateway'in cozdugu temel problem (tek noktadan
# karsilastirma/yonlendirme) zaten ortaya cikmaz.
MIN_PROVIDERS_FOR_GATEWAY = 2

# Bu esikten itibaren toplanan sinyal, "gerekmiyor" degerlendirmesinden
# "onerilir" degerlendirmesine gecisi belirler.
STRONG_SIGNAL_THRESHOLD = 3

GENERAL_CAUTION = (
    "Gateway kullanmak maliyeti otomatik olarak dusurmez; ara katmanin kendi "
    "gecikmesi olabilir ve bazi saglayiciya ozgu bir ozellik gateway uzerinden "
    "tam desteklenmeyebilir."
)

LOCAL_DATA_CAUTION = (
    "Yerel calistirma guvencesi yalnizca cikarim adimi icin gecerlidir; "
    "loglama, izleme veya harici bir arama/RAG servisi hala kurum disi bir "
    "sunucuya bagliysa veri o bilesen uzerinden disari cikabilir."
)

TOTAL_COST_CAUTION = (
    "Karar yalnizca birim fiyatla degil, toplam isletme maliyetiyle "
    "(donanim, bakim, guncelleme emegi ve hatali secimin duzeltme maliyeti "
    "dahil) verilmelidir; en ucuz secenek her zaman en dogru secim degildir."
)


@dataclass(frozen=True)
class OrganizationProfile:
    """Bir kurumun/ekibin model-saglayici kullanim durumunu ozetler."""

    name: str
    provider_count: int
    has_cost_tracking: bool = False
    has_fallback_provider: bool = False
    has_central_routing: bool = False
    switches_provider_by_task: bool = False
    sensitive_data_requires_local: bool = False
    plans_to_add_provider: bool = False


@dataclass(frozen=True)
class GatewayAssessment:
    """`evaluate_need` fonksiyonunun urettigi kanita dayali degerlendirme."""

    organization: str
    verdict: str
    signal_count: int
    reasons: tuple[str, ...]
    cautions: tuple[str, ...]
    recommendation: str


def collect_signals(profile: OrganizationProfile) -> tuple[str, ...]:
    """Birden fazla saglayici varken gateway ihtiyacini guclendiren sinyalleri toplar."""
    signals: list[str] = []
    if not profile.has_cost_tracking:
        signals.append(
            "Maliyet tek yerden izlenmiyor; her saglayicinin faturasi ayri takip ediliyor."
        )
    if profile.switches_provider_by_task:
        signals.append(
            "Gorev karmasikligina gore saglayici/model degistiriliyor; bu gecis elle yonetiliyor."
        )
    if not profile.has_central_routing:
        signals.append(
            "Tek noktadan yonlendirme yok; her saglayiciya ayri entegrasyon/arayuzle baglaniliyor."
        )
    if not profile.has_fallback_provider:
        signals.append(
            "Yedek saglayici yok; birincil saglayici durdugunda elle gecis planina bagli kaliniyor."
        )
    return tuple(signals)


def collect_cautions(profile: OrganizationProfile) -> tuple[str, ...]:
    """Verdict ne olursa olsun hatirlatilmasi gereken sinirlari toplar."""
    cautions = [GENERAL_CAUTION, TOTAL_COST_CAUTION]
    if profile.sensitive_data_requires_local:
        cautions.append(LOCAL_DATA_CAUTION)
    return tuple(cautions)


def evaluate_need(profile: OrganizationProfile) -> GatewayAssessment:
    """Bolum 17.5'teki KAVRAM kutusunun mantigini profile uygular.

    Saglayici sayisi ikiden azsa (`MIN_PROVIDERS_FOR_GATEWAY` altinda), gateway'in
    cozdugu temel problem (birden fazla saglayiciyi tek noktadan karsilastirma)
    henuz ortaya cikmamis demektir; doğrudan saglayici API'si yeterli kabul edilir.
    Iki veya daha fazla saglayici varsa, maliyet izleme/yonlendirme/yedekleme
    eksikliklerinden toplanan sinyal sayisi `STRONG_SIGNAL_THRESHOLD` esigini
    gecerse gateway onerilir; esigin altindaysa "degerlendirilebilir" ama henuz
    zorunlu degil sonucu dondurulur.
    """
    cautions = collect_cautions(profile)

    if profile.provider_count < MIN_PROVIDERS_FOR_GATEWAY:
        reason = (
            "Tek saglayici kullaniliyor; birden fazla saglayiciyi tek noktadan "
            "karsilastirma/yonlendirme ihtiyaci henuz yok."
        )
        if profile.plans_to_add_provider:
            recommendation = (
                "Ikinci bir saglayici eklenmesi planlaniyor; gateway'i su an degil, "
                "ikinci saglayici devreye girdiginde yeniden degerlendirin."
            )
        else:
            recommendation = (
                "Saglayici sayisi artmadan gateway kurmak, gecikme ekleyen bir ara "
                "katmani erken devreye sokar; ihtiyac dogdugunda tekrar degerlendirin."
            )
        return GatewayAssessment(
            organization=profile.name,
            verdict="dogrudan_api_yeterli",
            signal_count=0,
            reasons=(reason,),
            cautions=cautions,
            recommendation=recommendation,
        )

    signals = collect_signals(profile)
    reasons = (
        f"{profile.provider_count} farkli saglayici/model kullaniliyor "
        f"(esik: {MIN_PROVIDERS_FOR_GATEWAY}+).",
    ) + signals

    if len(signals) >= STRONG_SIGNAL_THRESHOLD:
        verdict = "gateway_onerilir"
        recommendation = (
            "Birden fazla saglayici zaten kullaniliyor ve maliyet/yonlendirme/yedekleme "
            "boslugu birikmis; bir gateway bu takibi tek noktaya tasir ve saglayici "
            "degisikliginde ust katmanin buyuk olcude ayni kalmasini saglar."
        )
    elif len(signals) >= 1:
        verdict = "gateway_degerlendirilebilir"
        recommendation = (
            "Birden fazla saglayici var ama eksik yalnizca bir-iki noktada; once bu "
            "boslugu (maliyet izleme, yonlendirme veya yedekleme) tek basina kapatmak "
            "yeterli olabilir, gateway kurmak simdilik zorunlu degil."
        )
    else:
        verdict = "dogrudan_api_yeterli"
        recommendation = (
            "Birden fazla saglayici kullanilsa da maliyet izleme, yonlendirme ve "
            "yedekleme zaten elde tutuluyor; gateway katmani su an icin ek "
            "karmasiklik ekleyebilir."
        )

    return GatewayAssessment(
        organization=profile.name,
        verdict=verdict,
        signal_count=len(signals),
        reasons=reasons,
        cautions=cautions,
        recommendation=recommendation,
    )


def format_assessment(assessment: GatewayAssessment) -> str:
    lines = [
        f"== {assessment.organization} ==",
        f"Sonuc: {assessment.verdict}",
        f"Sinyal sayisi: {assessment.signal_count}",
        "Gerekce: " + " | ".join(assessment.reasons),
        "Dikkat: " + " | ".join(assessment.cautions),
        "Oneri: " + assessment.recommendation,
    ]
    return "\n".join(lines)


def demo_profiles() -> tuple[OrganizationProfile, ...]:
    """Bolum 17.5'teki Deniz ornegine karsilik gelen dort profil."""
    return (
        OrganizationProfile(
            name="Hukuk burosu (tek yerel model, gizli veri)",
            provider_count=1,
            has_cost_tracking=True,
            has_fallback_provider=False,
            has_central_routing=False,
            switches_provider_by_task=False,
            sensitive_data_requires_local=True,
        ),
        OrganizationProfile(
            name="Tekstil atolyesi (gorev karmasikligina gore model degistiriyor)",
            provider_count=2,
            has_cost_tracking=False,
            has_fallback_provider=False,
            has_central_routing=False,
            switches_provider_by_task=True,
        ),
        OrganizationProfile(
            name="Kucuk ekip (iki saglayici, ama takip zaten kurulu)",
            provider_count=2,
            has_cost_tracking=True,
            has_fallback_provider=True,
            has_central_routing=True,
            switches_provider_by_task=False,
        ),
        OrganizationProfile(
            name="Deniz'in toplami (uc musteri, uc saglayici)",
            provider_count=3,
            has_cost_tracking=False,
            has_fallback_provider=False,
            has_central_routing=False,
            switches_provider_by_task=True,
            sensitive_data_requires_local=True,
        ),
    )


def demo() -> None:
    for profile in demo_profiles():
        print(format_assessment(evaluate_need(profile)))
        print()


if __name__ == "__main__":
    demo()
