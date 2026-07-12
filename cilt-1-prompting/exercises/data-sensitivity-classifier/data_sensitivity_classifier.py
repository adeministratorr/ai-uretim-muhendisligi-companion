"""Bir veri açıklamasını Bölüm 12'deki (Sorumlu ve Etik Kullanım) üçlü ayrıma göre
sınıflandıran ve anonimleştirme/maskeleme önerisi üreten küçük bir laboratuvar.

Kitap bağlantısı: Cilt 1, Bölüm 12 (Sorumlu ve Etik Kullanım), özellikle 12.1-12.5
(dur-sınıflandır-anonimleştir-izin kontrol et refleksi; kişisel veri, hassas veri ve
kurum içi bilgi ayrımı; anonimleştirme ve maskeleme teknikleri; yeniden kimliklendirme
riski).

Gerçek bir API çağrısı yapmaz. Basit anahtar sözcük eşleştirmesiyle çalışan bir
öğretim aracıdır; gerçek bir veri sınıflandırma/DLP (Data Loss Prevention) sistemi
değildir — bkz. README.md, "Riskler ve Sınırlar".
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Sequence

# 12.2'deki sınıflandırma tablosundaki "Hassas veri" örnekleri: sağlık bilgisi,
# disiplin/ceza kaydı, din, etnik köken, cinsel yaşam/yönelim; 12.4'teki rehberlik
# görüşme notu örneği de bu kategoridedir. Bu kategori 12.2'ye göre anonimleştirmeyle
# bile çoğu kurumda gönderilmez.
SENSITIVE_PERSONAL_HINTS: tuple[str, ...] = (
    "sağlık raporu",
    "sağlık bilgisi",
    "sağlık durumu",
    "disiplin dosyası",
    "disiplin kaydı",
    "disiplin soruşturması",
    "ceza kaydı",
    "adli sicil",
    "din",
    "mezhep",
    "etnik köken",
    "cinsel yönelim",
    "cinsel yaşam",
    "rehberlik görüşme notu",
    "rehberlik notu",
    "aile içi sorun",
    "psikolojik değerlendirme",
)

# 12.2'deki "Kurum içi bilgi" örnekleri: bütçe taslağı, personel değerlendirme notu,
# yayımlanmamış sınav, kurumun gizli kaynak kodu. Bu kategori de "aksi açıkça izinli
# değilse" gönderilmez.
INSTITUTIONAL_HINTS: tuple[str, ...] = (
    "bütçe taslağı",
    "personel değerlendirme",
    "yayımlanmamış sınav",
    "henüz yayımlanmamış sınav",
    "gizli kaynak kodu",
    "kaynak kodu",
    "ticari sır",
)

# 12.2'deki "Kişisel veri" örnekleri: öğrenci adı + notu, veli telefon numarası.
# Bu kategori 12.5'teki teknikle anonimleştirilerek/maskelenerek gönderilebilir.
PERSONAL_HINTS: tuple[str, ...] = (
    "ad soyad",
    "adı soyadı",
    "isim",
    "t.c. kimlik",
    "tc kimlik",
    "kimlik numarası",
    "öğrenci numarası",
    "adres",
    "telefon numarası",
    "veli telefon",
    "doğum tarihi",
    "e-posta",
)

# 12.5'teki DİKKAT kutusundaki yeniden kimliklendirme (re-identification) örneğiyle
# aynı türden kendine özgü ayrıntılar: "10. sınıfta okuyan, geçen ay bölgesel bir
# yarışmayı kazanan tek öğrenci" gibi az sayıda kişiye özgü nitelikler.
REIDENTIFICATION_HINTS: tuple[str, ...] = (
    "tek öğrenci",
    "yalnızca bir",
    "tek kişi",
    "kazanan tek",
    "tek bilinen",
)

# 12.5'teki maskeleme tablosuyla birebir tutarlı öneriler: isim kodlama, doğum
# tarihi yerine sınıf seviyesi, adres yerine mahalle düzeyi bölge, T.C. kimlik/
# öğrenci numarasının tamamen çıkarılması.
MASKING_SUGGESTIONS: dict[str, str] = {
    "ad soyad": (
        "İsimleri 'Öğrenci 1', 'Öğrenci 2' gibi geçici kodlarla değiştirin; "
        "kod-isim eşleşmesini yapay zekâ aracına hiç gönderilmeyen ayrı bir "
        "dosyada tutun."
    ),
    "adı soyadı": (
        "İsimleri 'Öğrenci 1', 'Öğrenci 2' gibi geçici kodlarla değiştirin; "
        "kod-isim eşleşmesini yapay zekâ aracına hiç gönderilmeyen ayrı bir "
        "dosyada tutun."
    ),
    "isim": (
        "İsimleri 'Öğrenci 1', 'Öğrenci 2' gibi geçici kodlarla değiştirin; "
        "kod-isim eşleşmesini yapay zekâ aracına hiç gönderilmeyen ayrı bir "
        "dosyada tutun."
    ),
    "t.c. kimlik": "T.C. kimlik numarasını tamamen çıkarın (maskelemeyin, tamamen kaldırın).",
    "tc kimlik": "T.C. kimlik numarasını tamamen çıkarın (maskelemeyin, tamamen kaldırın).",
    "kimlik numarası": "Kimlik numarasını tamamen çıkarın (maskelemeyin, tamamen kaldırın).",
    "öğrenci numarası": "Öğrenci numarasını tamamen çıkarın (maskelemeyin, tamamen kaldırın).",
    "adres": "Ev adresi yerine yalnızca mahalle düzeyinde genel bir bölge belirtin.",
    "telefon numarası": (
        "Telefon numarasını tamamen çıkarın; gerekirse kurumun ilgili biriminde "
        "ayrı ve güvenli saklayın."
    ),
    "veli telefon": (
        "Veli telefon numarasını tamamen çıkarın; gerekirse kurumun ilgili "
        "biriminde ayrı ve güvenli saklayın."
    ),
    "doğum tarihi": "Doğum tarihi yerine yalnızca sınıf seviyesini veya yaş grubunu yazın.",
    "e-posta": "E-posta adresini tamamen çıkarın veya kurum içi bir kodla değiştirin.",
}

CATEGORY_LABELS: dict[str, str] = {
    "dogrudan": "Doğrudan gönderilebilir",
    "anonimlestirerek": "Anonimleştirilerek gönderilebilir",
    "hic_gonderilemez": "Hiç gönderilemez",
}


@dataclass(frozen=True)
class Classification:
    """12.1-12.2'deki üçlü ayrıma göre üretilen sınıflandırma sonucu."""

    category: str  # "dogrudan" | "anonimlestirerek" | "hic_gonderilemez"
    category_label: str
    gerekce: str
    sensitive_matches: tuple[str, ...]
    institutional_matches: tuple[str, ...]
    personal_matches: tuple[str, ...]
    masking_suggestions: tuple[str, ...]
    reidentification_warning: str | None

    @property
    def gonderilebilir(self) -> bool:
        """Anonimleştirme uygulanmadan doğrudan gönderilebilir mi?"""
        return self.category == "dogrudan"


