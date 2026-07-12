"""Bölüm 10 için etki/efor ve risk/değer değerlendirme şablonu.

Kitap bağlantısı: Cilt 1, Bölüm 10 (Yapay Zekâ ile Günlük Hayat ve İş Akışları),
özellikle 10.12 (Etki/Efor Matrisi), 10.13 (Risk/Değer Matrisi) ve 10.16
(Yapay Zekâ Ne Zaman Kullanılmamalı?).

Gerçek bir API çağrısı yapmaz. Bir görev listesindeki her görevi iki ayrı 2x2
matrise yerleştirir:

- Etki/efor matrisi (10.12): "bunu kurmaya değer mi?" sorusuna cevap verir.
- Risk/değer matrisi (10.13): "bu çıktıya ne kadar güvenilebilir, ne kadar
  denetim gerekir?" sorusuna cevap verir.

İki matris birleştirilerek görevler, önce hangisinin otomatikleştirilmeye uygun
olduğunu gösteren tek bir öncelik sırasına dizilir. Hukuk, sağlık, finans veya
kişisel veri içeren yüksek riskli karar alanları (10.16) puandan bağımsız
olarak ayrı işaretlenir; bu tür görevler puanları iyi çıksa da sona bırakılır.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

BASE_DIR = Path(__file__).resolve().parent

SCALE_MIN = 1
SCALE_MAX = 5
YUKSEK_ESIGI = 3  # 1-5 ölçeğinde bu değer ve üstü "yüksek" sayılır

# (etki düzeyi, efor düzeyi) -> (çeyrek adı, önerilen eylem, çeyrek sırası)
# Kaynak: kitap 10.12 — Etki/Efor Matrisi tablosu.
IMPACT_EFFORT_QUADRANTS: dict[tuple[str, str], tuple[str, str, int]] = {
    ("yüksek", "düşük"): ("hızlı kazanç", "Önce bunlar kurulur", 1),
    ("yüksek", "yüksek"): ("büyük proje", "Planlanır, sıraya alınır", 2),
    ("düşük", "düşük"): ("dolgu işi", "Zaman kalırsa denenir", 3),
    ("düşük", "yüksek"): ("kaçın", "Genellikle ertelenir veya vazgeçilir", 4),
}

# (risk düzeyi, değer düzeyi) -> (çeyrek adı, önerilen eylem, çeyrek sırası)
# Kaynak: kitap 10.13 — Risk/Değer Matrisi tablosu.
RISK_VALUE_QUADRANTS: dict[tuple[str, str], tuple[str, str, int]] = {
    ("düşük", "yüksek"): ("düşük risk / yüksek değer", "Düşük düzeyde insan onayıyla kurulabilir", 1),
    ("düşük", "düşük"): ("düşük risk / düşük değer", "İhtiyaç olursa denenir", 2),
    ("yüksek", "yüksek"): ("yüksek risk / yüksek değer", "Kurulur ama sıkı onay noktası zorunlu", 3),
    ("yüksek", "düşük"): ("yüksek risk / düşük değer", "Muhtemelen kurulmaz", 4),
}

# Birleşik öncelik puanı (iki çeyrek sırasının en kötüsü, 1-4 arası) için kademeler.
PRIORITY_LABELS: dict[int, str] = {
    1: "Öncelik 1 — hemen kurulmaya uygun",
    2: "Öncelik 2 — planlanır, orta düzeyde onayla sıraya alınır",
    3: "Öncelik 3 — dikkatli değerlendirilmeli, sıkı onay veya erteleme düşünülmeli",
    4: "Öncelik 4 — muhtemelen ertelenir veya vazgeçilir",
}

YUKSEK_RISKLI_ALAN_ETIKETI = (
    "Yüksek riskli karar alanı (10.16) — matris puanından bağımsız olarak tam "
    "otomasyon önerilmez; ilgili alanın uzmanı onaylamadan uygulanmaz."
)


def level(value: int, field_name: str = "değer") -> str:
    """1-5 ölçeğindeki bir puanı 'düşük' / 'yüksek' iki düzeyine indirger.

    >>> level(2)
    'düşük'
    >>> level(4)
    'yüksek'
    """
    if not isinstance(value, int) or not SCALE_MIN <= value <= SCALE_MAX:
        raise ValueError(
            f"`{field_name}` {SCALE_MIN}-{SCALE_MAX} aralığında bir tam sayı olmalıdır: {value!r}"
        )
    return "yüksek" if value >= YUKSEK_ESIGI else "düşük"


@dataclass(frozen=True)
class Gorev:
    """Değerlendirilecek tek bir görev/iş akışı adayı.

    Alanlar 1 (en düşük) ile 5 (en yüksek) arasında tam sayıdır:

    - ``etki``: görev otomatikleştirilirse sağlayacağı fayda (zaman, hata, gelir).
    - ``efor``: kurmak/test etmek/öğrenmek için gereken çaba.
    - ``risk``: hata, gizlilik, itibar veya güvenlik riski.
    - ``deger``: çıktının sağladığı değer — ``etki`` ile aynı sayı olabilir ama
      farklı bir soruya cevap verir: etki "kurmaya değer mi", değer "ne kadar
      güvenilir olmalı" sorusunu besler (bkz. kitap 10.13).
    - ``yuksek_riskli_alan``: hukuk, sağlık, finans veya kişisel veri içeren,
      10.16 anlamında uzman onayı olmadan otomatikleştirilmemesi gereken bir
      alansa ``True``.
    """

    ad: str
    etki: int
    efor: int
    risk: int
    deger: int
    yuksek_riskli_alan: bool = False

    def __post_init__(self) -> None:
        if not self.ad.strip():
            raise ValueError("`ad` boş bırakılmamalıdır.")
        level(self.etki, "etki")
        level(self.efor, "efor")
        level(self.risk, "risk")
        level(self.deger, "deger")


@dataclass(frozen=True)
class Degerlendirme:
    """Bir görevin iki matristeki konumu ve birleşik önceliği."""

    gorev: Gorev
    ie_ceyrek: str
    ie_eylem: str
    ie_sira: int
    rv_ceyrek: str
    rv_eylem: str
    rv_sira: int
    oncelik_puani: int
    oncelik_etiketi: str

    @property
    def otomasyona_uygun(self) -> bool:
        """Puan iyi (1 veya 2) ve yüksek riskli alan işaretli değilse uygundur."""
        return self.oncelik_puani <= 2 and not self.gorev.yuksek_riskli_alan


def siniflandir_etki_efor(gorev: Gorev) -> tuple[str, str, int]:
    """Görevi 10.12'deki etki/efor matrisinin dört çeyreğinden birine yerleştirir."""
    return IMPACT_EFFORT_QUADRANTS[(level(gorev.etki, "etki"), level(gorev.efor, "efor"))]


