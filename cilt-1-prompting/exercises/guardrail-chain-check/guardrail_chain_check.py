"""Bölüm 14 için guardrail zinciri denetimi.

Kitap bağlantısı: Cilt 1, Bölüm 14 (Guardrails ve İnsan Gözetimi), özellikle
14.1 (girdi guardrail -> ajan -> çıktı guardrail zinciri) ve 14.6 (araç risk
sınıflandırma tablosu).

Gerçek bir API çağrısı yapmaz. Bir ajan akışındaki her aracın risk seviyesini
(14.6'daki dört seviye: düşük / orta / yüksek / kritik) okur, bu risk seviyesi
için beklenen guardrail katmanının (girdi denetimi / çıktı doğrulama / insan
onayı) fiilen tanımlı olup olmadığını denetler ve eksik katmanları uyarı
olarak listeler.

Beklenen katman politikası (REQUIRED_LAYERS), 14.6'daki tablo ile 14.1'deki
zincirden ve 14.8'deki insan onay eşiğinden türetilir: risk seviyesi
yükseldikçe beklenen katman sayısı artar; kritik seviyede insan onayı
zorunludur ("Hiçbir otomatik yürütme yok").
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence


BASE_DIR = Path(__file__).resolve().parent


class RiskLevel(str, Enum):
    """14.6'daki araç risk sınıflandırma tablosunun dört seviyesi."""

    DUSUK = "düşük"
    ORTA = "orta"
    YUKSEK = "yüksek"
    KRITIK = "kritik"


class GuardrailLayer(str, Enum):
    """14.1'deki denetim zincirinin katmanları (+ 14.8 insan onay eşiği)."""

    GIRDI_DENETIMI = "girdi denetimi"
    CIKTI_DOGRULAMA = "çıktı doğrulama"
    INSAN_ONAYI = "insan onayı"


# 14.6'daki tablo satırlarından türetilen politika:
# - Düşük (bilgi bankası arama): "Hayır, otomatik" -> yalnızca girdi denetimi.
# - Orta (destek kaydı oluşturma/güncelleme): "otomatik, ama işlem günlüğe
#   kaydedilir" -> girdi denetimi + çıktı doğrulama (günlük kaydı tespit edici
#   bir çıktı kontrolüdür).
# - Yüksek (standart şifre sıfırlama): "otomatik, ama anlık bildirim
#   gönderilir" -> girdi denetimi + çıktı doğrulama.
# - Kritik (yetki yükseltme / yönetici erişimi): "Evet, insan onayı zorunlu"
#   -> üç katmanın tümü, bkz. 14.8.
REQUIRED_LAYERS: dict[RiskLevel, frozenset[GuardrailLayer]] = {
    RiskLevel.DUSUK: frozenset({GuardrailLayer.GIRDI_DENETIMI}),
    RiskLevel.ORTA: frozenset({GuardrailLayer.GIRDI_DENETIMI, GuardrailLayer.CIKTI_DOGRULAMA}),
    RiskLevel.YUKSEK: frozenset({GuardrailLayer.GIRDI_DENETIMI, GuardrailLayer.CIKTI_DOGRULAMA}),
    RiskLevel.KRITIK: frozenset(
        {
            GuardrailLayer.GIRDI_DENETIMI,
            GuardrailLayer.CIKTI_DOGRULAMA,
            GuardrailLayer.INSAN_ONAYI,
        }
    ),
}


@dataclass(frozen=True)
class ToolDefinition:
    """Bir ajan aracının risk seviyesi ve fiilen tanımlı guardrail katmanları."""

    name: str
    risk_level: RiskLevel
    configured_layers: frozenset[GuardrailLayer]
    note: str = ""


@dataclass(frozen=True)
class ToolAuditResult:
    """Tek bir aracın denetim sonucu: gereken katmanlar vs. tanımlı katmanlar."""

    tool_name: str
    risk_level: RiskLevel
    required_layers: frozenset[GuardrailLayer]
    configured_layers: frozenset[GuardrailLayer]
    missing_layers: frozenset[GuardrailLayer]

    @property
    def is_compliant(self) -> bool:
        return not self.missing_layers

    @property
    def is_critical_gap(self) -> bool:
        """Kritik risk seviyesinde insan onayı eksikse, bölüm başındaki sahte
        yetki yükseltme olayıyla (14.1) aynı boşluk türüdür."""
        return self.risk_level == RiskLevel.KRITIK and GuardrailLayer.INSAN_ONAYI in self.missing_layers


