"""Bir proje güvenlik sözleşmesini Bölüm 14'ün kabul ölçütleriyle doğrular.

volume: 2
chapter: 14
book_section: "14.2-14.13 Güvenlik Sözleşmesi"
concepts:
  - veri sınıflandırması
  - secret yönetimi
  - tool permission yönetimi
  - korumalı dosya
  - loop güvenliği
objectives:
  - "LO-14.1"
  - "LO-14.2"
  - "LO-14.3"
  - "LO-14.4"
  - "LO-14.5"
  - "LO-14.6"
  - "LO-14.7"
last_verified: "2026-07"

Gömülü Vardiya sözleşmesi temsilîdir. Doğrulayıcı yazılı kararların yapısını
denetler; gerçek araç izinlerini, CI hattını veya secret taramasını değiştirmez.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Mapping, Sequence


DATA_DECISIONS = frozenset({"gönderilebilir", "anonimleştirilerek", "asla"})
PERMISSION_DECISIONS = frozenset({"allow", "ask", "deny"})
PROTECTED_PATH_DECISIONS = frozenset({"ask", "deny"})
SCANNER_LOCATIONS = ("ci", "pre-commit", "commit öncesi", "sunucu")
ROTATION_WORDS = ("iptal", "rotasyon", "rotate", "geçersiz")
CHAPTER_REFERENCE_PATTERN = re.compile(r"\b14\.(?:[1-9]|1[0-3])\b")
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
CREDENTIAL_PATTERN = re.compile(
    r"\b(?:api[_ -]?key|secret|token|password|şifre|parola)\b"
    r"\s*[:=]\s*[`'\"]?[^\s`'\"]{4,}",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ClassifiedData:
    """Bir veri türünün paylaşım kararını ve gerekçesini taşır."""

    name: str
    decision: str
    reason: str


@dataclass(frozen=True)
class SecretPlan:
    """Secret önleme ve sızıntı sonrası müdahale adımlarını taşır."""

    ignored_paths: tuple[str, ...]
    scanning_step: str
    incident_steps: tuple[str, ...]


@dataclass(frozen=True)
class PermissionRule:
    """Bir işlem için allow, ask veya deny kararını taşır."""

    operation: str
    decision: str
    reason: str


@dataclass(frozen=True)
class ProtectedPath:
    """Bir korumalı yolun izin katmanını ve gerekçesini taşır."""

    path: str
    decision: str
    reason: str


@dataclass(frozen=True)
class LoopLimits:
    """Bir ajan döngüsünün yetki, maliyet ve veri sınırlarını taşır."""

    authority: str
    cost: str
    data: str


@dataclass(frozen=True)
class SecurityContract:
    """Beş bölümlü güvenlik sözleşmesini tek kayıtta toplar."""

    data_rules: tuple[ClassifiedData, ...]
    secret_plan: SecretPlan
    permission_rules: tuple[PermissionRule, ...]
    protected_paths: tuple[ProtectedPath, ...]
    loop_limits: LoopLimits
    reference_note: str


@dataclass(frozen=True)
class ValidationReport:
    """Sözleşmenin sayısal özetini ve bulunan sorunları taşır."""

    data_count: int
    data_decision_count: int
    ignored_path_count: int
    incident_step_count: int
    permission_count: int
    permission_counts: tuple[tuple[str, int], ...]
    protected_path_count: int
    loop_limit_count: int
    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        """Hiç hata yoksa kabul ölçütlerinin karşılandığını bildirir."""

        return not self.errors

    def permission_count_for(self, decision: str) -> int:
        """İstenen izin kararının rapordaki sayısını döndürür."""

        return dict(self.permission_counts).get(decision, 0)


REPRESENTATIVE_CONTRACT = SecurityContract(
    data_rules=(
        ClassifiedData(
            name="Sentetik vardiya kuralı",
            decision="gönderilebilir",
            reason="Gerçek kullanıcı veya kuruma ait kayıt içermez.",
        ),
        ClassifiedData(
            name="Maskelenmiş hata kaydı",
            decision="anonimleştirilerek",
            reason="Ad, e-posta, IP adresi ve sipariş numarası çıkarılmalıdır.",
        ),
        ClassifiedData(
            name="Üretim veritabanı kaydı ve .env dosyası",
            decision="asla",
            reason="Gerçek müşteri verisi ile erişim bilgileri dışarı gönderilemez.",
        ),
    ),
    secret_plan=SecretPlan(
        ignored_paths=(".env", ".env.local"),
        scanning_step=(
            "Secret taraması commit öncesi denetimde ve CI hattında çalışır."
        ),
        incident_steps=(
            "Sızan anahtarı sağlayıcı panelinden hemen iptal et ve yenisini üret.",
            "Erişim kayıtlarını incele, olayı kaydet ve güvenlik sorumlusuna bildir.",
            (
                "14.11'deki sırayı izleyerek ekibi bilgilendir ve git geçmişini "
                "koordineli biçimde temizle."
            ),
        ),
    ),
    permission_rules=(
        PermissionRule(
            operation="Kaynak kodu okuma",
            decision="allow",
            reason="Görevin kapsamındaki kodu anlamak için gereklidir.",
        ),
        PermissionRule(
            operation="Yerel testleri çalıştırma",
            decision="allow",
            reason="Değişikliği dış sisteme dokunmadan doğrular.",
        ),
        PermissionRule(
            operation="Migration çalıştırma",
            decision="ask",
            reason="Veri yapısını değiştirdiği için insan onayı gerekir.",
        ),
        PermissionRule(
            operation="Yeni bağımlılık kurma",
            decision="ask",
            reason="Paket kaydı ve bakımcı geçmişi kurulmadan önce doğrulanmalıdır.",
        ),
        PermissionRule(
            operation=".env dosyasını okuma",
            decision="deny",
            reason="Dosya erişim bilgisi içerebilir ve görev için gerekli değildir.",
        ),
        PermissionRule(
            operation="Üretim veritabanına yazma",
            decision="deny",
            reason="Geri dönüşü zor ve kapsam dışı bir üretim işlemidir.",
        ),
    ),
    protected_paths=(
        ProtectedPath(
            path="auth/",
            decision="deny",
            reason="Yetkilendirme değişikliği ek güvenlik incelemesi gerektirir.",
        ),
        ProtectedPath(
            path="payments/",
            decision="deny",
            reason="Finansal yan etki riski taşıyan işlemleri içerir.",
        ),
        ProtectedPath(
            path=".github/workflows/",
            decision="ask",
            reason="CI davranışını değiştirdiği için insan onayı gerekir.",
        ),
    ),
    loop_limits=LoopLimits(
        authority="Döngü yalnızca test dosyalarını okuyabilir ve test çalıştırabilir.",
        cost="Bir çalışma en çok 3 deneme ve 15 dakika sürebilir.",
        data="Döngü yalnızca sentetik vardiya kayıtlarına erişebilir.",
    ),
    reference_note=(
        "Secret sızıntısında 14.11'deki rotasyon adımı geçmiş temizliğinden önce gelir."
    ),
)


def _word_count(text: str) -> int:
    """Boşlukla ayrılmış sözcüklerin sayısını döndürür."""

    return len(text.strip().split())


def _normalized(text: str) -> str:
    """Karşılaştırma için boşlukları ve harf büyüklüğünü düzenler."""

    return re.sub(r"\s+", " ", text.casefold()).strip()


def _duplicate_values(values: Sequence[str]) -> bool:
    """Dolu değerler arasında yinelenen kayıt olup olmadığını bildirir."""

    normalized = [_normalized(value) for value in values if value.strip()]
    return len(normalized) != len(set(normalized))


def _sensitive_data_kind(text: str) -> str | None:
    """Açık e-posta veya gizli bilgi atamasını adlandırır."""

    if EMAIL_PATTERN.search(text):
        return "açık e-posta adresi"
    if CREDENTIAL_PATTERN.search(text):
        return "gizli bilgi ataması"
    return None


def validate_contract(contract: SecurityContract) -> ValidationReport:
    """Güvenlik sözleşmesini açık kabul ölçütlerine göre doğrular."""

    errors: list[str] = []

    if len(contract.data_rules) < 3:
        errors.append("Veri sınıflandırması en az 3 örnek içermelidir.")
    data_decisions: set[str] = set()
    for number, rule in enumerate(contract.data_rules, start=1):
        decision = rule.decision.casefold().strip()
        if not rule.name.strip():
            errors.append(f"Veri kuralı {number} veri türünü belirtmelidir.")
        if decision not in DATA_DECISIONS:
            expected = ", ".join(sorted(DATA_DECISIONS))
            errors.append(
                f"Veri kuralı {number} şu kararlardan birini kullanmalıdır: {expected}."
            )
        else:
            data_decisions.add(decision)
        if _word_count(rule.reason) < 4:
            errors.append(f"Veri kuralı {number} somut bir gerekçe içermelidir.")
    missing_data_decisions = DATA_DECISIONS - data_decisions
    if missing_data_decisions:
        missing = ", ".join(sorted(missing_data_decisions))
        errors.append(f"Veri sınıflandırmasında şu kararlar eksik: {missing}.")
    if _duplicate_values([rule.name for rule in contract.data_rules]):
        errors.append("Aynı veri türü birden fazla kez sınıflandırılmamalıdır.")

    ignored_paths = tuple(
        path.strip() for path in contract.secret_plan.ignored_paths if path.strip()
    )
    if not ignored_paths:
        errors.append("Secret yönetimi en az bir yok sayılan dosya veya yol içermelidir.")
    elif not any(path == ".env" or path.startswith(".env.") for path in ignored_paths):
        errors.append("Yok sayılan yollar en az bir .env dosyasını açıkça belirtmelidir.")
    if _duplicate_values(ignored_paths):
        errors.append("Aynı yok sayılan yol birden fazla kez yazılmamalıdır.")

    scanning_step = _normalized(contract.secret_plan.scanning_step)
    if _word_count(scanning_step) < 5:
        errors.append("Secret taramasının nerede çalıştığı somut biçimde yazılmalıdır.")
    elif not any(location in scanning_step for location in SCANNER_LOCATIONS):
        errors.append(
            "Secret taraması CI, pre-commit veya commit öncesi denetim noktasına "
            "bağlanmalıdır."
        )

    incident_steps = tuple(
        step.strip() for step in contract.secret_plan.incident_steps if step.strip()
    )
    if len(incident_steps) < 3:
        errors.append("Secret sızıntısı için en az 3 sıralı müdahale adımı yazılmalıdır.")
    if incident_steps and not any(
        word in incident_steps[0].casefold() for word in ROTATION_WORDS
    ):
        errors.append("Secret sızıntısının ilk adımı anahtarı iptal etmek olmalıdır.")
    for number, step in enumerate(incident_steps, start=1):
        if _word_count(step) < 5:
            errors.append(f"Secret müdahalesinin {number}. adımı somut yazılmalıdır.")

    if len(contract.permission_rules) < 5:
        errors.append("İzin listesi en az 5 işlem içermelidir.")
    permission_counts = {decision: 0 for decision in PERMISSION_DECISIONS}
    for number, rule in enumerate(contract.permission_rules, start=1):
        decision = rule.decision.casefold().strip()
        if not rule.operation.strip():
            errors.append(f"İzin kuralı {number} işlemi belirtmelidir.")
        if decision not in PERMISSION_DECISIONS:
            errors.append(
                f"İzin kuralı {number} allow, ask veya deny kararı kullanmalıdır."
            )
        else:
            permission_counts[decision] += 1
        if _word_count(rule.reason) < 4:
            errors.append(f"İzin kuralı {number} somut bir gerekçe içermelidir.")
    missing_permissions = {
        decision for decision, count in permission_counts.items() if count == 0
    }
    if missing_permissions:
        missing = ", ".join(sorted(missing_permissions))
        errors.append(f"İzin listesinde şu kararlar eksik: {missing}.")
    if _duplicate_values([rule.operation for rule in contract.permission_rules]):
        errors.append("Aynı işlem izin listesinde birden fazla kez yazılmamalıdır.")

    if len(contract.protected_paths) < 3:
        errors.append("Korumalı dosyalar en az 3 yol içermelidir.")
    for number, protected in enumerate(contract.protected_paths, start=1):
        decision = protected.decision.casefold().strip()
        if not protected.path.strip():
            errors.append(f"Korumalı alan {number} dosya veya yolu belirtmelidir.")
        if decision not in PROTECTED_PATH_DECISIONS:
            errors.append(
                f"Korumalı alan {number} yalnızca ask veya deny kararı kullanmalıdır."
            )
        if _word_count(protected.reason) < 4:
            errors.append(f"Korumalı alan {number} somut bir gerekçe içermelidir.")
    if _duplicate_values([item.path for item in contract.protected_paths]):
        errors.append("Aynı korumalı yol birden fazla kez yazılmamalıdır.")

    loop_values = {
        "yetki": contract.loop_limits.authority,
        "maliyet": contract.loop_limits.cost,
        "veri": contract.loop_limits.data,
    }
    loop_limit_count = 0
    for name, value in loop_values.items():
        if _word_count(value) < 5:
            errors.append(f"Loop {name} sınırı somut bir cümleyle yazılmalıdır.")
        else:
            loop_limit_count += 1
    if contract.loop_limits.cost.strip() and not re.search(
        r"\d", contract.loop_limits.cost
    ):
        errors.append("Loop maliyet sınırı sayısal bir tavan içermelidir.")

    if not CHAPTER_REFERENCE_PATTERN.search(contract.reference_note):
        errors.append("Sözleşme Bölüm 14'teki en az bir alt başlığa başvurmalıdır.")

    contract_text = "\n".join(
        [
            *(f"{rule.name} {rule.reason}" for rule in contract.data_rules),
            *ignored_paths,
            contract.secret_plan.scanning_step,
            *incident_steps,
            *(
                f"{rule.operation} {rule.reason}"
                for rule in contract.permission_rules
            ),
            *(
                f"{item.path} {item.reason}" for item in contract.protected_paths
            ),
            *loop_values.values(),
            contract.reference_note,
        ]
    )
    sensitive_kind = _sensitive_data_kind(contract_text)
    if sensitive_kind:
        errors.append(
            f"Sözleşme {sensitive_kind} içeriyor; yalnızca temsilî veri kullanın."
        )

    return ValidationReport(
        data_count=len(contract.data_rules),
        data_decision_count=len(data_decisions),
        ignored_path_count=len(ignored_paths),
        incident_step_count=len(incident_steps),
        permission_count=len(contract.permission_rules),
        permission_counts=tuple(sorted(permission_counts.items())),
        protected_path_count=len(contract.protected_paths),
        loop_limit_count=loop_limit_count,
        errors=tuple(errors),
    )


def format_report(report: ValidationReport) -> str:
    """Doğrulama sonucunu terminalde okunacak kısa bir özete çevirir."""

    lines = [
        "Güvenlik Sözleşmesi Denetimi",
        f"Veri kuralı: {report.data_count} (kategori: {report.data_decision_count}/3)",
        (
            "Secret yönetimi: "
            f"{report.ignored_path_count} yok sayılan yol, "
            f"{report.incident_step_count} olay adımı"
        ),
        (
            f"İzin kuralı: {report.permission_count} "
            f"(allow: {report.permission_count_for('allow')}, "
            f"ask: {report.permission_count_for('ask')}, "
            f"deny: {report.permission_count_for('deny')})"
        ),
        f"Korumalı alan: {report.protected_path_count}",
        f"Loop sınırı: {report.loop_limit_count}/3",
    ]
    if report.is_valid:
        lines.append(
            "Kabul kriteri karşılandı: Beş bölüm ve karar gerekçeleri tamam."
        )
    else:
        lines.append("Kabul kriteri karşılanmadı:")
        lines.extend(f"- {error}" for error in report.errors)
    return "\n".join(lines)


def contract_from_mapping(data: Mapping[str, Any]) -> SecurityContract:
    """JSON nesnesini doğrulanacak güvenlik sözleşmesine dönüştürür."""

    secret_plan = data["secret_plan"]
    loop_limits = data["loop_limits"]
    return SecurityContract(
        data_rules=tuple(ClassifiedData(**item) for item in data["data_rules"]),
        secret_plan=SecretPlan(
            ignored_paths=tuple(secret_plan["ignored_paths"]),
            scanning_step=secret_plan["scanning_step"],
            incident_steps=tuple(secret_plan["incident_steps"]),
        ),
        permission_rules=tuple(
            PermissionRule(**item) for item in data["permission_rules"]
        ),
        protected_paths=tuple(
            ProtectedPath(**item) for item in data["protected_paths"]
        ),
        loop_limits=LoopLimits(**loop_limits),
        reference_note=data["reference_note"],
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Gömülü örneği veya verilen UTF-8 JSON sözleşmesini doğrular."""

    parser = argparse.ArgumentParser(
        description="Beş bölümlü bir güvenlik sözleşmesini doğrular."
    )
    parser.add_argument("contract_file", nargs="?", type=Path, metavar="SOZLESME_JSON")
    args = parser.parse_args(argv)

    if args.contract_file:
        try:
            raw = json.loads(args.contract_file.read_text(encoding="utf-8"))
            if not isinstance(raw, dict):
                raise TypeError("kök değer bir JSON nesnesi olmalıdır")
            contract = contract_from_mapping(raw)
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
            parser.error(f"sözleşme okunamadı: {error}")
    else:
        contract = REPRESENTATIVE_CONTRACT

    report = validate_contract(contract)
    print(format_report(report))
    return 0 if report.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
