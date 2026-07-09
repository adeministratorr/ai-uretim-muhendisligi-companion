"""Cilt 1 Bölüm 4 için talep sınıflandırma laboratuvarı.

Gerçek model çağrısı yapmaz. Zero-shot, one-shot ve few-shot promptları kurar;
few-shot sürümde karşı örnek çifti ve JSON şeması kullanır. Çıktıyı yerel bir
doğrulama adımıyla denetler.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any


CATEGORIES = ("İade", "Teknik Sorun", "Fatura", "Genel Bilgi")
URGENCY_LEVELS = ("Acil", "Normal", "Düşük")
REQUIRED_FIELDS = ("kategori", "aciliyet", "ozet", "onerilen_ilk_cumle")
APOLOGY_WORDS = ("özür", "üzgünüz", "kusura bakmayın")


@dataclass(frozen=True)
class TicketExample:
    request: str
    category: str
    urgency: str
    note: str = ""

    def format(self, label: str) -> str:
        note = f" Not: {self.note}" if self.note else ""
        return (
            f"{label} — Talep: {self.request}\n"
            f"Etiket: Kategori: {self.category}, Aciliyet: {self.urgency}.{note}"
        )


DEFAULT_EXAMPLES = (
    TicketExample(
        "Kargom 10 gündür yerinde sayıyor, ne zaman gelecek bilmiyorum.",
        "Teknik Sorun",
        "Normal",
    ),
    TicketExample(
        "Hesabımdan iki kez para çekilmiş, acilen iade istiyorum.",
        "Fatura",
        "Acil",
    ),
    TicketExample(
        "Ürünü beğenmedim, iade koşullarını öğrenmek istiyorum.",
        "İade",
        "Düşük",
    ),
    TicketExample(
        "Uygulama ödeme ekranında hata veriyor, sipariş tamamlanmıyor.",
        "Teknik Sorun",
        "Acil",
    ),
    TicketExample(
        "Mağazanız hafta sonu açık mı?",
        "Genel Bilgi",
        "Düşük",
    ),
)

CONTRAST_EXAMPLES = (
    TicketExample(
        "Param ne zaman iade edilecek?",
        "Fatura",
        "Normal",
        "Başlamış ödeme/iade sürecinin durumunu soruyor.",
    ),
    TicketExample(
        "Ürünü iade etmek istiyorum, süreç nasıl işliyor?",
        "İade",
        "Düşük",
        "Yeni iade talebi başlatıyor.",
    ),
)


def schema_instruction() -> str:
    categories = ", ".join(CATEGORIES)
    urgencies = ", ".join(URGENCY_LEVELS)
    return (
        "Çıktı yalnızca tek satırlık JSON nesnesi olsun. "
        f"kategori alanı şu değerlerden biri olmalı: {categories}. "
        f"aciliyet alanı şu değerlerden biri olmalı: {urgencies}. "
        "ozet en fazla 20 kelime olsun. onerilen_ilk_cumle, sorunu doğrudan "
        "çözüme bağlayan tek cümle olsun; özür kalıbı kullanma."
    )


def build_zero_shot_prompt(ticket: str) -> str:
    return f"Aşağıdaki müşteri destek talebini kategori ve aciliyete göre etiketle: {ticket}"


def build_one_shot_prompt(ticket: str, example: TicketExample = DEFAULT_EXAMPLES[0]) -> str:
    return "\n".join(
        [
            "Aşağıdaki müşteri destek talebini örnekteki biçimde etiketle.",
            example.format("Örnek"),
            f"Şimdi bu talebi etiketle: {ticket}",
        ]
    )


def build_few_shot_prompt(
    ticket: str,
    examples: tuple[TicketExample, ...] = DEFAULT_EXAMPLES,
    contrast_examples: tuple[TicketExample, ...] = CONTRAST_EXAMPLES,
) -> str:
    example_lines = [
        example.format(f"Örnek {index}") for index, example in enumerate(examples, 1)
    ]
    contrast_lines = [
        example.format(f"Karşı örnek {index}")
        for index, example in enumerate(contrast_examples, 1)
    ]
    return "\n".join(
        [
            "Bir e-ticaret müşteri destek ekibi için talep sınıflandırma asistanısın.",
            "Talep birden fazla konu içeriyorsa baskın konuyu esas al.",
            schema_instruction(),
            "",
            *example_lines,
            "",
            *contrast_lines,
            "",
            f"Şimdi bu yeni talebi aynı biçimde etiketle: {ticket}",
        ]
    )


def contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return any(marker in text for marker in markers)


def choose_category(ticket: str) -> str:
    text = ticket.lower()
    if contains_any(
        text, ("iki kez", "mükerrer", "tahsil", "para çek", "param", "ödeme", "fatura")
    ):
        return "Fatura"
    if contains_any(text, ("iade", "değişim", "yanlış ürün", "kırık", "beğenmedim")):
        return "İade"
    if contains_any(text, ("kargo", "gelmedi", "hata", "uygulama", "çalışmıyor", "bozuk")):
        return "Teknik Sorun"
    return "Genel Bilgi"


def choose_urgency(ticket: str) -> str:
    text = ticket.lower()
    if contains_any(text, ("acil", "hemen", "iki kez", "mükerrer", "para çek", "hesabımdan")):
        return "Acil"
    if contains_any(text, ("öğrenmek", "bilgi", "koşul", "hafta sonu", "açık mı")):
        return "Düşük"
    return "Normal"


def summary_for(category: str) -> str:
    summaries = {
        "İade": "Müşteri iade veya değişim sürecinin başlatılmasını istiyor.",
        "Teknik Sorun": "Müşteri teslimat veya teknik sorun için destek istiyor.",
        "Fatura": "Müşteri ödeme veya iade sürecindeki durumu sorguluyor.",
        "Genel Bilgi": "Müşteri genel bilgi talep ediyor.",
    }
    return summaries[category]


def opening_for(category: str, urgency: str) -> str:
    if urgency == "Acil":
        return "Talebinizi hemen inceliyor ve çözüm adımlarını başlatıyoruz."
    openings = {
        "İade": "İade süreci için gerekli adımları hemen kontrol ediyoruz.",
        "Teknik Sorun": "Teslimat veya teknik sorun için gerekli kontrolü başlatıyoruz.",
        "Fatura": "Ödeme sürecinizi kontrol edip net durumu paylaşacağız.",
        "Genel Bilgi": "Talep ettiğiniz bilgiyi net biçimde paylaşacağız.",
    }
    return openings[category]


def classify_ticket_locally(ticket: str) -> dict[str, str]:
    category = choose_category(ticket)
    urgency = choose_urgency(ticket)
    return {
        "kategori": category,
        "aciliyet": urgency,
        "ozet": summary_for(category),
        "onerilen_ilk_cumle": opening_for(category, urgency),
    }


def parse_json_object(text: str) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Çıktı tek bir JSON nesnesi olmalıdır") from exc
    if not isinstance(payload, dict):
        raise ValueError("Çıktı JSON nesnesi olmalıdır")
    return payload


def validate_ticket_output(payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return ["Çıktı JSON nesnesi olmalıdır."]

    errors: list[str] = []
    keys = set(payload)
    required = set(REQUIRED_FIELDS)
    missing = sorted(required - keys)
    extra = sorted(keys - required)
    if missing:
        errors.append("Eksik alan: " + ", ".join(missing))
    if extra:
        errors.append("Beklenmeyen alan: " + ", ".join(extra))

    category = payload.get("kategori")
    urgency = payload.get("aciliyet")
    summary = payload.get("ozet")
    opening = payload.get("onerilen_ilk_cumle")

    if category not in CATEGORIES:
        errors.append("kategori alanı izin verilen değerlerden biri olmalıdır.")
    if urgency not in URGENCY_LEVELS:
        errors.append("aciliyet alanı izin verilen değerlerden biri olmalıdır.")
    if not isinstance(summary, str) or not summary.strip():
        errors.append("ozet alanı boş olmayan metin olmalıdır.")
    elif len(summary.split()) > 20:
        errors.append("ozet alanı en fazla 20 kelime olmalıdır.")
    if not isinstance(opening, str) or not opening.strip():
        errors.append("onerilen_ilk_cumle alanı boş olmayan metin olmalıdır.")
    elif contains_any(opening.lower(), APOLOGY_WORDS):
        errors.append("onerilen_ilk_cumle özür kalıbı içermemelidir.")

    return errors


def to_json_line(payload: dict[str, str]) -> str:
    return json.dumps(payload, ensure_ascii=False)


def demo() -> None:
    ticket = (
        "Kargom gelmedi, ayrıca yanlış ürün gönderilmiş, "
        "hem iade hem yeni gönderim istiyorum."
    )
    prompts = (
        ("Zero-shot", build_zero_shot_prompt(ticket)),
        ("One-shot", build_one_shot_prompt(ticket)),
        ("Few-shot + şema", build_few_shot_prompt(ticket)),
    )
    for name, prompt in prompts:
        print(f"== {name} ==")
        print(f"Satır sayısı: {len(prompt.splitlines())}")
        print()

    payload = classify_ticket_locally(ticket)
    errors = validate_ticket_output(payload)
    print("== Şema çıktısı ==")
    print(to_json_line(payload))
    print("Doğrulama:", "geçti" if not errors else "; ".join(errors))


if __name__ == "__main__":
    demo()
