"""Cilt 1 Bölüm 9 için multimodal çıktı denetimi laboratuvarı.

Gerçek model çağrısı yapmaz. Bir ekran görüntüsü, grafik, tablo veya PDF kesiti
için üretilen model cevabının Bölüm 9'daki dört adımlı yapıya uyup uymadığını
basit metin işaretleriyle denetler.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


REQUIRED_SECTIONS = (
    "description",
    "interpretation",
    "assumptions",
    "privacy",
)

SECTION_LABELS = {
    "description": "betimleme",
    "interpretation": "yorum",
    "assumptions": "varsayım listesi",
    "privacy": "gizlilik ve telif kontrolü",
}

SECTION_ALIASES = {
    "description": ("betimleme", "gözlem"),
    "interpretation": ("yorum", "değerlendirme"),
    "assumptions": ("varsayım listesi", "varsayımlar"),
    "privacy": ("gizlilik ve telif kontrolü", "gizlilik", "telif kontrolü"),
}

INTERPRETATION_MARKERS = (
    "olası neden",
    "muhtemelen",
    "kesin",
    "teşhis",
    "uygundur",
    "uygun değildir",
)

REFERENCE_GUARD_MARKERS = (
    "sözlük verilmedi",
    "doküman verilmedi",
    "kesin neden söylemiyorum",
    "tahmin üretmiyorum",
    "dayanak yok",
)

VERIFICATION_MARKERS = (
    "doğrula",
    "kontrol",
    "bakılmalı",
    "servis dokümanı",
    "bakım kaydı",
    "ham veri",
    "uzman",
    "teknisyen",
    "fiziksel ölçüm",
    "veri tabanı",
)

PRIVACY_MARKERS = (
    "risk yok",
    "kırp",
    "maskele",
    "bulanıklaştır",
    "anonim",
    "meta veri",
    "izin",
    "veri politikası",
    "telif",
)


@dataclass(frozen=True)
class MultimodalReviewTask:
    source_kind: str
    question: str
    context: str
    reference_document: str = ""
    privacy_risks: tuple[str, ...] = ("yüz", "rozet", "müşteri bilgisi", "tedarikçi çizimi")

    @property
    def has_reference(self) -> bool:
        return bool(self.reference_document.strip())


@dataclass(frozen=True)
class ResponseAudit:
    ready: bool
    missing_sections: tuple[str, ...]
    assumption_count: int
    assumptions_with_verification: int
    description_clean: bool
    reference_guard_ready: bool
    privacy_ready: bool


def render_review_prompt(task: MultimodalReviewTask) -> str:
    reference_rule = (
        f"Yorum adımında yalnızca şu dayanağa yaslan: {task.reference_document}."
        if task.has_reference
        else (
            "Kod sözlüğü, servis dokümanı veya ham veri verilmediyse olası neden "
            "uydurma; dayanak yoksa bunu açıkça yaz."
        )
    )
    risks = ", ".join(task.privacy_risks)
    return "\n".join(
        [
            f"Ekli {task.source_kind} için şu soruyu yanıtla: {task.question}",
            f"Bağlam: {task.context}",
            reference_rule,
            "",
            "Cevabı şu dört başlıkla ver:",
            "## Betimleme",
            "Yalnızca görünen veya belgede açıkça yazan bilgiyi aktar; yorum katma.",
            "## Yorum",
            "Dayanağı olan yorumu yaz; dayanak yoksa kesin neden söyleme.",
            "## Varsayım Listesi",
            "En az iki varsayım yaz ve her varsayımın nasıl doğrulanacağını belirt.",
            "## Gizlilik ve Telif Kontrolü",
            f"Şu riskleri kontrol et: {risks}. Risk yoksa gerekçesini yaz.",
        ]
    )


def normalize(text: str) -> str:
    return text.strip().casefold()


def section_key_for_heading(line: str) -> str | None:
    heading = normalize(line.lstrip("#").strip(" :.-"))
    for key, aliases in SECTION_ALIASES.items():
        if any(alias in heading for alias in aliases):
            return key
    return None


def extract_sections(response: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current_key: str | None = None

    for line in response.splitlines():
        if line.lstrip().startswith("#"):
            key = section_key_for_heading(line)
            if key:
                current_key = key
                sections.setdefault(key, [])
                continue
        if current_key:
            sections[current_key].append(line)

    return {key: "\n".join(lines).strip() for key, lines in sections.items()}


def bullet_lines(text: str) -> tuple[str, ...]:
    pattern = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+(.+)$")
    return tuple(
        match.group(1).strip()
        for line in text.splitlines()
        if (match := pattern.match(line))
    )


def contains_any(text: str, markers: tuple[str, ...]) -> bool:
    lowered = normalize(text)
    return any(marker in lowered for marker in markers)


def count_verifiable_assumptions(assumptions: tuple[str, ...]) -> int:
    return sum(1 for item in assumptions if contains_any(item, VERIFICATION_MARKERS))


def audit_response(response: str, reference_provided: bool = False) -> ResponseAudit:
    sections = extract_sections(response)
    missing = tuple(key for key in REQUIRED_SECTIONS if key not in sections)
    assumptions = bullet_lines(sections.get("assumptions", ""))
    description_clean = not contains_any(
        sections.get("description", ""), INTERPRETATION_MARKERS
    )
    reference_guard_ready = reference_provided or contains_any(
        sections.get("interpretation", ""), REFERENCE_GUARD_MARKERS
    )
    privacy_ready = contains_any(sections.get("privacy", ""), PRIVACY_MARKERS)
    assumptions_with_verification = count_verifiable_assumptions(assumptions)

    ready = (
        not missing
        and description_clean
        and reference_guard_ready
        and len(assumptions) >= 2
        and assumptions_with_verification >= 2
        and privacy_ready
    )

    return ResponseAudit(
        ready=ready,
        missing_sections=missing,
        assumption_count=len(assumptions),
        assumptions_with_verification=assumptions_with_verification,
        description_clean=description_clean,
        reference_guard_ready=reference_guard_ready,
        privacy_ready=privacy_ready,
    )


def weak_response() -> str:
    return """## Betimleme
