"""Prompt sürüm günlüğü ve gerileme (regression) tespiti.

Kitap bağlantısı: Cilt 1, Bölüm 7 — Prompt Geliştirme, Test ve Belgeleme,
7.3 (Test Seti Oluşturma), 7.5 (Başarı Metriği Belirleme), 7.9 (En İyi Promptu
Seçme), 7.10 (Prompt Log Şablonu) ve 7.11 (Prompt Sürümleme).

Gerçek bir API çağrısı yapmaz. Kaan'ın Hasar Özet Asistanı örneğindeki A/B/C
sürümlerini (7.9'daki karşılaştırma tablosuyla aynı puanlar) ve ardından
üretime alınan v1/v1.1/v2 sürümlerini (7.11'deki anlatım) temel alır. Her
sürüm, 7.3'teki kolay/orta/zor test dosyalarından bir alt kümede (test_results)
ve 7.5'teki dört metrikte (D=Doğruluk, E=Eksiksizlik, B=Biçim uyumu,
K=Kullanılabilirlik) puanlanır. Bu modül iki şeyi otomatik olarak tespit eder:

1. Test gerilemesi: bir önceki sürümde geçen bir test dosyasının yeni sürümde
   başarısız olması (7.11'deki "v2'nin üretimde beklenmedik bir hataya yol
   açtığı" senaryosunun somut karşılığı).
2. Puan gerilemesi: bir metriğin bir önceki sürüme göre, gürültü payını aşacak
   ölçüde düşmesi (7.9'daki "97 ile 98 arasındaki küçük fark gürültü payı
   taşıyabilir" uyarısının doğrudan uygulaması — metrik başına farklı tolerans
   kullanılır çünkü D/E/B 0-100 ölçeğinde, K ise 1-3 rubrik ölçeğindedir).
"""

from __future__ import annotations

from dataclasses import dataclass, field

# 7.5'teki dört metriğin kısaltmaları (7.10'daki "Puan (D/E/B/K)" sütunuyla aynı).
METRIC_KEYS: tuple[str, ...] = ("D", "E", "B", "K")

# Her metrik farklı ölçekte olduğu için (D/E/B: 0-100, K: 1-3 rubrik), gerileme
# tespiti tek bir mutlak eşik yerine metrik başına tolerans kullanır. 7.9'da
# geçen "C 97, B 98 aldı; bu küçük fark gürültü payı taşıyabilir" örneği D/E/B
# için 1.0 puanlık toleransın gerekçesidir.
DEFAULT_METRIC_TOLERANCE: dict[str, float] = {"D": 1.0, "E": 1.0, "B": 1.0, "K": 0.15}


@dataclass(frozen=True)
class PromptVersionEntry:
    """7.10'daki prompt log tablosunun bir satırı, test dosyası düzeyinde ayrıntıyla."""

    version: str
    date: str
    change_summary: str
    change_reason: str
    test_set: str
    model_version: str
    test_results: dict[str, bool]  # test dosyası kimliği -> geçti mi (altın cevaba göre)
    scores: dict[str, float]  # METRIC_KEYS alt kümesi -> puan
    decision: str
    note: str = ""


@dataclass(frozen=True)
class TestRegression:
    """Bir test dosyasının bir önceki sürümde geçip yeni sürümde başarısız olması."""

    test_id: str
    from_version: str
    to_version: str


@dataclass(frozen=True)
class ScoreRegression:
    """Bir metriğin, tolerans payını aşacak biçimde bir önceki sürüme göre düşmesi."""

    metric: str
    from_version: str
    to_version: str
    previous_score: float
    current_score: float

    @property
    def drop(self) -> float:
        return self.previous_score - self.current_score


def validate_entry(entry: PromptVersionEntry) -> list[str]:
    """Bir günlük satırının 7.10 şablonundaki zorunlu alanları taşıyıp taşımadığını denetler."""
    errors: list[str] = []
    if not entry.version.strip():
        errors.append("Sürüm adı boş olamaz.")
    if not entry.change_summary.strip():
        errors.append(f"{entry.version}: değişiklik özeti boş olamaz.")
    if not entry.change_reason.strip():
        errors.append(f"{entry.version}: değişiklik gerekçesi boş olamaz.")
    if not entry.test_set.strip():
        errors.append(f"{entry.version}: test seti adı boş olamaz.")
    if not entry.model_version.strip():
        errors.append(f"{entry.version}: model sürümü boş olamaz.")
    if not entry.test_results:
        errors.append(f"{entry.version}: en az bir test sonucu kaydedilmelidir.")
    if not entry.scores:
        errors.append(f"{entry.version}: en az bir metrik puanı kaydedilmelidir.")
    for metric in entry.scores:
        if metric not in METRIC_KEYS:
            errors.append(f"{entry.version}: bilinmeyen metrik kısaltması '{metric}'.")
    if not entry.decision.strip():
        errors.append(f"{entry.version}: karar (kabul/eleme) boş olamaz.")
    return errors


