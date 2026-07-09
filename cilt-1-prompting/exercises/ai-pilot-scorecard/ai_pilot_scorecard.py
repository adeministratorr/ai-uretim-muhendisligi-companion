"""Bölüm 15 için yapay zekâ pilotu ölçüm kartı.

Kitap bağlantısı: Cilt 1, Bölüm 15 (Yapay Zekâ Öncüsü Şirketlerden Dersler),
özellikle 15.1, 15.8, 15.9 ve 15.10.

Gerçek API çağrısı yapmaz. Doldurulmuş bir pilot tasarımını beş alan, dört ölçüt,
veri riski ve geri çekilme eşiği açısından denetler.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


BASE_DIR = Path(__file__).resolve().parent

MAIN_FIELDS = (
    "hedef",
    "kullanici_grubu",
    "veri_riski",
    "basari_metrikleri",
    "pilot_sonrasi_karar_kriteri",
)

METRIC_FIELDS = ("zaman_kazanci", "kalite", "maliyet", "risk_azalmasi")

MEASUREMENT_HINTS = (
    "%",
    "yüzde",
    "dakika",
    "saat",
    "gün",
    "ay",
    "çeyrek",
    "adet",
    "sayı",
    "oran",
    "tl",
    "maliyet",
    "süre",
    "alt",
    "üst",
    "başına",
)

SENSITIVE_DATA_HINTS = (
    "kişisel",
    "banka",
    "iban",
    "sağlık",
    "öğrenci",
    "kaynak kodu",
    "mali",
    "finansal",
    "müşteri",
)

CONTROL_HINTS = (
    "kurumsal onaylı",
    "onaylı araç",
    "insan kontrol",
    "insan denetim",
    "uzman kontrol",
    "model eğitiminde kullanılmadığı",
    "maskele",
    "anonim",
)

DECISION_ACTIONS = ("genişlet", "daralt", "durdur", "geri çek", "insan kontrol", "onay")


@dataclass(frozen=True)
class Scorecard:
    status: str
    completed_checks: int
    total_checks: int
    issues: tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.issues


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


def normalized(value: str) -> str:
    return value.casefold()


def has_any(text: str, hints: Sequence[str]) -> bool:
    lowered = normalized(text)
    return any(hint in lowered for hint in hints)


def is_measurable(text: str) -> bool:
    return any(char.isdigit() for char in text) or has_any(text, MEASUREMENT_HINTS)


def evaluate_pilot(pilot: Mapping[str, Any]) -> Scorecard:
    issues: list[str] = []
    completed_checks = 0
    total_checks = 5 + len(METRIC_FIELDS)

    for field in MAIN_FIELDS:
        if field == "basari_metrikleri":
            continue
        if has_text(pilot.get(field)):
            completed_checks += 1
        else:
            issues.append(f"`{field}` alanı boş bırakılmamalıdır.")

    hedef = pilot.get("hedef")
    if has_text(hedef) and not is_measurable(hedef):
        issues.append("`hedef` ölçülebilir bir süre, oran, eşik veya birim içermelidir.")

    veri_riski = pilot.get("veri_riski")
    if has_text(veri_riski) and has_any(veri_riski, SENSITIVE_DATA_HINTS):
        if not has_any(veri_riski, CONTROL_HINTS):
            issues.append("`veri_riski` hassas veri içeriyor; onaylı araç veya insan kontrolü yazılmalıdır.")

    metrics = pilot.get("basari_metrikleri")
    if not isinstance(metrics, Mapping):
        issues.append("`basari_metrikleri` dört ölçütü taşıyan bir nesne olmalıdır.")
    else:
        completed_checks += 1
        for metric in METRIC_FIELDS:
            value = metrics.get(metric)
            if has_text(value):
                completed_checks += 1
                if not is_measurable(value):
                    issues.append(f"`basari_metrikleri.{metric}` ölçülebilir bir gösterge içermelidir.")
            else:
                issues.append(f"`basari_metrikleri.{metric}` boş bırakılmamalıdır.")

    karar = pilot.get("pilot_sonrasi_karar_kriteri")
    if has_text(karar):
        action_count = sum(1 for action in DECISION_ACTIONS if action in normalized(karar))
        if action_count < 2:
            issues.append("`pilot_sonrasi_karar_kriteri` en az iki karar yolu içermelidir.")
        if not is_measurable(karar):
            issues.append("`pilot_sonrasi_karar_kriteri` ölçülebilir bir eşik içermelidir.")

    status = "geçti" if not issues else "revizyon gerekli"
    return Scorecard(
        status=status,
        completed_checks=completed_checks,
        total_checks=total_checks,
        issues=tuple(issues),
    )


def summarize_cases(cases: Sequence[Mapping[str, Any]]) -> str:
    waiting = sum(1 for case in cases if case.get("dogrulama_durumu") != "doğrulandı")
    return f"Vaka satırı: {len(cases)} | Kaynak doğrulaması bekleyen: {waiting}"


def format_scorecard(scorecard: Scorecard) -> str:
    lines = [
        f"Durum: {scorecard.status}",
        f"Tamamlanan kontrol: {scorecard.completed_checks}/{scorecard.total_checks}",
    ]
    if scorecard.passed:
        lines.append("Kabul kriteri geçti: beş alan ve dört ölçüt dolduruldu.")
    else:
        lines.append("Eksikler:")
        lines.extend(f"- {issue}" for issue in scorecard.issues)
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bölüm 15 yapay zekâ pilotu ölçüm kartı")
    parser.add_argument("pilot_file", nargs="?", default="example_pilot.json")
    parser.add_argument("--cases", default="case_table.json")
    args = parser.parse_args(argv)

    cases = load_json(resolve_path(args.cases))
    pilot = load_json(resolve_path(args.pilot_file))
    scorecard = evaluate_pilot(pilot)

    print("Vaka tablosu:", summarize_cases(cases))
    print(format_scorecard(scorecard))
    return 0 if scorecard.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