@dataclass(frozen=True)
class ChainAuditReport:
    """Bir ajanın tüm araç zincirinin denetim özeti."""

    results: tuple[ToolAuditResult, ...]

    @property
    def is_compliant(self) -> bool:
        return all(result.is_compliant for result in self.results)

    @property
    def compliant_count(self) -> int:
        return sum(1 for result in self.results if result.is_compliant)

    @property
    def critical_gaps(self) -> tuple[ToolAuditResult, ...]:
        return tuple(result for result in self.results if result.is_critical_gap)


def parse_risk_level(value: str) -> RiskLevel:
    normalized = value.strip().casefold()
    for level in RiskLevel:
        if level.value == normalized:
            return level
    raise ValueError(f"Bilinmeyen risk seviyesi: {value!r}")


def parse_guardrail_layer(value: str) -> GuardrailLayer:
    normalized = value.strip().casefold()
    for layer in GuardrailLayer:
        if layer.value == normalized:
            return layer
    raise ValueError(f"Bilinmeyen guardrail katmanı: {value!r}")


def tool_from_dict(data: Mapping[str, Any]) -> ToolDefinition:
    return ToolDefinition(
        name=str(data["name"]),
        risk_level=parse_risk_level(str(data["risk_level"])),
        configured_layers=frozenset(
            parse_guardrail_layer(str(layer)) for layer in data.get("configured_layers", [])
        ),
        note=str(data.get("note", "")),
    )


def resolve_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return BASE_DIR / candidate


def load_tool_chain(path: str | Path) -> tuple[ToolDefinition, ...]:
    with resolve_path(path).open(encoding="utf-8") as file:
        raw = json.load(file)
    return tuple(tool_from_dict(item) for item in raw)


def audit_tool(tool: ToolDefinition) -> ToolAuditResult:
    required = REQUIRED_LAYERS[tool.risk_level]
    missing = required - tool.configured_layers
    return ToolAuditResult(
        tool_name=tool.name,
        risk_level=tool.risk_level,
        required_layers=required,
        configured_layers=tool.configured_layers,
        missing_layers=missing,
    )


def audit_tool_chain(tools: Sequence[ToolDefinition]) -> ChainAuditReport:
    return ChainAuditReport(results=tuple(audit_tool(tool) for tool in tools))


def _layer_label(layers: frozenset[GuardrailLayer]) -> str:
    ordered = [layer.value for layer in GuardrailLayer if layer in layers]
    return ", ".join(ordered) if ordered else "(yok)"


def format_report(report: ChainAuditReport) -> str:
    lines = [
        f"Denetlenen araç: {len(report.results)} | Uyumlu: {report.compliant_count}/{len(report.results)}"
    ]
    for result in report.results:
        status = "UYUMLU" if result.is_compliant else "EKSİK"
        lines.append(
            f"- [{status}] {result.tool_name} (risk: {result.risk_level.value}) "
            f"— gerekli: {_layer_label(result.required_layers)} "
            f"| tanımlı: {_layer_label(result.configured_layers)}"
        )
        for layer in GuardrailLayer:
            if layer in result.missing_layers:
                prefix = (
                    "[YÜKSEK ÖNCELİKLİ]"
                    if result.is_critical_gap and layer == GuardrailLayer.INSAN_ONAYI
                    else "[UYARI]"
                )
                lines.append(f"    {prefix} '{layer.value}' katmanı tanımlı değil.")
    if report.critical_gaps:
        names = ", ".join(result.tool_name for result in report.critical_gaps)
        lines.append(
            f"Kritik boşluk: {names} — bölüm başındaki sahte yetki yükseltme olayıyla aynı desen "
            "(kritik risk seviyesinde otomatik yürütme, insan onayı yok)."
        )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bölüm 14 guardrail zinciri denetimi")
    parser.add_argument("chain_file", nargs="?", default="example_incident.json")
    args = parser.parse_args(argv)

    tools = load_tool_chain(args.chain_file)
    report = audit_tool_chain(tools)
    print(format_report(report))
    return 0 if report.is_compliant else 1


if __name__ == "__main__":
    raise SystemExit(main())