def _find_matches(text: str, hints: Sequence[str]) -> tuple[str, ...]:
    """`text` içinde geçen `hints` öğelerini, tanımlandıkları sırayla döndürür."""
    lowered = text.casefold()
    return tuple(hint for hint in hints if hint in lowered)


def classify_data(description: str) -> Classification:
    """Bir veri açıklamasını dur-sınıflandır-anonimleştir-izin kontrol et
    refleksinin (12.1) "sınıflandır" adımına göre üç kategoriden birine ayırır ve
    gerekliyse 12.5'teki maskeleme tekniğine uygun öneriler üretir.

    Öncelik sırası 12.2'deki tabloyla tutarlıdır: hassas veri veya kurum içi bilgi
    işareti bulunursa (anonimleştirilse bile) "hiç gönderilemez" kategorisi kazanır;
    yalnızca kişisel veri işareti varsa "anonimleştirilerek gönderilebilir"; hiçbiri
    yoksa "doğrudan gönderilebilir" varsayılır (12.1'deki "genel/herkese açık bilgi").
    """
    if not description or not description.strip():
        raise ValueError("description boş olamaz")

    sensitive = _find_matches(description, SENSITIVE_PERSONAL_HINTS)
    institutional = _find_matches(description, INSTITUTIONAL_HINTS)
    personal = _find_matches(description, PERSONAL_HINTS)

    if sensitive or institutional:
        category = "hic_gonderilemez"
        if sensitive and institutional:
            gerekce = (
                "Metinde hem hassas veri (" + ", ".join(sensitive) + ") hem kurum içi "
                "bilgi (" + ", ".join(institutional) + ") işareti bulundu; 12.2'ye göre "
                "bu iki kategori anonimleştirmeyle bile yapay zekâ aracına gönderilmez."
            )
        elif sensitive:
            gerekce = (
                "Metinde hassas veri işareti bulundu (" + ", ".join(sensitive) + "); "
                "12.2'ye göre hassas veri kişisel veriden daha sıkı korunur ve çoğu "
                "kurumda hiçbir şekilde gönderilmez."
            )
        else:
            gerekce = (
                "Metinde kurum içi bilgi işareti bulundu (" + ", ".join(institutional) + "); "
                "12.2'ye göre bu kategori aksi açıkça izinli olmadıkça gönderilmez."
            )
        return Classification(
            category=category,
            category_label=CATEGORY_LABELS[category],
            gerekce=gerekce,
            sensitive_matches=sensitive,
            institutional_matches=institutional,
            personal_matches=personal,
            masking_suggestions=(),
            reidentification_warning=None,
        )

    if personal:
        category = "anonimlestirerek"
        gerekce = (
            "Metinde kişisel veri işareti bulundu (" + ", ".join(personal) + "); "
            "12.1-12.2'ye göre bu veri, kimliklendirici bilgi çıkarılıp maskelendikten "
            "sonra gönderilebilir."
        )
        masking_suggestions = tuple(
            dict.fromkeys(
                MASKING_SUGGESTIONS[hint] for hint in personal if hint in MASKING_SUGGESTIONS
            )
        )
        reid_hits = _find_matches(description, REIDENTIFICATION_HINTS)
        reidentification_warning = (
            (
                "DİKKAT (12.5): Metin '" + ", ".join(reid_hits) + "' gibi kendine özgü bir "
                "ayrıntı içeriyor; isim çıkarılsa bile bu ayrıntı kişiyi yeniden "
                "tanımlanabilir kılabilir (yeniden kimliklendirme riski). Yalnızca ismi "
                "değil, kişiyi tekilleştiren tüm ayrıntıları gözden geçirin."
            )
            if reid_hits
            else None
        )
        return Classification(
            category=category,
            category_label=CATEGORY_LABELS[category],
            gerekce=gerekce,
            sensitive_matches=sensitive,
            institutional_matches=institutional,
            personal_matches=personal,
            masking_suggestions=masking_suggestions,
            reidentification_warning=reidentification_warning,
        )

    category = "dogrudan"
    gerekce = (
        "Metinde kişisel veri, hassas veri veya kurum içi bilgi işareti bulunamadı; "
        "12.1'e göre genel/herkese açık bilgi doğrudan gönderilebilir."
    )
    return Classification(
        category=category,
        category_label=CATEGORY_LABELS[category],
        gerekce=gerekce,
        sensitive_matches=sensitive,
        institutional_matches=institutional,
        personal_matches=personal,
        masking_suggestions=(),
        reidentification_warning=None,
    )


