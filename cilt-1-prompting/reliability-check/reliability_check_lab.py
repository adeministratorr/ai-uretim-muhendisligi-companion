"""Güvenilirlik Piramidi Denetleyicisi.

Kitap bağlantısı: Cilt 1, Bölüm 11 (AI Çıktısını Değerlendirmek), 11.5-11.8.
Gerçek bir API çağrısı yapmaz. Bir AI çıktısından ayrılmış iddiaları (claim)
tek tek listeye alır ve her biri için üç şeyi zorunlu kılar:

1. İddia kritik mi (piramidin tepesine mi giriyor — 11.5, 11.13)?
2. İddia hangi kanıt kademesinde (kendi bilgin / genel bilgi / doğrulanabilir
   kaynak / birincil kaynak — 11.5 ve 11.8'in birleşimi)?
3. Kaynak varsa adı belirtildi mi, kullanıcı bizzat doğruladı mı (11.7, 11.8)?

Bu kurallardan hareketle her iddiayı "hazır" / "uyarı" / "hata" olarak
işaretler; kaynaksız kritik iddialar (piramidin tepesinde ama tabandaki
kanıt gücüyle bırakılmış iddialar) uyarı üretir.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class EvidenceTier(str, Enum):
    """11.5 (güvenilirlik piramidi) ve 11.8 (birincil/ikincil kaynak) ile
    uyumlu, en zayıftan en güçlüye sıralanmış dört kanıt kademesi."""

    OWN_KNOWLEDGE = "kendi_bilgin"
    GENERAL_KNOWLEDGE = "genel_bilgi"
    VERIFIABLE_SOURCE = "dogrulanabilir_kaynak"
    PRIMARY_SOURCE = "birincil_kaynak"


TIER_LABELS: dict[EvidenceTier, str] = {
    EvidenceTier.OWN_KNOWLEDGE: "Kendi bilgin (modelin ezberi, kaynaksız)",
    EvidenceTier.GENERAL_KNOWLEDGE: "Genel bilgi (yaygın, tartışmasız)",
    EvidenceTier.VERIFIABLE_SOURCE: "Doğrulanabilir kaynak (ikincil kaynak)",
    EvidenceTier.PRIMARY_SOURCE: "Birincil kaynak (olayı doğrudan üreten kaynak)",
}

# Sırasıyla en zayıftan en güçlüye; _tier_rank bu sırayı karşılaştırmak için kullanılır.
_TIER_ORDER: tuple[EvidenceTier, ...] = (
    EvidenceTier.OWN_KNOWLEDGE,
    EvidenceTier.GENERAL_KNOWLEDGE,
    EvidenceTier.VERIFIABLE_SOURCE,
    EvidenceTier.PRIMARY_SOURCE,
)

# Kritik (piramidin tepesindeki) bir iddianın kabul edilebilmesi için gereken
# asgari kanıt kademesi (11.5: "piramidin tepesi ... birden fazla bağımsız
# kaynak" ve 11.13: hassas alanlarda ek doğrulama).
MINIMUM_TIER_FOR_CRITICAL = EvidenceTier.VERIFIABLE_SOURCE

# Kaynak adı zorunlu olan kademeler (11.7: "her madde için kaynağı adıyla belirt").
TIERS_REQUIRING_SOURCE_NAME = (EvidenceTier.VERIFIABLE_SOURCE, EvidenceTier.PRIMARY_SOURCE)


def _tier_rank(tier: EvidenceTier) -> int:
    return _TIER_ORDER.index(tier)


@dataclass(frozen=True)
class Claim:
    """Bir AI çıktısından fact-checking'in birinci adımında (11.6) ayrılmış
    tek bir doğrulanabilir iddia."""

    text: str
    is_critical: bool = False
    evidence_tier: EvidenceTier = EvidenceTier.OWN_KNOWLEDGE
    source_name: str = ""
    verified_by_user: bool = False

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("iddia metni boş olamaz")


@dataclass(frozen=True)
class ClaimAudit:
    """Tek bir iddia için denetim sonucu."""

    claim: Claim
    status: str  # "hazir" | "uyari" | "hata"
    messages: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return self.status == "hazir"


def audit_claim(claim: Claim) -> ClaimAudit:
    """Tek bir iddiayı 11.5-11.8'deki kurallara göre denetler."""
    messages: list[str] = []
    status = "hazir"

    needs_name = claim.evidence_tier in TIERS_REQUIRING_SOURCE_NAME
    has_name = bool(claim.source_name.strip())

    if needs_name and not has_name:
        status = "hata"
        messages.append(
            "Bu kademe (doğrulanabilir kaynak / birincil kaynak) için kaynağı "
            "adıyla belirtmek zorunludur (11.7)."
        )

    if claim.is_critical and _tier_rank(claim.evidence_tier) < _tier_rank(MINIMUM_TIER_FOR_CRITICAL):
        if status != "hata":
            status = "uyari"
        messages.append(
            "Kaynaksız kritik iddia: piramidin tepesindeki bu iddia yalnızca "
            "kendi bilgiye/genel bilgiye dayanıyor; en az doğrulanabilir bir "
            "kaynak gerekir (11.5, 11.13)."
        )

    if claim.is_critical and needs_name and has_name and not claim.verified_by_user:
        if status != "hata":
            status = "uyari"
        messages.append(
            "Kaynak adı var ama kullanıcı doğrulaması eksik: 'bir kaynak var' "
            "ile 'bu kaynak bu cümleyi destekliyor' aynı şey değildir (11.8)."
        )

    if not messages:
        messages.append("İddia, işaretlenen kanıt kademesine uygun biçimde belgelendirilmiş.")

    return ClaimAudit(claim=claim, status=status, messages=tuple(messages))


