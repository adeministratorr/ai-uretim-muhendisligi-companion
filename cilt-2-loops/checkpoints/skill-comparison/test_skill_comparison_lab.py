"""Skill karşılaştırma kaydının kabul ve ret durumları."""

from dataclasses import asdict, replace
from html.parser import HTMLParser
import json
from pathlib import Path

import pytest

from skill_comparison_lab import (
    REPRESENTATIVE_TRIALS,
    REQUIRED_ANATOMY_PARTS,
    format_report,
    load_trials,
    main,
    validate_comparison,
)


class BalancedHTMLParser(HTMLParser):
    """Tek dosyalık laboratuvarın temel etiket dengesini denetler."""

    VOID_ELEMENTS = frozenset({"meta", "input", "br", "hr", "img", "link"})

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag not in self.VOID_ELEMENTS:
            self.stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        assert self.stack, f"Kapanış etiketi başlangıçsız: {tag}"
        assert self.stack.pop() == tag, f"Etiket sırası bozuk: {tag}"


def test_representative_trials_meet_acceptance_criteria():
    report = validate_comparison(REPRESENTATIVE_TRIALS)

    assert report.is_valid
    assert report.errors == ()
    assert report.task_count == 3
    assert report.anatomy_complete_count == 3
    assert report.trigger_positive_count == 2
    assert report.instruction_positive_count == 2
    assert report.prohibition_positive_count == 3
    assert report.attention_count == 1


def test_report_keeps_negative_observation_visible_without_rejecting_record():
    output = format_report(validate_comparison(REPRESENTATIVE_TRIALS))

    assert "Trigger gözlemi: 2/3 olumlu" in output
    assert "İncelenecek skill: 1" in output
    assert "Kabul kriteri karşılandı" in output


def test_all_three_required_tasks_must_be_present():
    report = validate_comparison(REPRESENTATIVE_TRIALS[:2])

    assert not report.is_valid
    assert "Eksik görev: commit mesajı yazma." in report.errors


def test_task_cannot_be_recorded_twice():
    duplicate = replace(REPRESENTATIVE_TRIALS[2], task="kod inceleme")

    report = validate_comparison((*REPRESENTATIVE_TRIALS[:2], duplicate))

    assert '"kod inceleme" görevi bir kez kaydedilmelidir.' in report.errors


def test_skill_names_and_requests_must_be_distinct():
    duplicate = replace(
        REPRESENTATIVE_TRIALS[2],
        skill_name=REPRESENTATIVE_TRIALS[0].skill_name,
        test_request=REPRESENTATIVE_TRIALS[0].test_request,
    )

    report = validate_comparison((*REPRESENTATIVE_TRIALS[:2], duplicate))

    assert any("Skill adları yinelenmemelidir" in error for error in report.errors)
    assert "Her skill farklı bir deneme isteğiyle sınanmalıdır." in report.errors


def test_each_anatomy_part_must_be_reviewed():
    incomplete = replace(
        REPRESENTATIVE_TRIALS[0],
        anatomy_parts=REQUIRED_ANATOMY_PARTS[:-1],
    )

    report = validate_comparison((incomplete, *REPRESENTATIVE_TRIALS[1:]))

    assert any("incelenmeyen anatomi parçası: yasaklar" in error for error in report.errors)
    assert report.anatomy_complete_count == 2


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("triggered", "trigger gözlemi evet veya hayır olmalıdır"),
        ("instructions_applied", "talimat gözlemi evet veya hayır olmalıdır"),
        ("prohibitions_respected", "yasaklar gözlemi evet veya hayır olmalıdır"),
    ],
)
def test_each_observation_must_be_answered(field, message):
    unanswered = replace(REPRESENTATIVE_TRIALS[0], **{field: None})

    report = validate_comparison((unanswered, *REPRESENTATIVE_TRIALS[1:]))

    assert any(message in error for error in report.errors)


def test_comparison_note_must_explain_result():
    vague = replace(REPRESENTATIVE_TRIALS[0], comparison_note="İyi çalıştı.")

    report = validate_comparison((vague, *REPRESENTATIVE_TRIALS[1:]))

    assert any("karşılaştırma notu sonucu açıklamalıdır" in error for error in report.errors)


@pytest.mark.parametrize(
    "unsafe_note",
    [
        "Çıktı incelensin diye kisi@example.com adresine gönderildi.",
        "Deneme için API_KEY=gercek_anahtar değeri kullanıldı.",
    ],
)
def test_sensitive_data_patterns_are_rejected(unsafe_note):
    unsafe = replace(REPRESENTATIVE_TRIALS[0], comparison_note=unsafe_note)

    report = validate_comparison((unsafe, *REPRESENTATIVE_TRIALS[1:]))

    assert any("örnek veri kullanın" in error for error in report.errors)


def test_json_file_round_trip(tmp_path):
    path = tmp_path / "karsilastirma.json"
    path.write_text(
        json.dumps([asdict(trial) for trial in REPRESENTATIVE_TRIALS], ensure_ascii=False),
        encoding="utf-8",
    )

    loaded = load_trials(path)

    assert loaded == REPRESENTATIVE_TRIALS
    assert validate_comparison(loaded).is_valid


def test_json_observation_must_be_boolean_or_null(tmp_path):
    records = [asdict(trial) for trial in REPRESENTATIVE_TRIALS]
    records[0]["triggered"] = "evet"
    path = tmp_path / "yanlis.json"
    path.write_text(json.dumps(records, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ValueError, match='"triggered" alanı'):
        load_trials(path)


def test_main_returns_success_for_representative_trials(capsys):
    assert main([]) == 0
    assert "Kabul kriteri karşılandı" in capsys.readouterr().out


def test_html_is_balanced_and_contains_required_explanations_and_links():
    html_path = Path(__file__).with_name("skill_comparison_lab.html")
    html = html_path.read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)

    assert parser.stack == []
    assert "Kavram — Gözlem Kaydı" in html
    assert "Temsilîlik Notu" in html
    assert "last_verified: \"2026-07\"" in html
    assert "prefers-reduced-motion" in html
    assert html.count("github.com/adeministratorr/ai-uretim-muhendisligi-companion") >= 3
