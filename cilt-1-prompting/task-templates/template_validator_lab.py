"""Cilt 1 Bölüm 8 için Şablon Doğrulayıcı laboratuvarı.

Gerçek model çağrısı yapmaz. Bölüm 8.2'nin beş sabit alanına (Amaç, Hedef Kitle,
Kaynak, Format, Sınır — bkz. Ek C, Prompt Şablon Kütüphanesi) göre yazılmış bir
şablonu, kullanıcı doldurduktan sonra saf metin işleme ile denetler: hangi köşeli
parantezli [DEĞİŞKEN] alanları hâlâ doldurulmamış, hangi zorunlu alanlar tümüyle
eksik veya boş bırakılmış. İsteğe bağlı altıncı alan (Başarı Kriteri, 8.2) tespit
edilir ama zorunlu sayılmaz.
"""

from __future__ import annotations

from dataclasses import dataclass

import re


REQUIRED_FIELDS: tuple[str, ...] = ("Amaç", "Hedef Kitle", "Kaynak", "Format", "Sınır")
OPTIONAL_FIELDS: tuple[str, ...] = ("Başarı Kriteri",)

_CANONICAL_LABELS = {
    "amaç": "Amaç",
    "hedef kitle": "Hedef Kitle",
    "kaynak": "Kaynak",
    "format": "Format",
    "sınır": "Sınır",
    "başarı kriteri": "Başarı Kriteri",
}

_FIELD_LABEL_PATTERN = re.compile(
    r"(?P<label>Amaç|Hedef\s+[Kk]itle|Kaynak|Format|Sınır|Başarı\s+[Kk]riteri)\s*:\s*",
    re.IGNORECASE,
)

_VARIABLE_PATTERN = re.compile(r"\[([^\[\]]+)\]")


@dataclass(frozen=True)
class TemplateExample:
    """Ek C'den alınan bir persona şablonu (bkz. prompt_sablon_kutuphanesi.md)."""

    persona: str
    title: str
    template: str


@dataclass(frozen=True)
class FieldCheck:
    """Beş alandan (veya isteğe bağlı altıncısından) birinin denetim sonucu."""

    name: str
    present: bool
    is_empty: bool
    unfilled_variables: tuple[str, ...]


@dataclass(frozen=True)
class ValidationReport:
    """`validate_template`in ürettiği tam denetim raporu."""

    template_name: str
    fields: tuple[FieldCheck, ...]
    missing_fields: tuple[str, ...]
    empty_fields: tuple[str, ...]
    unfilled_variables: tuple[str, ...]
    is_ready: bool


def _canonical_label(raw_label: str) -> str:
    normalized = re.sub(r"\s+", " ", raw_label.strip())
    return _CANONICAL_LABELS.get(normalized.lower(), normalized)


def find_variables(text: str) -> tuple[str, ...]:
    """Metindeki hâlâ doldurulmamış [DEĞİŞKEN] alanlarını, göründükleri sırayla döndürür."""
    return tuple(_VARIABLE_PATTERN.findall(text))


def parse_fields(text: str) -> dict[str, str]:
    """"Alan: içerik" biçimindeki bir şablon metnini alan adı -> içerik sözlüğüne çevirir.

    Ek C'deki şablonlar tek paragraf içinde "Amaç: ... Hedef kitle: ... Kaynak: ...
    Format: ... Sınır: ..." sırasını izler (bkz. Bölüm 8.2). Bu fonksiyon büyük/küçük
    harfe duyarsız çalışır ve yalnızca beş zorunlu alan ile isteğe bağlı "Başarı
    Kriteri" alanını tanır; metinde bu etiketlerin dışında geçen ":" karakterleri
    alan sınırı sayılmaz.
    """
    matches = list(_FIELD_LABEL_PATTERN.finditer(text))
    fields: dict[str, str] = {}
    for index, match in enumerate(matches):
        name = _canonical_label(match.group("label"))
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        if content.endswith("."):
            content = content[:-1].rstrip()
        fields[name] = content
    return fields