def format_classification(description: str, result: Classification) -> str:
    lines = [f"Veri: {description}", f"Karar: {result.category_label}", f"Gerekçe: {result.gerekce}"]
    if result.masking_suggestions:
        lines.append("Maskeleme önerileri:")
        lines.extend(f"- {suggestion}" for suggestion in result.masking_suggestions)
    if result.reidentification_warning:
        lines.append(result.reidentification_warning)
    return "\n".join(lines)


# 12.1'in kalibrasyon örneğiyle (satır 372-377) tutarlı dört senaryo: biri güvenli,
# biri hassas veri (kitaptaki iki kalibrasyon örneğiyle birebir aynı), biri kişisel
# veri (12.5'teki maskeleme tablosunu tetikler), biri de yeniden kimliklendirme
# uyarısını tetikleyen kişisel veri + kendine özgü ayrıntı bileşimi.
DEMO_CASES: tuple[str, ...] = (
    "7. sınıf fen bilgisi müfredatının bu haftaki konusu fotosentez.",
    "Öğrencinin rehberlik görüşme notu: ailede boşanma süreci yaşanıyor.",
    "Ayşe Yılmaz'ın bu dönem matematik notu 72; veli telefon numarası 0532 xxx xx xx.",
    (
        "Öğrencinin ad soyad bilgisi ve son sınav notu birlikte paylaşılacak; "
        "üstelik bu öğrenci geçen ay bölgesel bir yarışmayı kazanan tek öğrenci."
    ),
    "Okulun bir sonraki dönem bütçe taslağı ve öğretmenlerin performans değerlendirme notları.",
)


def demo() -> None:
    for description in DEMO_CASES:
        result = classify_data(description)
        print(format_classification(description, result))
        print("---")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bölüm 12 veri hassasiyeti sınıflandırıcısı (12.1-12.5)"
    )
    parser.add_argument(
        "description",
        nargs="?",
        default=None,
        help="Sınıflandırılacak veri açıklaması; verilmezse kitaptaki örnek senaryolar çalışır.",
    )
    args = parser.parse_args(argv)

    if args.description is None:
        demo()
        return 0

    result = classify_data(args.description)
    print(format_classification(args.description, result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
