"""Cilt 1 Bölüm 6 için karar gerekçesi ve pilot plan laboratuvarı.

Gerçek model çağrısı yapmaz. Tree of Thoughts (ToT) fikrini, adlandırılmış
kriterlerle karşılaştırılan karar dallarına çevirir. Ardından seçilen dal için
planla-uygula-kontrol et döngüsünün ölçülebilir eşik taşıyıp taşımadığını
yerel olarak denetler.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Criterion:
    key: str
    label: str
    weight: int
    evidence: str


@dataclass(frozen=True)
class DecisionBranch:
    key: str
    title: str
    description: str
    scores: dict[str, int]
    resources: dict[str, int]
    risks: tuple[str, ...] = ()


@dataclass(frozen=True)
class BranchEvaluation:
    branch: DecisionBranch
    weighted_score: int
    missing_criteria: tuple[str, ...]
    blockers: tuple[str, ...]

    @property
    def is_actionable(self) -> bool:
        return not self.missing_criteria and not self.blockers


@dataclass(frozen=True)
class ControlThreshold:
    metric: str
    target: str
    failure_action: str


@dataclass(frozen=True)
class PilotPlan:
    branch_key: str
    duration_weeks: int
    plan: str
    data_to_track: tuple[str, ...]
    thresholds: tuple[ControlThreshold, ...]


CRITERIA = (
    Criterion(
        key="peak_load",
        label="sefer sıklığı",
        weight=3,
        evidence="Sabah 07:00-09:00 arası doluluk %95, akşam 17:00-19:00 arası %40.",
    ),
    Criterion(
        key="access",
        label="mahalle erişimi",
        weight=4,
        evidence="Yeşiltepe Mahallesi'nin güney ucu en yakın durağa 1,2 km uzaklıkta.",
    ),
    Criterion(
        key="budget_fit",
        label="bütçe kısıtı",
        weight=2,
        evidence="Ek olarak en fazla 2 araç ve 4 şoför tahsis edilebilir.",
    ),
)

RESOURCE_LIMITS = {"vehicles": 2, "drivers": 4}

DEFAULT_BRANCHES = (
    DecisionBranch(
        key="A",
        title="Sefer sıklığını artır",
        description="Mevcut güzergâhı koru, sabah yoğun saatlerde ek sefer koy.",
        scores={"peak_load": 5, "access": 1, "budget_fit": 4},
        resources={"vehicles": 1, "drivers": 2},
        risks=("Yeşiltepe erişim sorununu çözmez.",),
    ),
    DecisionBranch(
        key="B",
        title="Hattı ikiye böl",
        description="142 numaralı hattı iki kısa hatta ayır, aktarma noktasını merkeze al.",
        scores={"peak_load": 3, "access": 2, "budget_fit": 2},
        resources={"vehicles": 2, "drivers": 4},
        risks=("Aktarma zorunluluğu şikâyeti artırabilir.",),
    ),
    DecisionBranch(
        key="C",
        title="Besleyici hat ekle",
        description="Yeşiltepe için kısa besleyici hat kur, ana hatta aktarma ver.",
        scores={"peak_load": 3, "access": 5, "budget_fit": 4},
        resources={"vehicles": 1, "drivers": 2},
        risks=("Aktarma noktası ve saatleri pilotta izlenmelidir.",),
    ),
)

NUMBER_PATTERN = re.compile(r"\d+(?:[,.]\d+)?")


def build_tree_of_thoughts_prompt(
    criteria: tuple[Criterion, ...] = CRITERIA,
    branches: tuple[DecisionBranch, ...] = DEFAULT_BRANCHES,
) -> str:
    criterion_lines = "\n".join(
        f"- {criterion.label}: {criterion.evidence}" for criterion in criteria
    )
    branch_lines = "\n".join(
        f"- {branch.key} - {branch.title}: {branch.description}" for branch in branches
    )
    return "\n".join(
        [
            "142 numaralı otobüs hattı için Tree of Thoughts karşılaştırması yap.",
            "Her dalı aynı kriterlerle değerlendir; tek cümlelik öneriye atlama.",
            "",
            "Kriterler:",
            criterion_lines,
            "",
            "Dallar:",
            branch_lines,
            "",
            "Çıktı: dal, kanıt, güçlü yan, zayıf yan, bütçe uyumu ve nihai öneri tablosu.",
            "Öneriyi desteklemeyen veya çelişen veriyi ayrıca belirt.",
        ]
    )


def score_branch(
    branch: DecisionBranch,
    criteria: tuple[Criterion, ...] = CRITERIA,
    limits: dict[str, int] | None = None,
) -> BranchEvaluation:
    limits = limits or RESOURCE_LIMITS
    missing = tuple(criterion.key for criterion in criteria if criterion.key not in branch.scores)
    blockers: list[str] = []

    for name, limit in limits.items():
        used = branch.resources.get(name, 0)
        if used > limit:
            label = "araç" if name == "vehicles" else "şoför"
            blockers.append(f"{label} kısıtı aşıldı: {used}/{limit}")

    weighted_score = 0
    for criterion in criteria:
        value = branch.scores.get(criterion.key, 0)
        if value < 0 or value > 5:
            blockers.append(f"{criterion.label} puanı 0-5 aralığında olmalıdır")
            continue
        weighted_score += value * criterion.weight

    return BranchEvaluation(
        branch=branch,
        weighted_score=weighted_score,
        missing_criteria=missing,
        blockers=tuple(blockers),
    )


def rank_branches(
    branches: tuple[DecisionBranch, ...] = DEFAULT_BRANCHES,
    criteria: tuple[Criterion, ...] = CRITERIA,
) -> tuple[BranchEvaluation, ...]:
    evaluations = tuple(score_branch(branch, criteria) for branch in branches)
    return tuple(
        sorted(
            evaluations,
            key=lambda item: (item.is_actionable, item.weighted_score),
            reverse=True,
        )
    )


def recommended_branch(evaluations: tuple[BranchEvaluation, ...]) -> BranchEvaluation:
    for evaluation in evaluations:
        if evaluation.is_actionable:
            return evaluation
    raise ValueError("Uygulanabilir karar dalı bulunamadı")


def format_markdown_table(evaluations: tuple[BranchEvaluation, ...]) -> str:
    rows = ["| Dal | Toplam puan | Durum |", "|---|---:|---|"]
    for item in evaluations:
        status = "uygulanabilir" if item.is_actionable else "kontrol gerekli"
        rows.append(f"| {item.branch.key} - {item.branch.title} | {item.weighted_score} | {status} |")
    return "\n".join(rows)


def build_pilot_plan(branch: DecisionBranch) -> PilotPlan:
    return PilotPlan(
        branch_key=branch.key,
        duration_weeks=4,
        plan=(
            f"{branch.title} dalını dört haftalık sınırlı pilot olarak çalıştır. "
            "Sabah yoğun saatleri önceliklendir; uygulamayı tüm hat ağına yayma."
        ),
        data_to_track=(
            "Yeşiltepe kaynaklı günlük şikâyet sayısı",
            "besleyici hat doluluk oranı",
            "sabah ana hat doluluk oranı",
        ),
        thresholds=(
            ControlThreshold(
                metric="Yeşiltepe kaynaklı şikâyet sayısı",
                target="4 hafta sonunda en az %50 azalma",
                failure_action="Sefer saatlerini ve durak konumunu yeniden düzenle.",
            ),
            ControlThreshold(
                metric="besleyici hat doluluk oranı",
                target="haftalık ortalama %30'un altına düşmemeli",
                failure_action="Sefer sayısını azalt veya güzergâhı kısalt.",
            ),
            ControlThreshold(
                metric="sabah ana hat doluluk oranı",
                target="07:00-09:00 aralığında %85'in altına inmeli",
                failure_action="Ana hat sabah sefer sıklığını ayrı bir dal olarak yeniden değerlendir.",
            ),
        ),
    )


def build_pilot_plan_prompt(plan: PilotPlan) -> str:
    data_lines = "\n".join(f"- {item}" for item in plan.data_to_track)
    threshold_lines = "\n".join(
        f"- {threshold.metric}: {threshold.target}; karşılanmazsa {threshold.failure_action}"
        for threshold in plan.thresholds
    )
    return "\n".join(
        [
            "Yeşiltepe besleyici hattı için planla-uygula-kontrol et çıktısı hazırla.",
            f"Süre: {plan.duration_weeks} hafta.",
            "",
            "İzlenecek veri:",
            data_lines,
            "",
            "Kontrol eşikleri:",
            threshold_lines,
            "",
            "Çıktıyı Plan, Uygulama Sırasında İzlenecek Veri ve Kontrol Adımı başlıklarıyla ver.",
        ]
    )


def has_number(text: str) -> bool:
    return bool(NUMBER_PATTERN.search(text))


def validate_pilot_plan(plan: PilotPlan) -> list[str]:
    errors: list[str] = []
    if plan.duration_weeks <= 0:
        errors.append("Pilot süresi pozitif olmalıdır.")
    if not plan.plan.strip():
        errors.append("Plan bölümü boş olmamalıdır.")
    if not plan.data_to_track:
        errors.append("İzlenecek veri listesi boş olmamalıdır.")
    if not plan.thresholds:
        errors.append("Kontrol eşiği bulunmalıdır.")

    for threshold in plan.thresholds:
        if not threshold.metric.strip():
            errors.append("Kontrol eşiğinde metrik adı bulunmalıdır.")
        if not has_number(threshold.target):
            errors.append(f"{threshold.metric} için sayısal eşik bulunmalıdır.")
        if not threshold.failure_action.strip():
            errors.append(f"{threshold.metric} için karşılanmazsa adımı bulunmalıdır.")

    return errors


def demo() -> None:
    evaluations = rank_branches()
    choice = recommended_branch(evaluations)
    table = format_markdown_table(evaluations)
    plan = build_pilot_plan(choice.branch)
    errors = validate_pilot_plan(plan)

    print("== Tree of Thoughts tablo özeti ==")
    print(table)
    print()
    print(f"Önerilen dal: {choice.branch.key} - {choice.branch.title}")
    print(f"Gerekçe puanı: {choice.weighted_score}")
    print()
    print("== Pilot plan kontrolü ==")
    print(f"Süre: {plan.duration_weeks} hafta")
    for threshold in plan.thresholds:
        print(f"- {threshold.metric}: {threshold.target}")
    print("Doğrulama:", "geçti" if not errors else "; ".join(errors))
    print()
    print("== Prompt uzunluğu ==")
    print(f"ToT prompt satırı: {len(build_tree_of_thoughts_prompt().splitlines())}")
    print(f"Pilot prompt satırı: {len(build_pilot_plan_prompt(plan).splitlines())}")


if __name__ == "__main__":
    demo()
