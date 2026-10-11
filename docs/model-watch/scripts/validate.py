#!/usr/bin/env python3
"""Model Watch yerel JSON yapisi ve goreli Markdown baglanti kontrolu.

Harici paket ve internet baglantisi gerektirmez.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
ALLOWED_STATUS = {"ga", "preview", "listed", "released", "watch"}
ALLOWED_DIST = {"api", "weights", "api_and_weights", "unknown"}
ALLOWED_EVIDENCE = {"R1", "R2", "R3", "R4", "B", "T"}
MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def main() -> int:
    errors: list[str] = []
    data_path = BASE / "data" / "models.json"
    try:
        data = json.loads(data_path.read_text(encoding="utf-8"))
        date.fromisoformat(data["last_verified"])
        if data["schema_version"] != "1.0":
            errors.append("schema_version 1.0 olmali")
        models = data["models"]
    except (OSError, KeyError, ValueError, TypeError) as exc:
        print(f"Gecersiz model verisi: {exc}", file=sys.stderr)
        return 1

    seen: set[tuple[str, str]] = set()
    for index, model in enumerate(models):
        for key in ("provider", "family", "name", "status", "distribution", "evidence", "source"):
            if not isinstance(model.get(key), str) or not model[key].strip():
                errors.append(f"models[{index}].{key} bos/gecersiz")
        if model.get("status") not in ALLOWED_STATUS:
            errors.append(f"models[{index}] bilinmeyen status")
        if model.get("distribution") not in ALLOWED_DIST:
            errors.append(f"models[{index}] bilinmeyen distribution")
        if model.get("evidence") not in ALLOWED_EVIDENCE:
            errors.append(f"models[{index}] bilinmeyen evidence")
        if not str(model.get("source", "")).startswith("https://"):
            errors.append(f"models[{index}] HTTPS kaynak bekleniyor")
        mid = model.get("model_id")
        if mid is not None and (not isinstance(mid, str) or not mid.strip()):
            errors.append(f"models[{index}].model_id gecersiz")
        identity = (str(model.get("provider")), str(model.get("name")))
        if identity in seen:
            errors.append(f"Tekrarlanan model: {identity}")
        seen.add(identity)

    checked = 0
    skipped_root_links = 0
    for file in sorted(BASE.rglob("*.md")):
        content = file.read_text(encoding="utf-8")
        for target in MD_LINK.findall(content):
            target = target.strip().split("#", 1)[0].strip()
            if not target or target.startswith(("https://", "http://", "mailto:")):
                continue
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            checked += 1
            linked = (file.parent / unquote(target)).resolve()
            if not linked.is_relative_to(REPO):
                errors.append(f"Baglanti repo disina cikiyor: {file}: {target}")
            elif not linked.exists():
                # Paket, depo kokundeki mevcut AGENTS / CONTRIBUTING dosyalarini tasimaz.
                if linked.parent == REPO and linked.name in {"AGENTS.md", "CONTRIBUTING.md"}:
                    skipped_root_links += 1
                else:
                    errors.append(f"Kirık yerel baglanti: {file.relative_to(BASE)} -> {target}")

    if errors:
        for error in errors:
            print("HATA:", error, file=sys.stderr)
        return 1
    print(f"OK: {len(models)} model kaydi, {checked} goreli Markdown baglantisi kontrol edildi.")
    if skipped_root_links:
        print(f"NOT: Paket disindaki repo kokune giden {skipped_root_links} baglanti, asil depoda kontrol edilmeli.")
    print("Dis baglantilar, API cagirilari, fiyat ve lisans metinleri bu komutla dogrulanmaz.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
