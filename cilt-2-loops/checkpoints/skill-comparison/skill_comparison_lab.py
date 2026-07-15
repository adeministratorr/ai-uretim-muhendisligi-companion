"""Üç skill denemesinin karşılaştırma kaydını doğrular.

volume: 2
chapter: 10
book_section: "10.3-10.10 Skill Anatomisi, Hazır Skill Kullanımı ve Doğrulama"
concepts:
  - Skill
  - trigger koşulu
  - örnek girdi/çıktı
  - yasaklar
objectives:
  - "LO-10.1"
  - "LO-10.2"
  - "LO-10.4"
last_verified: "2026-07"

Bu laboratuvar skill çalıştırmaz. Kullanıcının gerçek araçta yaptığı üç denemenin
kanıt kaydını denetler. Gömülü kayıtlar temsilîdir; gerçek bir ekip veya ürün
ölçümü değildir.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Sequence


REQUIRED_TASKS = (
    "kod inceleme",
    "test yazma",
    "commit mesajı yazma",
)
REQUIRED_ANATOMY_PARTS = (
    "front matter",
    "talimat",
    "örnek girdi/çıktı",
    "yasaklar",
)

EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
CREDENTIAL_PATTERN = re.compile(
    r"\b(?:api[_ -]?key|secret|token|password|şifre|parola)\b"
    r"\s*[:=]\s*[`'\"]?[^\s`'\"]{4,}",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class SkillTrial:
    """Bir skill için kaynak, deneme isteği ve gözlem sonuçlarını taşır."""

    task: str
    skill_name: str
    source: str
    trigger_condition: str
    anatomy_parts: tuple[str, ...]
    test_request: str
    triggered: bool | None
    instructions_applied: bool | None
    prohibitions_respected: bool | None
    comparison_note: str


@dataclass(frozen=True)
class ComparisonReport:
    """Karşılaştırmanın sayısal özetini ve bulunan eksikleri taşır."""

    task_count: int
    anatomy_complete_count: int
    trigger_positive_count: int
    instruction_positive_count: int
    prohibition_positive_count: int
    attention_count: int
    errors: tuple[str, ...]

    @property
    def is_valid(self) -> bool:
        """Hiç eksik yoksa karşılaştırma kaydının tamamlandığını bildirir."""

        return not self.errors


REPRESENTATIVE_TRIALS = (
    SkillTrial(
        task="kod inceleme",
        skill_name="pr-guvenlik-kontrolu",
        source="Ekip kütüphanesi / güvenlik inceleme paketi",
        trigger_condition='"kod incele", "PR kontrol et" veya benzer bir inceleme isteği',
        anatomy_parts=REQUIRED_ANATOMY_PARTS,
        test_request="Şu pull request diff'ini güvenlik ve test kapsamı açısından incele.",
        triggered=True,
        instructions_applied=True,
        prohibitions_respected=True,
        comparison_note="Skill üç kontrolü raporladı; onay ya da dosya değişikliği yapmadı.",
    ),
    SkillTrial(
        task="test yazma",
        skill_name="test-kapsami-hazirla",
        source="Araç kütüphanesi / test destek paketi",
        trigger_condition='Yalnızca "test yaz" ifadesi geçtiğinde devreye girer',
        anatomy_parts=REQUIRED_ANATOMY_PARTS,
        test_request="Bu hata için bir regresyon senaryosu ekle.",
        triggered=False,
        instructions_applied=False,
        prohibitions_respected=True,
        comparison_note="Trigger koşulu dar kaldı; istek açık çağrıyla yeniden denenecek.",
    ),
    SkillTrial(
        task="commit mesajı yazma",
        skill_name="commit-mesaji-oner",
        source="Ekip kütüphanesi / Git çalışma paketi",
        trigger_condition="Commit mesajı yazma veya önerme isteklerinde devreye girer",
        anatomy_parts=REQUIRED_ANATOMY_PARTS,
        test_request="Bu diff için kısa bir conventional commit mesajı öner.",
        triggered=True,
        instructions_applied=True,
        prohibitions_respected=True,
        comparison_note="Skill yalnızca mesaj önerdi; commit atmadı ve diff'i değiştirmedi.",
    ),
)


def _normalized(value: str) -> str:
    """Karşılaştırma alanını boşluk ve harf farklarından arındırır."""

    return re.sub(r"\s+", " ", value.strip()).casefold()


def _sensitive_data_kind(text: str) -> str | None:
    """Açık e-posta veya gizli bilgi atamasını adlandırır."""

    if EMAIL_PATTERN.search(text):
        return "e-posta adresi"
    if CREDENTIAL_PATTERN.search(text):
        return "gizli bilgi ataması"
    return None


def validate_comparison(trials: Sequence[SkillTrial]) -> ComparisonReport:
    """Üç skill kaydını açık kabul kriterlerine göre doğrular."""

    errors: list[str] = []
    normalized_tasks = [_normalized(trial.task) for trial in trials]
    task_counts = Counter(normalized_tasks)
    required_tasks = {_normalized(task) for task in REQUIRED_TASKS}

    missing_tasks = sorted(required_tasks - set(normalized_tasks))
    unexpected_tasks = sorted(set(normalized_tasks) - required_tasks)
    if missing_tasks:
        errors.append("Eksik görev: " + ", ".join(missing_tasks) + ".")
    if unexpected_tasks:
        errors.append("Kapsam dışı görev: " + ", ".join(unexpected_tasks) + ".")
    for task, count in sorted(task_counts.items()):
        if count > 1:
            errors.append(f'"{task}" görevi bir kez kaydedilmelidir.')

    skill_names = [_normalized(trial.skill_name) for trial in trials if trial.skill_name]
    duplicate_names = sorted(
        name for name, count in Counter(skill_names).items() if count > 1
    )
    if duplicate_names:
        errors.append("Skill adları yinelenmemelidir: " + ", ".join(duplicate_names) + ".")

    requests = [_normalized(trial.test_request) for trial in trials if trial.test_request]
    duplicate_requests = sorted(
        request for request, count in Counter(requests).items() if count > 1
    )
    if duplicate_requests:
        errors.append("Her skill farklı bir deneme isteğiyle sınanmalıdır.")

    anatomy_complete_count = 0
    attention_count = 0
    for number, trial in enumerate(trials, start=1):
        label = trial.skill_name.strip() or f"{number}. kayıt"
        required_text_fields = {
            "skill adı": trial.skill_name,
            "kaynak": trial.source,
            "trigger koşulu": trial.trigger_condition,
            "deneme isteği": trial.test_request,
            "karşılaştırma notu": trial.comparison_note,
        }
        for field_name, value in required_text_fields.items():
            if not value.strip():
                errors.append(f"{label}: {field_name} boş bırakılamaz.")

        if trial.comparison_note.strip() and len(trial.comparison_note.split()) < 4:
            errors.append(f"{label}: karşılaştırma notu sonucu açıklamalıdır.")

        anatomy = {_normalized(part) for part in trial.anatomy_parts}
        missing_parts = [
            part for part in REQUIRED_ANATOMY_PARTS if _normalized(part) not in anatomy
        ]
        if missing_parts:
            errors.append(f"{label}: incelenmeyen anatomi parçası: {', '.join(missing_parts)}.")
        else:
            anatomy_complete_count += 1

        observations = {
            "trigger gözlemi": trial.triggered,
            "talimat gözlemi": trial.instructions_applied,
            "yasaklar gözlemi": trial.prohibitions_respected,
        }
        for observation_name, value in observations.items():
            if value is None:
                errors.append(f"{label}: {observation_name} evet veya hayır olmalıdır.")

        if any(value is False for value in observations.values()):
            attention_count += 1

        combined_text = "\n".join(
            [
                trial.skill_name,
                trial.source,
                trial.trigger_condition,
                trial.test_request,
                trial.comparison_note,
            ]
        )
        sensitive_kind = _sensitive_data_kind(combined_text)
        if sensitive_kind:
            errors.append(f"{label}: kayıt {sensitive_kind} içeriyor; örnek veri kullanın.")

    return ComparisonReport(
        task_count=len(set(normalized_tasks) & required_tasks),
        anatomy_complete_count=anatomy_complete_count,
        trigger_positive_count=sum(trial.triggered is True for trial in trials),
        instruction_positive_count=sum(
            trial.instructions_applied is True for trial in trials
        ),
        prohibition_positive_count=sum(
            trial.prohibitions_respected is True for trial in trials
        ),
        attention_count=attention_count,
        errors=tuple(errors),
    )


def format_report(report: ComparisonReport) -> str:
    """Doğrulama sonucunu terminalde okunacak kısa bir özete çevirir."""

    lines = [
        "Skill Karşılaştırma Kaydı",
        f"Görev: {report.task_count}/3",
        f"Anatomi kontrolü: {report.anatomy_complete_count}/3",
        f"Trigger gözlemi: {report.trigger_positive_count}/3 olumlu",
        f"Talimat gözlemi: {report.instruction_positive_count}/3 olumlu",
        f"Yasaklar gözlemi: {report.prohibition_positive_count}/3 olumlu",
        f"İncelenecek skill: {report.attention_count}",
    ]
    if report.is_valid:
        lines.append(
            "Kabul kriteri karşılandı: Üç skill denendi ve karşılaştırma kaydı tamamlandı."
        )
    else:
        lines.append("Kabul kriteri karşılanmadı:")
        lines.extend(f"- {error}" for error in report.errors)
    return "\n".join(lines)


def _optional_observation(value: Any, field_name: str) -> bool | None:
    """JSON gözlem alanının yalnızca boolean veya null olmasını sağlar."""

    if value is None or isinstance(value, bool):
        return value
    raise ValueError(f'"{field_name}" alanı true, false veya null olmalıdır')


def _trial_from_mapping(data: Any, number: int) -> SkillTrial:
    """Bir JSON nesnesini güvenli biçimde SkillTrial kaydına çevirir."""

    if not isinstance(data, dict):
        raise ValueError(f"{number}. kayıt bir JSON nesnesi olmalıdır")

    def text_field(name: str) -> str:
        value = data.get(name, "")
        if not isinstance(value, str):
            raise ValueError(f'{number}. kayıttaki "{name}" alanı metin olmalıdır')
        return value

    anatomy = data.get("anatomy_parts", [])
    if not isinstance(anatomy, list) or not all(
        isinstance(part, str) for part in anatomy
    ):
        raise ValueError(f'{number}. kayıttaki "anatomy_parts" metin listesi olmalıdır')

    return SkillTrial(
        task=text_field("task"),
        skill_name=text_field("skill_name"),
        source=text_field("source"),
        trigger_condition=text_field("trigger_condition"),
        anatomy_parts=tuple(anatomy),
        test_request=text_field("test_request"),
        triggered=_optional_observation(data.get("triggered"), "triggered"),
        instructions_applied=_optional_observation(
            data.get("instructions_applied"), "instructions_applied"
        ),
        prohibitions_respected=_optional_observation(
            data.get("prohibitions_respected"), "prohibitions_respected"
        ),
        comparison_note=text_field("comparison_note"),
    )


def load_trials(path: Path) -> tuple[SkillTrial, ...]:
    """UTF-8 JSON dosyasındaki kayıt listesini okur."""

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("JSON kökü bir kayıt listesi olmalıdır")
    return tuple(_trial_from_mapping(item, number) for number, item in enumerate(data, 1))


def main(argv: Sequence[str] | None = None) -> int:
    """Gömülü kayıtları veya verilen JSON dosyasını doğrular."""

    parser = argparse.ArgumentParser(
        description="Üç skill denemesinin karşılaştırma kaydını doğrular."
    )
    parser.add_argument("comparison_file", nargs="?", type=Path, metavar="KAYIT_JSON")
    args = parser.parse_args(argv)

    if args.comparison_file:
        try:
            trials = load_trials(args.comparison_file)
        except (OSError, json.JSONDecodeError, ValueError) as error:
            parser.error(f"karşılaştırma kaydı okunamadı: {error}")
    else:
        trials = REPRESENTATIVE_TRIALS

    report = validate_comparison(trials)
    print(format_report(report))
    return 0 if report.is_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