Ekranda E-204 hatası görünüyor; muhtemelen sensör bozuk ve istasyon durdurulmalı.

## Yorum
Sensör kesin arızalı. Bakım ekibi sensörü değiştirmeli.
"""


def reviewable_response() -> str:
    return """## Betimleme
Ekranda "HATA E-204: Sensör bağlantısı zaman aşımına uğradı" metni ve
"İstasyon 7" etiketi görünüyor.

## Yorum
Bu sistemin hata kodu sözlüğü verilmedi. Bu yüzden kesin neden söylemiyorum;
kök neden için servis dokümanı ve bakım kaydı kontrol edilmeli.

## Varsayım Listesi
- E-204 kodunun bu sistemde aynı anlama geldiğini varsaydım; servis dokümanı ile doğrula.
- İstasyon 7 etiketinin fiziksel makineyle eşleştiğini varsaydım; bakım kaydı üzerinden kontrol et.
- Hatanın tekrar eden bir olay olup olmadığını bilmiyorum; veri tabanı geçmişine bakılmalı.

## Gizlilik ve Telif Kontrolü
Ekran görüntüsünde çalışan yüzü veya rozet görünmüyorsa risk yok notu yazılabilir.
Görünüyorsa paylaşmadan önce kalıcı maskeleme yapılmalı ve aracın veri politikası kontrol edilmeli.
"""


def example_task() -> MultimodalReviewTask:
    return MultimodalReviewTask(
        source_kind="ekran görüntüsü",
        question="Hata mesajını yorumla ve hangi noktaların doğrulanacağını yaz.",
        context="MES ekranı üretim hattındaki İstasyon 7 için alınmış.",
    )


def format_audit(name: str, audit: ResponseAudit) -> str:
    missing = ", ".join(SECTION_LABELS[item] for item in audit.missing_sections) or "yok"
    return "\n".join(
        [
            f"== {name} ==",
            f"Hazır: {'evet' if audit.ready else 'hayır'}",
            f"Eksik başlıklar: {missing}",
            f"Varsayım sayısı: {audit.assumption_count}",
            f"Doğrulanabilir varsayım: {audit.assumptions_with_verification}",
        ]
    )


def demo() -> None:
    print(render_review_prompt(example_task()))
    print()
    print(format_audit("Zayıf cevap", audit_response(weak_response())))
    print()
    print(format_audit("Denetlenebilir cevap", audit_response(reviewable_response())))


if __name__ == "__main__":
    demo()