def validate_log(entries: tuple[PromptVersionEntry, ...]) -> list[str]:
    """Günlüğün tamamını denetler; ayrıca sürüm adlarının tekrarsız olmasını ister."""
    errors: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        errors.extend(validate_entry(entry))
        if entry.version in seen:
            errors.append(f"Sürüm adı tekrar ediyor: {entry.version}.")
        seen.add(entry.version)
    return errors


def detect_test_regressions(
    entries: tuple[PromptVersionEntry, ...]
) -> tuple[TestRegression, ...]:
    """Ardışık sürüm çiftlerinde, bir önceki sürümde geçen bir testin yeni sürümde
    başarısız olduğu durumları listeler.

    `entries` sıralaması kronolojik kabul edilir (günlüğe eklendiği sıra); yalnızca
    birbirini takip eden çiftler karşılaştırılır, çünkü 7.11'deki geri dönüş kararı
    da her zaman "bir önceki sürüme" göre verilir.
    """
    regressions: list[TestRegression] = []
    for previous, current in zip(entries, entries[1:]):
        shared_ids = set(previous.test_results) & set(current.test_results)
        for test_id in sorted(shared_ids):
            if previous.test_results[test_id] and not current.test_results[test_id]:
                regressions.append(
                    TestRegression(
                        test_id=test_id,
                        from_version=previous.version,
                        to_version=current.version,
                    )
                )
    return tuple(regressions)


def detect_score_regressions(
    entries: tuple[PromptVersionEntry, ...],
    tolerance: dict[str, float] | None = None,
) -> tuple[ScoreRegression, ...]:
    """Ardışık sürüm çiftlerinde, tolerans payını aşan metrik düşüşlerini listeler.

    `tolerance` verilmezse DEFAULT_METRIC_TOLERANCE kullanılır (metrik başına ayrı
    eşik; K metriği 1-3 ölçeğinde olduğu için D/E/B'den çok daha küçük bir eşik
    taşır). Tolerans payının içinde kalan düşüşler 7.9'da anlatılan "tek çalıştırma
    gürültüsü" kabul edilir ve gerileme sayılmaz.
    """
    limits = tolerance or DEFAULT_METRIC_TOLERANCE
    regressions: list[ScoreRegression] = []
    for previous, current in zip(entries, entries[1:]):
        shared_metrics = set(previous.scores) & set(current.scores)
        for metric in sorted(shared_metrics):
            prev_score = previous.scores[metric]
            curr_score = current.scores[metric]
            drop = prev_score - curr_score
            limit = limits.get(metric, 1.0)
            if drop > limit:
                regressions.append(
                    ScoreRegression(
                        metric=metric,
                        from_version=previous.version,
                        to_version=current.version,
                        previous_score=prev_score,
                        current_score=curr_score,
                    )
                )
    return tuple(regressions)


def format_log_table(entries: tuple[PromptVersionEntry, ...]) -> str:
    """7.10'daki günlük tablosuyla aynı sütun sırasını üretir."""
    header = "| Tarih | Sürüm | Değişiklik özeti | Test seti | Model sürümü | Puan (D/E/B/K) | Karar |"
    separator = "|---|---|---|---|---|---|---|"
    rows = [header, separator]
    for entry in entries:
        score_text = "/".join(
            _format_score(entry.scores[key]) for key in METRIC_KEYS if key in entry.scores
        )
        rows.append(
            f"| {entry.date} | {entry.version} | {entry.change_summary} | {entry.test_set} "
            f"| {entry.model_version} | {score_text} | {entry.decision} |"
        )
    return "\n".join(rows)


def _format_score(value: float) -> str:
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.1f}".replace(".", ",")


def format_regression_report(
    test_regressions: tuple[TestRegression, ...],
    score_regressions: tuple[ScoreRegression, ...],
) -> str:
    """İnsan tarafından okunabilir kısa bir gerileme raporu üretir."""
    if not test_regressions and not score_regressions:
        return "Gerileme tespit edilmedi: her sürüm bir öncekinde geçen testleri korudu."

    lines: list[str] = []
    for regression in test_regressions:
        lines.append(
            f"[TEST GERİLEMESİ] {regression.test_id}: {regression.from_version} sürümünde "
            f"geçti, {regression.to_version} sürümünde başarısız oldu."
        )
    for regression in score_regressions:
        lines.append(
            f"[PUAN GERİLEMESİ] {regression.metric}: {regression.from_version} sürümünde "
            f"{_format_score(regression.previous_score)}, {regression.to_version} sürümünde "
            f"{_format_score(regression.current_score)} (düşüş: {_format_score(regression.drop)})."
        )
    return "\n".join(lines)