def validate_template(text: str, template_name: str = "") -> ValidationReport:
    """Doldurulmuş (veya kısmen doldurulmuş) bir şablon metnini denetler.

    Her zorunlu alan (8.2) için üç şeyi kontrol eder: alan etiketi metinde hiç
    geçmiyor mu (eksik), etiket var ama içerik boş mu (boş), içerikte hâlâ
    [DEĞİŞKEN] biçiminde doldurulmamış bir yer tutucu var mı. `is_ready`, üçünden
    biri bile true olduğunda False döner — yani şablon kabul kriterini (8.2, 8.14)
    henüz karşılamıyor demektir. Bu fonksiyon içeriğin *doğruluğunu* denetlemez,
    yalnızca beş alanın *eksiksiz doldurulduğunu* denetler (bkz. 8.14 — Bağlam
    Eksikliği kavramı ile bu ayrımın kendisi karıştırılmamalıdır).
    """
    fields_found = parse_fields(text)
    field_checks: list[FieldCheck] = []
    missing: list[str] = []
    empty: list[str] = []
    all_variables: list[str] = []

    for name in REQUIRED_FIELDS:
        if name not in fields_found:
            missing.append(name)
            field_checks.append(FieldCheck(name, present=False, is_empty=True, unfilled_variables=()))
            continue
        content = fields_found[name]
        variables = find_variables(content)
        is_empty = content == ""
        if is_empty:
            empty.append(name)
        field_checks.append(FieldCheck(name, present=True, is_empty=is_empty, unfilled_variables=variables))
        all_variables.extend(variables)

    for name in OPTIONAL_FIELDS:
        if name in fields_found:
            content = fields_found[name]
            variables = find_variables(content)
            field_checks.append(
                FieldCheck(name, present=True, is_empty=content == "", unfilled_variables=variables)
            )
            all_variables.extend(variables)

    is_ready = not missing and not empty and not all_variables
    return ValidationReport(
        template_name=template_name,
        fields=tuple(field_checks),
        missing_fields=tuple(missing),
        empty_fields=tuple(empty),
        unfilled_variables=tuple(all_variables),
        is_ready=is_ready,
    )


def format_report(report: ValidationReport) -> str:
    """`validate_template` çıktısını terminalde okunabilir bir metne çevirir."""
    lines = [f"Şablon: {report.template_name}" if report.template_name else "Şablon"]
    for field in report.fields:
        if not field.present:
            lines.append(f"  - {field.name}: EKSİK (alan hiç yazılmamış)")
            continue
        if field.is_empty:
            lines.append(f"  - {field.name}: BOŞ (etiket var, içerik yok)")
            continue
        if field.unfilled_variables:
            joined = ", ".join(f"[{v}]" for v in field.unfilled_variables)
            lines.append(f"  - {field.name}: doldurulmamış değişken var -> {joined}")
        else:
            lines.append(f"  - {field.name}: tamam")
    lines.append("Sonuç: HAZIR" if report.is_ready else "Sonuç: HAZIR DEĞİL")
    return "\n".join(lines)


# --- Ek C'den örnek persona şablonları (bkz. content/cilt1/ekler/prompt_sablon_kutuphanesi.md) ---

OGRETMEN_TEMPLATE = TemplateExample(
    persona="Öğretmen",
    title="Ders Materyali Sadeleştirme",
    template=(
        "Amaç: [konu] hakkındaki bu metni [sınıf seviyesi] öğrencisinin anlayacağı dile "
        "indirge. Hedef kitle: [yaş grubu], [ön bilgi düzeyi]. Kaynak: yalnızca "
        "[orijinal_metin]. Format: beş paragraf, her paragrafta tek bir alt kavram, "
        "paragraf sonunda tek soruluk bir anlama kontrolü. Sınır: [orijinal_metin] "
        "dışından bilgi ekleme, teknik terimi tamamen kaldırma yerine parantez içinde "
        "bir cümlelik açıklama ekle."
    ),
)

ANALIST_TEMPLATE = TemplateExample(
    persona="Analist",
    title="Veri Yorumu ve Varsayım Listesi",
    template=(
        'Amaç: [veri_dosyasi] içindeki eğilimi özetleyen bir yorum hazırla. Hedef '
        "kitle: sayısal ayrıntıdan çok sonuca bakan karar vericiler. Kaynak: yalnızca "
        '[veri_dosyasi]. Format: kısa bir yorum paragrafı + üç maddelik bulgu listesi + '
        'ayrı bir "Varsayımlar" listesi. Sınır: veri dışında sayı üretme, veride '
        "olmayan bir kategori veya dönem adı verme."
    ),
)

GELISTIRICI_TEMPLATE = TemplateExample(
    persona="Geliştirici",
    title="Hata Açıklatma",
    template=(
        "Amaç: [hata_mesaji_ve_stack_trace] içindeki hatanın olası nedenini açıkla. "
        "Hedef kitle: kodu yazan geliştirici (sen). Kaynak: yalnızca "
        "[hata_mesaji_ve_stack_trace] ve [ilgili_kod_parcasi]. Format: önce olası "
        "neden (tek paragraf), sonra doğrulanacak iki hipotez, sonra önerilen ilk "
        'adım. Sınır: doğrudan "düzelt" deme, kesin teşhis koymadan önce hangi ek '
        "bilginin (log, ortam, sürüm) gerektiğini belirt."
    ),
)

