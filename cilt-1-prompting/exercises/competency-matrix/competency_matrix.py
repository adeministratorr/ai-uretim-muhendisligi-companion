"""Bölüm 16 için ekip yetkinlik matrisi ve kurum çapında prompt kütüphanesi kayıt denetleyicisi.

Kitap bağlantısı: Cilt 1, Bölüm 16 (AI Odaklı Kültür), özellikle 16.2-16.4
(rol bazlı yetkinlik haritası, beş rol ailesi için beceri setleri, kurum çapında
prompt kütüphanesi).

Gerçek API çağrısı yapmaz. İki bağımsız denetim sunar:

- `evaluate_team`: ekip üyesi x yetkinlik alanı ızgarasını tarar, hiç kimsenin hedef
  seviyeye ulaşmadığı BOŞLUKLARI ve yalnızca tek kişinin karşıladığı TEK NOKTA
  RİSKLERİNİ (bkz. 16.7'deki iç şampiyon fikri — tek kişiye bağımlılık) bulur.
- `validate_library_entry`: kurum çapında prompt kütüphanesi kaydının (16.4) başlık,
  sahip, kullanım alanı ve son doğrulama tarihi zorunlu alanlarını, ve son doğrulama
  tarihinin güncelliğini (16.5'teki yıllık gözden geçirme ilkesiyle tutarlı) denetler.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence


BASE_DIR = Path(__file__).resolve().parent

# 16.1'deki dört AI okuryazarlığı seviyesi, düşükten yükseğe.
LEVELS = (
    "farkındalık",
    "temel_kullanım",
    "eleştirel_değerlendirme",
    "sistematik_entegrasyon",
)

# 16.3'teki beş rol ailesinin "temel AI becerisi" ve "hedef okuryazarlık seviyesi"
# sütunlarından türetilmiş yetkinlik alanları. Alanlar rollere değil, becerilere
# bağlıdır: bir ekip üyesi kendi rolünün dışındaki bir alanda da değerlendirilebilir.
COMPETENCY_AREAS: dict[str, dict[str, str]] = {
    "ders_materyali_hazirlama": {
        "etiket": "Ders materyali ve etkinlik hazırlama",
        "hedef_seviye": "eleştirel_değerlendirme",
    },
    "rapor_ve_yazisma": {
        "etiket": "Rapor, yazışma ve veli iletişimi",
        "hedef_seviye": "eleştirel_değerlendirme",
    },
    "veri_yorumu_ve_dogrulama": {
        "etiket": "Veri yorumu ve doğrulama disiplini",
        "hedef_seviye": "eleştirel_değerlendirme",
    },
    "arac_secimi_ve_entegrasyon": {
        "etiket": "Model/araç seçimi ve entegrasyon",
        "hedef_seviye": "sistematik_entegrasyon",
    },
    "standart_yazisma_ve_form": {
        "etiket": "Standart yazışma, form ve özet metni üretme",
        "hedef_seviye": "temel_kullanım",
    },
}

# 16.4'teki kurum çapında prompt kütüphanesi kaydının zorunlu alanları.
REQUIRED_LIBRARY_FIELDS = ("baslik", "sahip", "kullanim_alani", "son_dogrulama_tarihi")

# 16.5'teki "politika sürümlenir, komite yılda bir gözden geçirir" ilkesiyle tutarlı
# güncellik penceresi.
STALE_AFTER_DAYS = 365

# Bu laboratuvarın demo çıktısında kullandığı sabit referans tarih. Gerçek kullanımda
# `--today` bayrağıyla o günün tarihini geçebilirsiniz (bkz. Riskler ve Sınırlar).
DEFAULT_REFERENCE_DATE = date(2026, 7, 1)


def level_rank(level: str) -> int:
    """Bir okuryazarlık seviyesinin 0 (farkındalık) ile 3 (sistematik entegrasyon)
    arasındaki sırasını döndürür. Bilinmeyen seviye adında ValueError fırlatır."""
    try:
        return LEVELS.index(level)
    except ValueError as exc:
        raise ValueError(
            f"Bilinmeyen okuryazarlık seviyesi: {level!r}. Geçerli seviyeler: {LEVELS}"
        ) from exc


def load_json(path: str | Path) -> Any:
    with Path(path).open(encoding="utf-8") as file:
        return json.load(file)


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return BASE_DIR / candidate


def has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


# --------------------------------------------------------------------------- #
# Ekip yetkinlik matrisi
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class GapReport:
    """Tek bir yetkinlik alanı için ekip çapında denetim sonucu."""

    area: str
    etiket: str
    hedef_seviye: str
    en_yuksek_seviye: str | None
    yeterli_kisiler: tuple[str, ...]
    durum: str  # "boşluk" | "tek_nokta_riski" | "yeterli"

    @property
    def is_gap(self) -> bool:
        return self.durum == "boşluk"

    @property
    def is_single_point_risk(self) -> bool:
        return self.durum == "tek_nokta_riski"


def evaluate_team(team: Sequence[Mapping[str, Any]]) -> tuple[GapReport, ...]:
    """Ekip üyesi x yetkinlik alanı ızgarasını her alan için tarar.

    Her ekip üyesi ``{"ad": str, "rol": str, "seviyeler": {alan: seviye}}`` biçiminde
    olmalıdır; ``seviyeler`` içinde değerlendirilmeyen bir alan basitçe atlanabilir.
    Her `COMPETENCY_AREAS` alanı için hiç kimsenin hedef seviyeye ulaşmadığı bir
    "boşluk", yalnızca bir kişinin ulaştığı bir "tek nokta riski" veya en az iki
    kişinin ulaştığı "yeterli" durumu üretir.
    """
    reports: list[GapReport] = []
    for area, info in COMPETENCY_AREAS.items():
        hedef_seviye = info["hedef_seviye"]
        hedef_rank = level_rank(hedef_seviye)

        en_yuksek_rank = -1
        yeterli_kisiler: list[str] = []
        for member in team:
            seviyeler = member.get("seviyeler", {})
            seviye = seviyeler.get(area)
            if not seviye:
                continue
            rank = level_rank(seviye)
            en_yuksek_rank = max(en_yuksek_rank, rank)
            if rank >= hedef_rank:
                yeterli_kisiler.append(member.get("ad") or "İsimsiz")

        if not yeterli_kisiler:
            durum = "boşluk"
        elif len(yeterli_kisiler) == 1:
            durum = "tek_nokta_riski"
        else:
            durum = "yeterli"

        reports.append(
            GapReport(
                area=area,
                etiket=info["etiket"],
                hedef_seviye=hedef_seviye,
                en_yuksek_seviye=LEVELS[en_yuksek_rank] if en_yuksek_rank >= 0 else None,
                yeterli_kisiler=tuple(yeterli_kisiler),
                durum=durum,
            )
        )
    return tuple(reports)


def format_gap_reports(reports: Sequence[GapReport]) -> str:
    lines = []
    for report in reports:
        if report.durum == "boşluk":
            lines.append(
                f"BOŞLUK — {report.etiket}: hedef '{report.hedef_seviye}', "
                "ekipte hiç kimse bu seviyeye ulaşmıyor."
            )
        elif report.durum == "tek_nokta_riski":
            lines.append(
                f"TEK NOKTA RİSKİ — {report.etiket}: yalnızca "
                f"{report.yeterli_kisiler[0]} hedefi karşılıyor."
            )
        else:
            lines.append(
                f"YETERLİ — {report.etiket}: {len(report.yeterli_kisiler)} kişi "
                "hedefi karşılıyor."
            )
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Kurum çapında prompt kütüphanesi kaydı denetimi
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class LibraryCheck:
    """Tek bir prompt kütüphanesi kaydı için denetim sonucu."""

    baslik: str
    status: str  # "geçti" | "revizyon gerekli"
    issues: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.issues


def validate_library_entry(
    entry: Mapping[str, Any], reference_date: date | None = None
) -> LibraryCheck:
    """16.4'teki kurum çapında kayıt biçiminin zorunlu alanlarını denetler.

    Zorunlu alanlar: `baslik`, `sahip`, `kullanim_alani`, `son_dogrulama_tarihi`
    (bkz. `REQUIRED_LIBRARY_FIELDS`). `son_dogrulama_tarihi` ayrıca YYYY-AA-GG
    biçiminde geçerli bir tarih olmalı ve `reference_date`'e göre
    `STALE_AFTER_DAYS` günden eski olmamalıdır (16.5'teki yıllık gözden geçirme
    ilkesi).
    """
    reference = reference_date or DEFAULT_REFERENCE_DATE
    issues: list[str] = []

    for field in REQUIRED_LIBRARY_FIELDS:
        if not has_text(entry.get(field)):
            issues.append(f"`{field}` alanı boş bırakılmamalıdır.")

    tarih_metni = entry.get("son_dogrulama_tarihi")
    if has_text(tarih_metni):
        try:
            tarih = date.fromisoformat(tarih_metni.strip())
        except ValueError:
            issues.append(
                "`son_dogrulama_tarihi` YYYY-AA-GG biçiminde geçerli bir tarih olmalıdır."
            )
        else:
            if (reference - tarih).days > STALE_AFTER_DAYS:
                issues.append(
                    f"`son_dogrulama_tarihi` {STALE_AFTER_DAYS} günden eski; "
                    "yıllık gözden geçirmeden geçmemiş olabilir."
                )

    baslik = entry.get("baslik") if has_text(entry.get("baslik")) else "(başlıksız kayıt)"
    status = "geçti" if not issues else "revizyon gerekli"
    return LibraryCheck(baslik=baslik, status=status, issues=tuple(issues))


def validate_library(
    entries: Sequence[Mapping[str, Any]], reference_date: date | None = None
) -> tuple[LibraryCheck, ...]:
    return tuple(validate_library_entry(entry, reference_date) for entry in entries)


def format_library_checks(checks: Sequence[LibraryCheck]) -> str:
    lines = []
    for check in checks:
        lines.append(f"[{check.status}] {check.baslik}")
        lines.extend(f"  - {issue}" for issue in check.issues)
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Komut satırı
# --------------------------------------------------------------------------- #


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bölüm 16 ekip yetkinlik matrisi ve prompt kütüphanesi kaydı denetleyicisi"
    )
    parser.add_argument("team_file", nargs="?", default="example_team.json")
    parser.add_argument("--library", default="example_library.json")
    parser.add_argument(
        "--today",
        default=DEFAULT_REFERENCE_DATE.isoformat(),
        help="Referans tarih (YYYY-AA-GG); son_dogrulama_tarihi güncelliği buna göre ölçülür.",
    )
    args = parser.parse_args(argv)

    reference_date = date.fromisoformat(args.today)
    team = load_json(resolve_path(args.team_file))
    library = load_json(resolve_path(args.library))

    reports = evaluate_team(team)
    checks = validate_library(library, reference_date)

    print("Ekip Yetkinlik Matrisi:")
    print(format_gap_reports(reports))
    print()
    print("Prompt Kütüphanesi Kayıtları:")
    print(format_library_checks(checks))

    gap_count = sum(1 for report in reports if report.is_gap)
    failed_count = sum(1 for check in checks if not check.passed)
    return 0 if gap_count == 0 and failed_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