@dataclass(frozen=True)
class PyramidReport:
    """Bir taslaktaki tüm iddiaların toplu denetim sonucu."""

    audits: tuple[ClaimAudit, ...]

    @property
    def error_count(self) -> int:
        return sum(1 for audit in self.audits if audit.status == "hata")

    @property
    def warning_count(self) -> int:
        return sum(1 for audit in self.audits if audit.status == "uyari")

    @property
    def ready_to_publish(self) -> bool:
        return self.error_count == 0 and self.warning_count == 0

    def summary(self) -> str:
        durum = "yayına hazır" if self.ready_to_publish else "ek doğrulama gerekli"
        return (
            f"İddia: {len(self.audits)} | Hata: {self.error_count} | "
            f"Uyarı: {self.warning_count} | Durum: {durum}"
        )


def audit_claims(claims: list[Claim]) -> PyramidReport:
    """Bir iddia listesini denetleyip toplu bir rapor üretir."""
    if not claims:
        raise ValueError("en az bir iddia gerekir")
    return PyramidReport(audits=tuple(audit_claim(claim) for claim in claims))


# Kitaptaki 11.11 UYGULAMA örneğinin (Mert'in ekibi, ilçe haberi) dört iddiası.
EXAMPLE_CLAIMS: list[Claim] = [
    Claim(
        text="İlçede son iki yılda küçük işletme sayısı arttı",
        is_critical=False,
        evidence_tier=EvidenceTier.VERIFIABLE_SOURCE,
        source_name="İlgili resmî kayıt/oda verisi",
        verified_by_user=True,
    ),
    Claim(
        text="Bir yetkili bu artışın teşvik programından kaynaklandığını söyledi",
        is_critical=True,
        evidence_tier=EvidenceTier.OWN_KNOWLEDGE,
        source_name="",
        verified_by_user=False,
    ),
    Claim(
        text="Artış oranı yaklaşık yüzde 18",
        is_critical=True,
        evidence_tier=EvidenceTier.GENERAL_KNOWLEDGE,
        source_name="",
        verified_by_user=False,
    ),
    Claim(
        text="İlçenin nüfusu resmî kayıtlara göre yaklaşık 42 bin",
        is_critical=False,
        evidence_tier=EvidenceTier.PRIMARY_SOURCE,
        source_name="İlgili kamu kurumunun resmî web sayfası",
        verified_by_user=True,
    ),
]


def demo() -> None:
    report = audit_claims(EXAMPLE_CLAIMS)
    print("Mert'in ekibinin ilçe haberi taslağı — 4 iddia denetimi:\n")
    for audit in report.audits:
        print(f"[{audit.status.upper()}] {audit.claim.text}")
        print(f"  Kademe: {TIER_LABELS[audit.claim.evidence_tier]}")
        for message in audit.messages:
            print(f"  - {message}")
        print()
    print(report.summary())


if __name__ == "__main__":
    demo()