EXAMPLES: tuple[TemplateExample, ...] = (OGRETMEN_TEMPLATE, ANALIST_TEMPLATE, GELISTIRICI_TEMPLATE)


# --- Aynı üç persona için kullanıcının doldurduğu iki sürüm: eksikli ve tam ---

OGRETMEN_EKSIK_DOLU = (
    "Amaç: hücre bölünmesi hakkındaki bu metni 7. sınıf öğrencisinin anlayacağı dile "
    "indirge. Hedef kitle: [yaş grubu], ön bilgiye sahip olmayan öğrenciler. Kaynak: "
    "yalnızca fen bilimleri ders kitabı 3. ünite metni. Format: beş paragraf, her "
    "paragrafta tek bir alt kavram, paragraf sonunda tek soruluk bir anlama kontrolü. "
    "Sınır:"
)

OGRETMEN_TAM_DOLU = (
    "Amaç: hücre bölünmesi hakkındaki bu metni 7. sınıf öğrencisinin anlayacağı dile "
    "indirge. Hedef kitle: 12-13 yaş, ön bilgiye sahip olmayan öğrenciler. Kaynak: "
    "yalnızca fen bilimleri ders kitabı 3. ünite metni. Format: beş paragraf, her "
    "paragrafta tek bir alt kavram, paragraf sonunda tek soruluk bir anlama kontrolü. "
    "Sınır: ders kitabı 3. ünite metni dışından bilgi ekleme, teknik terimi tamamen "
    "kaldırma yerine parantez içinde bir cümlelik açıklama ekle."
)

ANALIST_EKSIK_DOLU = (
    "Amaç: üçüncü çeyrek bağış verisindeki eğilimi özetleyen bir yorum hazırla. Hedef "
    "kitle: sayısal ayrıntıdan çok sonuca bakan karar vericiler. Kaynak: yalnızca "
    '[veri_dosyasi]. Format: kısa bir yorum paragrafı + üç maddelik bulgu listesi + '
    'ayrı bir "Varsayımlar" listesi.'
)

ANALIST_TAM_DOLU = (
    "Amaç: üçüncü çeyrek bağış verisindeki eğilimi özetleyen bir yorum hazırla. Hedef "
    "kitle: sayısal ayrıntıdan çok sonuca bakan karar vericiler. Kaynak: yalnızca ekli "
    'bağış_2026_q3.csv dosyası. Format: kısa bir yorum paragrafı + üç maddelik bulgu '
    'listesi + ayrı bir "Varsayımlar" listesi. Sınır: veri dışında sayı üretme, veride '
    "olmayan bir kategori veya dönem adı verme."
)

GELISTIRICI_EKSIK_DOLU = (
    "Amaç: KeyError: 'kanal' hatasının olası nedenini açıkla. Hedef kitle: kodu yazan "
    "geliştirici (sen). Kaynak: yalnızca hata mesajı metni ve [ilgili_kod_parcasi]. "
    "Format: önce olası neden (tek paragraf), sonra doğrulanacak iki hipotez, sonra "
    "önerilen ilk adım. Sınır:"
)

GELISTIRICI_TAM_DOLU = (
    "Amaç: KeyError: 'kanal' hatasının olası nedenini açıkla. Hedef kitle: kodu yazan "
    "geliştirici (sen). Kaynak: yalnızca hata mesajı metni ve etiketleme betiğinin "
    "ilgili satırları. Format: önce olası neden (tek paragraf), sonra doğrulanacak iki "
    'hipotez, sonra önerilen ilk adım. Sınır: doğrudan "düzelt" deme, kesin teşhis '
    "koymadan önce hangi ek bilginin (log, ortam, sürüm) gerektiğini belirt."
)


def demo() -> None:
    scenarios = (
        ("Öğretmen — eksik dolu", OGRETMEN_EKSIK_DOLU),
        ("Öğretmen — tam dolu", OGRETMEN_TAM_DOLU),
        ("Analist — eksik dolu", ANALIST_EKSIK_DOLU),
        ("Analist — tam dolu", ANALIST_TAM_DOLU),
        ("Geliştirici — eksik dolu", GELISTIRICI_EKSIK_DOLU),
        ("Geliştirici — tam dolu", GELISTIRICI_TAM_DOLU),
    )
    for name, text in scenarios:
        report = validate_template(text, template_name=name)
        print(format_report(report))
        print()


if __name__ == "__main__":
    demo()