def siniflandir_risk_deger(gorev: Gorev) -> tuple[str, str, int]:
    """Görevi 10.13'teki risk/değer matrisinin dört çeyreğinden birine yerleştirir."""
    return RISK_VALUE_QUADRANTS[(level(gorev.risk, "risk"), level(gorev.deger, "deger"))]


def degerlendir(gorev: Gorev) -> Degerlendirme:
    """Bir görevi iki matriste sınıflandırır ve birleşik öncelik puanı üretir.

    Öncelik puanı, iki çeyrek sırasının en kötüsüdür (``max``): bir görev tek
    eksende iyi görünse bile, öteki eksende "kaçın" veya "muhtemelen kurulmaz"
    çeyreğine düşüyorsa öncelik o kötü eksene göre belirlenir. Bu, kitabın
    10.13'te vurguladığı "aynı iş akışı iki matriste farklı köşeye düşebilir"
    ilkesinin doğrudan sonucudur.
    """
    ie_ceyrek, ie_eylem, ie_sira = siniflandir_etki_efor(gorev)
    rv_ceyrek, rv_eylem, rv_sira = siniflandir_risk_deger(gorev)
    puan = max(ie_sira, rv_sira)
    etiket = YUKSEK_RISKLI_ALAN_ETIKETI if gorev.yuksek_riskli_alan else PRIORITY_LABELS[puan]
    return Degerlendirme(
        gorev=gorev,
        ie_ceyrek=ie_ceyrek,
        ie_eylem=ie_eylem,
        ie_sira=ie_sira,
        rv_ceyrek=rv_ceyrek,
        rv_eylem=rv_eylem,
        rv_sira=rv_sira,
        oncelik_puani=puan,
        oncelik_etiketi=etiket,
    )


def onceliklendir(gorevler: Sequence[Gorev]) -> list[Degerlendirme]:
    """Görev listesini önce otomatikleştirilmeye en uygun olan başa gelecek biçimde sıralar.

    Yüksek riskli karar alanı işaretli görevler puanları ne olursa olsun sona
    bırakılır (bkz. kitap 10.16); geri kalanlar öncelik puanına, eşitlikte iki
    çeyrek sırasının toplamına, yine eşitlikte ada göre sıralanır.
    """
    degerlendirmeler = [degerlendir(gorev) for gorev in gorevler]
    return sorted(
        degerlendirmeler,
        key=lambda d: (
            d.gorev.yuksek_riskli_alan,
            d.oncelik_puani,
            d.ie_sira + d.rv_sira,
            d.gorev.ad,
        ),
    )


def gorev_yukle(veri: dict[str, Any]) -> Gorev:
    return Gorev(
        ad=veri["ad"],
        etki=veri["etki"],
        efor=veri["efor"],
        risk=veri["risk"],
        deger=veri["deger"],
        yuksek_riskli_alan=bool(veri.get("yuksek_riskli_alan", False)),
    )


def json_yukle(yol: str | Path) -> list[Gorev]:
    with Path(yol).open(encoding="utf-8") as dosya:
        veri = json.load(dosya)
    return [gorev_yukle(kayit) for kayit in veri]


def resolve_path(yol: str | Path) -> Path:
    candidate = Path(yol)
    if candidate.is_absolute():
        return candidate
    return BASE_DIR / candidate


def format_rapor(siralanmis: Sequence[Degerlendirme]) -> str:
    """``onceliklendir`` çıktısını okunabilir bir metin raporuna çevirir.

    Sırayı değiştirmez; verilen sırayla numaralandırır.
    """
    if not siralanmis:
        return (
            "Görev listesi boş; gorev_listesi_ornek.json içindeki alanları izleyerek "
            "kendi listenizi gorev_listesi_sablonu.json üzerine kurabilirsiniz."
        )
    satirlar = [f"{len(siralanmis)} görev değerlendirildi.\n"]
    for sira, d in enumerate(siralanmis, start=1):
        satirlar.append(
            f"{sira}. {d.gorev.ad}\n"
            f"   Etki/Efor: {d.ie_ceyrek} → {d.ie_eylem}\n"
            f"   Risk/Değer: {d.rv_ceyrek} → {d.rv_eylem}\n"
            f"   {d.oncelik_etiketi}"
        )
    return "\n".join(satirlar)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bölüm 10 etki/efor ve risk/değer değerlendirme şablonu"
    )
    parser.add_argument("gorev_dosyasi", nargs="?", default="gorev_listesi_ornek.json")
    args = parser.parse_args(argv)

    gorevler = json_yukle(resolve_path(args.gorev_dosyasi))
    siralanmis = onceliklendir(gorevler)
    print(format_rapor(siralanmis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
