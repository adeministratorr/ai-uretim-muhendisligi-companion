"""Bir bakım loop'unun specification ve terminal state kurallarını gösterir.

volume: 2
chapter: 13
book_section: "13.3 Loop Specification ve 13.12-13.15 Doğrulama, Durdurma ve İz"
concepts:
  - loop specification
  - verification ladder
  - terminal state
  - bütçe
  - trace
objectives:
  - "LO-13.2"
  - "LO-13.3"
  - "LO-13.4"
  - "LO-13.5"
  - "LO-13.6"
  - "LO-13.7"
last_verified: "2026-07"

Senaryo ve eşikler temsilîdir. Kod dış servis çağrısı yapmaz, dosya değiştirmez ve
gerçek bir CI sistemi çalıştırmaz.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class LoopState(str, Enum):
    """Bir çalışma turunun devam veya bitiş durumunu tanımlar."""

    RUNNING = "running"
    DONE = "done"
    BLOCKED = "blocked"
    NEEDS_REVIEW = "needs-review"
    UNSAFE = "unsafe"
    BUDGET_EXCEEDED = "budget-exceeded"


TERMINAL_STATES = frozenset(
    {
        LoopState.DONE,
        LoopState.BLOCKED,
        LoopState.NEEDS_REVIEW,
        LoopState.UNSAFE,
        LoopState.BUDGET_EXCEEDED,
    }
)


@dataclass(frozen=True)
class LoopSpec:
    """Bir bakım loop'unun tasarım kararlarını tek kayıtta tutar."""

    name: str
    scale: str
    trigger: str
    goal: str
    verification_ladder: tuple[str, ...]
    stopping_rules: dict[LoopState, str]
    memory: str
    git_strategy: str
    human_review_states: tuple[LoopState, ...]
    max_attempts: int
    max_duration_minutes: int

    def validation_errors(self) -> tuple[str, ...]:
        """Eksik veya çelişkili specification alanlarını açıklar."""

        errors: list[str] = []
        text_fields = {
            "ad": self.name,
            "tetikleyici": self.trigger,
            "hedef": self.goal,
            "hafıza": self.memory,
            "Git stratejisi": self.git_strategy,
        }
        for label, value in text_fields.items():
            if not value.strip():
                errors.append(f"{label} alanı boş bırakılamaz.")

        if self.scale not in {"inner", "middle", "outer"}:
            errors.append("ölçek inner, middle veya outer olmalıdır.")
        if len(self.verification_ladder) < 2:
            errors.append("doğrulama merdiveni en az iki kademeden oluşmalıdır.")
        if len(set(self.verification_ladder)) != len(self.verification_ladder):
            errors.append("doğrulama kademeleri yinelenmemelidir.")
        if any(not step.strip() for step in self.verification_ladder):
            errors.append("doğrulama kademesi boş bırakılamaz.")

        defined_states = set(self.stopping_rules)
        missing_states = TERMINAL_STATES - defined_states
        extra_states = defined_states - TERMINAL_STATES
        if missing_states:
            names = ", ".join(sorted(state.value for state in missing_states))
            errors.append(f"durdurma kuralı eksik: {names}.")
        if extra_states:
            names = ", ".join(sorted(state.value for state in extra_states))
            errors.append(f"terminal olmayan duruma durdurma kuralı yazılmış: {names}.")
        if any(not rule.strip() for rule in self.stopping_rules.values()):
            errors.append("durdurma kuralları boş bırakılamaz.")

        review_states = set(self.human_review_states)
        if not review_states:
            errors.append("en az bir terminal state insan onayına düşmelidir.")
        if not review_states <= TERMINAL_STATES:
            errors.append("insan onayı yalnızca terminal state'ler için tanımlanabilir.")
        if not review_states.intersection({LoopState.NEEDS_REVIEW, LoopState.UNSAFE}):
            errors.append("needs-review veya unsafe insan onayına düşmelidir.")

        if self.max_attempts < 1:
            errors.append("deneme bütçesi en az 1 olmalıdır.")
        if self.max_duration_minutes < 1:
            errors.append("süre bütçesi en az 1 dakika olmalıdır.")
        return tuple(errors)


@dataclass(frozen=True)
class VerificationResult:
    """Doğrulama merdivenindeki tek bir kademenin sonucunu taşır."""

    name: str
    passed: bool


@dataclass(frozen=True)
class RunObservation:
    """Bir loop turunda gözlenen kanıtları taşır."""

    attempt: int
    elapsed_minutes: int
    verification_results: tuple[VerificationResult, ...]
    behavior_matches_goal: bool = True
    external_blocker: str | None = None
    needs_human_judgment: bool = False
    touches_sensitive_area: bool = False


@dataclass(frozen=True)
class LoopDecision:
    """Değerlendirmenin durumunu, gerekçesini ve iz kaydını taşır."""

    state: LoopState
    reason: str
    trace: str

    @property
    def is_terminal(self) -> bool:
        """Karar loop'u durduruyorsa doğru döndürür."""

        return self.state in TERMINAL_STATES


