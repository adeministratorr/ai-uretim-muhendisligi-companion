"""Bakım loop'u specification, karar ve HTML eşleniği için testler."""

from dataclasses import replace
from html.parser import HTMLParser
from pathlib import Path

import pytest

from maintenance_loop import (
    TERMINAL_STATES,
    LoopState,
    RunObservation,
    VerificationResult,
    evaluate_run,
    format_report,
    representative_decisions,
    representative_spec,
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


def results(*passed: bool) -> tuple[VerificationResult, ...]:
    """Temsilî specification sırasıyla doğrulama sonucu üretir."""

    spec = representative_spec()
    return tuple(
        VerificationResult(name=name, passed=result)
        for name, result in zip(spec.verification_ladder, passed, strict=True)
    )


def test_representative_spec_meets_chapter_acceptance_criteria() -> None:
    spec = representative_spec()

    assert spec.validation_errors() == ()
    assert len(spec.verification_ladder) >= 2
    assert set(spec.stopping_rules) == TERMINAL_STATES
    assert {LoopState.NEEDS_REVIEW, LoopState.UNSAFE} <= set(spec.human_review_states)


def test_missing_memory_and_terminal_rule_are_rejected() -> None:
    spec = representative_spec()
    rules = dict(spec.stopping_rules)
    del rules[LoopState.BLOCKED]

    errors = replace(spec, memory="", stopping_rules=rules).validation_errors()

    assert "hafıza alanı boş bırakılamaz." in errors
    assert "durdurma kuralı eksik: blocked." in errors


def test_verification_ladder_requires_two_distinct_steps() -> None:
    spec = representative_spec()

    short_errors = replace(spec, verification_ladder=("Birim testleri",)).validation_errors()
    duplicate_errors = replace(
        spec,
        verification_ladder=("Birim testleri", "Birim testleri"),
    ).validation_errors()

    assert "doğrulama merdiveni en az iki kademeden oluşmalıdır." in short_errors
    assert "doğrulama kademeleri yinelenmemelidir." in duplicate_errors


@pytest.mark.parametrize(
    ("observation", "expected_state"),
    [
        (RunObservation(1, 8, results(True, True, True)), LoopState.DONE),
        (
            RunObservation(
                1,
                4,
                results(True, False, False),
                external_blocker="paket kayıt defterine erişilemiyor",
            ),
            LoopState.BLOCKED,
        ),
        (
            RunObservation(1, 9, results(True, True, True), needs_human_judgment=True),
            LoopState.NEEDS_REVIEW,
        ),
        (
            RunObservation(1, 2, results(True, True, True), touches_sensitive_area=True),
            LoopState.UNSAFE,
        ),
        (RunObservation(4, 31, results(True, False, False)), LoopState.BUDGET_EXCEEDED),
    ],
)
def test_each_terminal_state_has_a_distinct_condition(
    observation: RunObservation,
    expected_state: LoopState,
) -> None:
    decision = evaluate_run(representative_spec(), observation)

    assert decision.state == expected_state
    assert decision.is_terminal
    assert f"state={expected_state.value}" in decision.trace


def test_failed_check_continues_only_while_budget_remains() -> None:
    decision = evaluate_run(
        representative_spec(),
        RunObservation(1, 7, results(True, False, False)),
    )

    assert decision.state == LoopState.RUNNING
    assert not decision.is_terminal
    assert "bütçe içinde yeni tur" in decision.reason


def test_budget_boundary_stops_failed_run() -> None:
    spec = representative_spec()
    decision = evaluate_run(
        spec,
        RunObservation(spec.max_attempts, 12, results(True, False, False)),
    )

    assert decision.state == LoopState.BUDGET_EXCEEDED
    assert "doğrulama tamamlanamadı" in decision.reason


def test_green_checks_do_not_override_wrong_behavior() -> None:
    decision = evaluate_run(
        representative_spec(),
        RunObservation(1, 9, results(True, True, True), behavior_matches_goal=False),
    )

    assert decision.state == LoopState.NEEDS_REVIEW
    assert "hedef davranış kanıtlanmadı" in decision.reason


def test_verification_results_must_follow_spec_order() -> None:
    reversed_results = tuple(reversed(results(True, True, True)))

    with pytest.raises(ValueError, match="specification'daki sırayla"):
        evaluate_run(
            representative_spec(),
            RunObservation(1, 5, reversed_results),
        )


def test_report_covers_exactly_five_terminal_states() -> None:
    decisions = representative_decisions()
    report = format_report(decisions)

    assert {decision.state for decision in decisions} == TERMINAL_STATES
    assert "Terminal state kapsamı: 5/5" in report


def test_html_is_balanced_and_contains_required_context() -> None:
    html = Path(__file__).with_name("maintenance_loop.html").read_text(encoding="utf-8")
    parser = BalancedHTMLParser()

    parser.feed(html)
    parser.close()

    assert parser.stack == []
    assert '<html lang="tr">' in html
    assert "volume: 2" in html
    assert "chapter: 13" in html
    assert 'last_verified: "2026-07"' in html
    assert "Kavram — Loop Specification" in html
    assert "Temsilîlik Notu" in html
    assert "prefers-reduced-motion" in html


def test_html_links_to_python_readme_and_repository() -> None:
    html = Path(__file__).with_name("maintenance_loop.html").read_text(encoding="utf-8")
    repository = "https://github.com/adeministratorr/ai-uretim-muhendisligi-companion"
    lab_path = "cilt-2-loops/debug-loops/maintenance-loop"

    assert f'{repository}/blob/main/{lab_path}/maintenance_loop.py' in html
    assert f'{repository}/tree/main/{lab_path}' in html
    assert f'href="{repository}"' in html