# --- Kaan'ın Hasar Özet Asistanı için örnek günlük (7.9 ve 7.11'deki anlatımla tutarlı) ---
#
# Test dosyası kimlikleri 7.3'teki kolay/orta/zor karışımını temsil eder; "dosya_15_zor"
# 7.3'te tarif edilen "çelişkili ekspertiz raporu içeren" zor dosya türüdür.

DEFAULT_LOG: tuple[PromptVersionEntry, ...] = (
    PromptVersionEntry(
        version="A",
        date="2026-06-02",
        change_summary="İlk taslak (rol tanımı yok, serbest metin çıktı)",
        change_reason="Başlangıç referansı olarak en basit yaklaşım denendi.",
        test_set="test-30",
        model_version="temel model v1",
        test_results={
            "dosya_03_kolay": True,
            "dosya_28_kolay": True,
            "dosya_07_orta": False,
            "dosya_18_orta": False,
            "dosya_15_zor": False,
            "dosya_22_zor": False,
        },
        scores={"D": 61, "E": 58, "B": 40, "K": 1.8},
        decision="Elendi",
    ),
    PromptVersionEntry(
        version="B",
        date="2026-06-05",
        change_summary="Rol + katı JSON şeması eklendi",
        change_reason="Biçim uyumunu artırmak için rol tanımı ve şema zorunluluğu getirildi.",
        test_set="test-30",
        model_version="temel model v1",
        test_results={
            "dosya_03_kolay": True,
            "dosya_28_kolay": True,
            "dosya_07_orta": True,
            "dosya_18_orta": True,
            "dosya_15_zor": False,
            "dosya_22_zor": True,
        },
        scores={"D": 84, "E": 90, "B": 98, "K": 2.1},
        decision="Elendi (C'ye göre düşük doğruluk)",
    ),
    PromptVersionEntry(
        version="C",
        date="2026-06-09",
        change_summary="Meta-prompting ile tutar arama stratejisi eklendi",
        change_reason=(
            "B sürümü çelişkili ekspertiz raporu içeren zor dosyalarda hasar tutarını "
            "bulamıyordu; meta-prompting ile üretilen bir tutar arama stratejisi eklendi."
        ),
        test_set="test-30",
        model_version="temel model v1",
        test_results={
            "dosya_03_kolay": True,
            "dosya_28_kolay": True,
            "dosya_07_orta": True,
            "dosya_18_orta": True,
            "dosya_15_zor": True,
            "dosya_22_zor": True,
        },
        scores={"D": 91, "E": 93, "B": 97, "K": 2.6},
        decision="Kabul edildi",
        note="Üretime alındı; 7.11'e göre sürüm adı v1 olarak belirlendi.",
    ),
    PromptVersionEntry(
        version="v1.1",
        date="2026-06-20",
        change_summary="hasar_tutari alanına sayısal tip zorlaması eklendi",
        change_reason="7.9'da not edilen biçim uyumu sorunu (tutar bazen metin bazen sayı) giderildi.",
        test_set="test-30",
        model_version="temel model v1",
        test_results={
            "dosya_03_kolay": True,
            "dosya_28_kolay": True,
            "dosya_07_orta": True,
            "dosya_18_orta": True,
            "dosya_15_zor": True,
            "dosya_22_zor": True,
        },
        scores={"D": 91, "E": 93, "B": 99, "K": 2.6},
        decision="Kabul edildi (üretimde)",
    ),
    PromptVersionEntry(
        version="v2",
        date="2026-07-01",
        change_summary="Hasar tutarı arama stratejisi kökten değiştirildi (iki adımlı çıkarım)",
        change_reason="Zor dosyalarda doğruluğu daha da artırmak amacıyla yeni bir strateji denendi.",
        test_set="test-30",
        model_version="temel model v1",
        test_results={
            "dosya_03_kolay": True,
            "dosya_28_kolay": True,
            "dosya_07_orta": True,
            "dosya_18_orta": True,
            "dosya_15_zor": False,
            "dosya_22_zor": True,
        },
        scores={"D": 88, "E": 90, "B": 97, "K": 2.5},
        decision="Geri alındı (v1.1'e dönüldü)",
        note=(
            "7.11'deki senaryo: üretimde beklenmedik hata görüldü. Bu günlük kaydı, "
            "dosya_15_zor testinin v1.1'de geçip v2'de başarısız olduğunu gösterir."
        ),
    ),
)


def demo() -> None:
    print("== Prompt log tablosu ==")
    print(format_log_table(DEFAULT_LOG))
    print()

    log_errors = validate_log(DEFAULT_LOG)
    print("== Şablon doğrulama ==")
    print("Hata yok." if not log_errors else "\n".join(log_errors))
    print()

    test_regressions = detect_test_regressions(DEFAULT_LOG)
    score_regressions = detect_score_regressions(DEFAULT_LOG)
    print("== Gerileme raporu ==")
    print(format_regression_report(test_regressions, score_regressions))


if __name__ == "__main__":
    demo()