def representative_spec() -> LoopSpec:
    """Vardiya'nın haftalık bakım işi için eksiksiz specification üretir."""

    return LoopSpec(
        name="Haftalık test sağlığı taraması",
        scale="outer",
        trigger="Her pazartesi saat 09.00'da elle onaylanan zamanlayıcı",
        goal="Test paketi sıfır hatayla tamamlansın ve hedef davranış korunsun",
        verification_ladder=(
            "Sözdizimi ve lint kontrolü",
            "Birim testleri",
            "Davranış ve diff incelemesi",
        ),
        stopping_rules={
            LoopState.DONE: "Bütün kontroller ve hedef davranış doğrulandı.",
            LoopState.BLOCKED: "Dış bağımlılık loop'un ilerlemesini engelliyor.",
            LoopState.NEEDS_REVIEW: "İş mantığı insan yorumu gerektiriyor.",
            LoopState.UNSAFE: "Hassas alana dokunuldu; otomatik işlem durdu.",
            LoopState.BUDGET_EXCEEDED: "Deneme veya süre bütçesi doldu.",
        },
        memory="Önceki başarısız deneme, hata özeti ve son checkpoint kaydı",
        git_strategy="Her bulgu ayrı worktree ve feature branch üzerinde işlenir",
        human_review_states=(LoopState.NEEDS_REVIEW, LoopState.UNSAFE),
        max_attempts=3,
        max_duration_minutes=30,
    )


def _validate_observation(spec: LoopSpec, observation: RunObservation) -> None:
    """Çalışma gözleminin specification ile aynı merdiveni kullandığını denetler."""

    errors = spec.validation_errors()
    if errors:
        raise ValueError("Geçersiz loop specification: " + " ".join(errors))
    if observation.attempt < 1:
        raise ValueError("deneme numarası en az 1 olmalıdır.")
    if observation.elapsed_minutes < 0:
        raise ValueError("geçen süre negatif olamaz.")

    observed_steps = tuple(result.name for result in observation.verification_results)
    if observed_steps != spec.verification_ladder:
        raise ValueError("doğrulama sonuçları specification'daki sırayla verilmelidir.")


def evaluate_run(spec: LoopSpec, observation: RunObservation) -> LoopDecision:
    """Bir çalışma gözlemini güvenlik, bütçe ve doğrulama sırasıyla değerlendirir."""

    _validate_observation(spec, observation)
    passed = sum(result.passed for result in observation.verification_results)
    total = len(observation.verification_results)

    if observation.touches_sensitive_area:
        state = LoopState.UNSAFE
        reason = "yetkilendirme dosyasına dokunuldu; otomatik işlem durdu."
    elif observation.external_blocker:
        state = LoopState.BLOCKED
        reason = observation.external_blocker.rstrip(".") + "."
    elif (
        observation.attempt > spec.max_attempts
        or observation.elapsed_minutes > spec.max_duration_minutes
    ):
        state = LoopState.BUDGET_EXCEEDED
        reason = (
            f"{spec.max_attempts} deneme veya {spec.max_duration_minutes} dakika "
            "sınırı aşıldı."
        )
    elif passed == total and not observation.behavior_matches_goal:
        state = LoopState.NEEDS_REVIEW
        reason = "teknik kontroller geçti; hedef davranış kanıtlanmadı."
    elif passed == total and observation.needs_human_judgment:
        state = LoopState.NEEDS_REVIEW
        reason = "teknik kontroller geçti; iş mantığı yorumu gerekiyor."
    elif passed == total:
        state = LoopState.DONE
        reason = "test paketi ve davranış kontrolü geçti."
    elif (
        observation.attempt >= spec.max_attempts
        or observation.elapsed_minutes >= spec.max_duration_minutes
    ):
        state = LoopState.BUDGET_EXCEEDED
        reason = (
            f"{spec.max_attempts} deneme veya {spec.max_duration_minutes} dakika "
            "sınırında doğrulama tamamlanamadı."
        )
    else:
        state = LoopState.RUNNING
        failed_step = next(
            result.name for result in observation.verification_results if not result.passed
        )
        reason = f"{failed_step} geçmedi; bütçe içinde yeni tur açılabilir."

    trace = (
        f"tur={observation.attempt}; süre={observation.elapsed_minutes}dk; "
        f"doğrulama={passed}/{total}; state={state.value}; gerekçe={reason}"
    )
    return LoopDecision(state=state, reason=reason, trace=trace)


def _results(spec: LoopSpec, *passed: bool) -> tuple[VerificationResult, ...]:
    """Temsilî gözlemler için sıralı doğrulama sonuçları üretir."""

    return tuple(
        VerificationResult(name=name, passed=result)
        for name, result in zip(spec.verification_ladder, passed, strict=True)
    )


def representative_decisions() -> tuple[LoopDecision, ...]:
    """Beş terminal state için birer temsilî karar üretir."""

    spec = representative_spec()
    checks = _results(spec, True, True, True)
    observations = (
        RunObservation(1, 8, checks),
        RunObservation(
            1,
            4,
            _results(spec, True, False, False),
            external_blocker="paket kayıt defterine erişilemiyor",
        ),
        RunObservation(1, 9, checks, needs_human_judgment=True),
        RunObservation(1, 2, checks, touches_sensitive_area=True),
        RunObservation(4, 31, _results(spec, True, False, False)),
    )
    return tuple(evaluate_run(spec, observation) for observation in observations)


def format_report(decisions: tuple[LoopDecision, ...]) -> str:
    """Temsilî terminal state kararlarını kısa bir rapora dönüştürür."""

    covered = {decision.state for decision in decisions}.intersection(TERMINAL_STATES)
    lines = ["Bakım Loop'u Karar Raporu"]
    lines.extend(f"{decision.state.value}: {decision.reason}" for decision in decisions)
    lines.append(f"Terminal state kapsamı: {len(covered)}/{len(TERMINAL_STATES)}")
    return "\n".join(lines)


def main() -> None:
    """Beş temsilî terminal state'i terminale yazar."""

    print(format_report(representative_decisions()))


if __name__ == "__main__":
    main()
