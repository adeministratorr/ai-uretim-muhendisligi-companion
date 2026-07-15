"""Değişebilir varsayılan argüman hatasını kanıtlayıp güvenli düzeltmeyi gösterir.

volume: 2
chapter: 12
book_section: "12.5 Minimal Repro Hazırlama ve 12.9 Testle Doğrulama"
concepts:
  - minimal repro
  - açıkla-hipotez kur-kanıt göster
  - failing test
  - fix
  - regression
objectives:
  - "LO-12.2"
  - "LO-12.3"
  - "LO-12.4"
last_verified: "2026-07"

Senaryo temsilîdir. Bozuk fonksiyon, hatayı deterministik biçimde yeniden üretirken her
denemede boş bir listeyle başlamak için yeniden oluşturulur; uygulama kodunda kullanılmamalıdır.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Shift:
    """Kurgusal bir vardiyanın kısa kimliğini taşır."""

    shift_id: str


@dataclass
class Schedule:
    """Kurgusal bir planın vardiya listesini taşır."""

    name: str
    shifts: list[Shift] = field(default_factory=list)


@dataclass(frozen=True)
class ReproEvidence:
    """Minimal repro'nun beklenen, gerçek ve izlenebilir sonuçlarını taşır."""

    expected_second: tuple[str, ...]
    actual_first: tuple[str, ...]
    actual_second: tuple[str, ...]
    shares_same_list: bool


@dataclass(frozen=True)
class DebugReport:
    """Hata ayıklama döngüsünün kanıtını ve düzeltme sonucunu bir arada tutar."""

    repro: ReproEvidence
    fixed_first: tuple[str, ...]
    fixed_second: tuple[str, ...]
    regression_passed: int
    regression_total: int

    @property
    def fix_is_valid(self) -> bool:
        """Düzeltme planları ayırıyor ve bütün regresyon kontrolleri geçiyorsa doğrudur."""

        return (
            self.fixed_first == ("A",)
            and self.fixed_second == ("B",)
            and self.regression_passed == self.regression_total
        )


ShiftAdder = Callable[[Schedule, Shift], Schedule]


def make_buggy_adder() -> ShiftAdder:
    """Her çağrıda aynı varsayılan listeyi kullanan bozuk fonksiyonu üretir.

    Üretici fonksiyon, paylaşılan listenin her minimal repro çalışmasında boş başlamasını sağlar.
    İçteki fonksiyon bölümdeki `assigned=[]` hatasını bilinçli olarak taşır.
    """

    shared_default: list[Shift] = []

    def add_shift_to_schedule(
        schedule: Schedule,
        shift: Shift,
        assigned: list[Shift] = shared_default,
    ) -> Schedule:
        assigned.append(shift)
        schedule.shifts = assigned
        return schedule

    return add_shift_to_schedule


def add_shift_to_schedule(
    schedule: Schedule,
    shift: Shift,
    assigned: list[Shift] | None = None,
) -> Schedule:
    """Vardiyayı, her çağrı için ayrı varsayılan liste oluşturarak plana ekler."""

    if assigned is None:
        assigned = []
    assigned.append(shift)
    schedule.shifts = assigned
    return schedule


def _shift_ids(schedule: Schedule) -> tuple[str, ...]:
    """Plan vardiyalarını raporda kullanılacak değişmez kimlik dizisine çevirir."""

    return tuple(shift.shift_id for shift in schedule.shifts)


def run_minimal_repro() -> ReproEvidence:
    """İki ayrı planın bozuk sürümde aynı listeyi paylaştığını yeniden üretir."""

    buggy_add = make_buggy_adder()
    first = Schedule("Birinci plan")
    second = Schedule("İkinci plan")

    buggy_add(first, Shift("A"))
    buggy_add(second, Shift("B"))

    return ReproEvidence(
        expected_second=("B",),
        actual_first=_shift_ids(first),
        actual_second=_shift_ids(second),
        shares_same_list=first.shifts is second.shifts,
    )


def run_fixed_scenario() -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Aynı iki çağrıyı güvenli sürümle çalıştırıp plan sonuçlarını döndürür."""

    first = Schedule("Birinci plan")
    second = Schedule("İkinci plan")

    add_shift_to_schedule(first, Shift("A"))
    add_shift_to_schedule(second, Shift("B"))

    return _shift_ids(first), _shift_ids(second)


def build_debug_report() -> DebugReport:
    """Minimal repro, düzeltme ve regresyon kontrollerini tek raporda toplar."""

    repro = run_minimal_repro()
    fixed_first, fixed_second = run_fixed_scenario()

    supplied: list[Shift] = []
    supplied_schedule = Schedule("Dış liste kullanan plan")
    add_shift_to_schedule(supplied_schedule, Shift("C"), supplied)

    regression_checks = (
        fixed_first == ("A",),
        fixed_second == ("B",),
        supplied_schedule.shifts is supplied and _shift_ids(supplied_schedule) == ("C",),
    )
    return DebugReport(
        repro=repro,
        fixed_first=fixed_first,
        fixed_second=fixed_second,
        regression_passed=sum(regression_checks),
        regression_total=len(regression_checks),
    )


def _listed(values: tuple[str, ...]) -> str:
    """Kimlik dizisini okunabilir listeye çevirir."""

    return ", ".join(values) if values else "boş"


def format_report(report: DebugReport) -> str:
    """Hata ayıklama kanıtını ve Git adımlarını Türkçe metin olarak biçimler."""

    shared = "evet" if report.repro.shares_same_list else "hayır"
    return "\n".join(
        (
            "Minimal Repro'dan Düzeltmeye Hata Ayıklama Döngüsü",
            "Beklenen davranış: ikinci plan yalnızca B vardiyasını içerir.",
            f"Gerçek davranış: ikinci plan {_listed(report.repro.actual_second)} "
            "vardiyalarını içeriyor.",
            f"Hata izi: birinci ve ikinci plan aynı listeyi kullanıyor: {shared}",
            "Hipotez: değişebilir varsayılan liste çağrılar arasında paylaşılıyor.",
            "Kanıt: assigned listesi fonksiyon oluşturulurken bir kez üretildi.",
            "Düzeltme: assigned=None; yalnızca None geldiğinde yeni liste oluştur.",
            f"Düzeltme sonrası: ikinci plan yalnızca "
            f"{_listed(report.fixed_second)} vardiyasını içeriyor.",
            f"Regression: {report.regression_passed}/{report.regression_total} kontrol geçti.",
            "Commit 1: test: ayrı planların vardiya listesini paylaşmadığını kanıtla",
            "Commit 2: fix: varsayılan vardiya listesini her çağrıda oluştur",
        )
    )


def main() -> None:
    """Temsilî hata ayıklama raporunu terminale yazar."""

    print(format_report(build_debug_report()))


if __name__ == "__main__":
    main()
