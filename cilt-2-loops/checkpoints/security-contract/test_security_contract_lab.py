"""Güvenlik sözleşmesi doğrulayıcısının kabul ve ret durumları."""

from dataclasses import asdict, replace
from html.parser import HTMLParser
import json
from pathlib import Path

import pytest

from security_contract_lab import (
    REPRESENTATIVE_CONTRACT,
    ClassifiedData,
    LoopLimits,
    PermissionRule,
    ProtectedPath,
    SecretPlan,
    contract_from_mapping,
    format_report,
    main,
    validate_contract,
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


def test_representative_contract_meets_acceptance_criteria():
    report = validate_contract(REPRESENTATIVE_CONTRACT)

    assert report.is_valid
    assert report.errors == ()
    assert report.data_count == 3
    assert report.data_decision_count == 3
    assert report.ignored_path_count == 2
    assert report.incident_step_count == 3
    assert report.permission_count == 6
    assert report.permission_count_for("allow") == 2
    assert report.permission_count_for("ask") == 2
    assert report.permission_count_for("deny") == 2
    assert report.protected_path_count == 3
    assert report.loop_limit_count == 3


def test_report_shows_five_sections_and_success_result():
    output = format_report(validate_contract(REPRESENTATIVE_CONTRACT))

    assert "Veri kuralı: 3 (kategori: 3/3)" in output
    assert "Secret yönetimi: 2 yok sayılan yol, 3 olay adımı" in output
    assert "İzin kuralı: 6 (allow: 2, ask: 2, deny: 2)" in output
    assert "Korumalı alan: 3" in output
    assert "Loop sınırı: 3/3" in output
    assert "Kabul kriteri karşılandı" in output


def test_data_classification_requires_three_examples_and_all_decisions():
    invalid = replace(
        REPRESENTATIVE_CONTRACT,
        data_rules=(
            ClassifiedData("Sentetik kayıt", "gönderilebilir", "Gerçek veri içermez ve paylaşılabilir."),
            ClassifiedData("Şema", "gönderilebilir", "Yalnızca alan adlarını ve türleri içerir."),
        ),
    )

    report = validate_contract(invalid)

    assert "Veri sınıflandırması en az 3 örnek içermelidir." in report.errors
    assert any("anonimleştirilerek" in error and "asla" in error for error in report.errors)


def test_every_data_decision_requires_a_concrete_reason():
    rules = list(REPRESENTATIVE_CONTRACT.data_rules)
    rules[0] = replace(rules[0], reason="Güvenli.")

    report = validate_contract(replace(REPRESENTATIVE_CONTRACT, data_rules=tuple(rules)))

    assert "Veri kuralı 1 somut bir gerekçe içermelidir." in report.errors


def test_secret_plan_requires_env_path_and_scanner_location():
    invalid = replace(
        REPRESENTATIVE_CONTRACT,
        secret_plan=SecretPlan(
            ignored_paths=("config.local",),
            scanning_step="Tarama düzenli çalışır.",
            incident_steps=REPRESENTATIVE_CONTRACT.secret_plan.incident_steps,
        ),
    )

    report = validate_contract(invalid)

    assert "Yok sayılan yollar en az bir .env dosyasını açıkça belirtmelidir." in report.errors
    assert "Secret taramasının nerede çalıştığı somut biçimde yazılmalıdır." in report.errors


def test_secret_incident_requires_three_steps_and_rotation_first():
    invalid = replace(
        REPRESENTATIVE_CONTRACT,
        secret_plan=replace(
            REPRESENTATIVE_CONTRACT.secret_plan,
            incident_steps=(
                "Önce git geçmişini ekip üyeleriyle birlikte temizle.",
                "Olay kaydını güvenlik sorumlusuyla paylaş ve incele.",
            ),
        ),
    )

    report = validate_contract(invalid)

    assert "Secret sızıntısı için en az 3 sıralı müdahale adımı yazılmalıdır." in report.errors
    assert "Secret sızıntısının ilk adımı anahtarı iptal etmek olmalıdır." in report.errors


def test_permission_list_requires_five_operations_and_all_decisions():
    only_allow = tuple(
        PermissionRule(f"İşlem {number}", "allow", "Yerel ve geri alınabilir bir işlemdir.")
        for number in range(1, 5)
    )

    report = validate_contract(
        replace(REPRESENTATIVE_CONTRACT, permission_rules=only_allow)
    )

    assert "İzin listesi en az 5 işlem içermelidir." in report.errors
    assert any("ask" in error and "deny" in error for error in report.errors)


def test_permission_rule_rejects_unknown_decision_and_short_reason():
    rules = list(REPRESENTATIVE_CONTRACT.permission_rules)
    rules[0] = replace(rules[0], decision="auto", reason="Gerekli.")

    report = validate_contract(
        replace(REPRESENTATIVE_CONTRACT, permission_rules=tuple(rules))
    )

    assert "İzin kuralı 1 allow, ask veya deny kararı kullanmalıdır." in report.errors
    assert "İzin kuralı 1 somut bir gerekçe içermelidir." in report.errors


def test_protected_paths_require_three_entries_and_reject_allow():
    invalid = replace(
        REPRESENTATIVE_CONTRACT,
        protected_paths=(
            ProtectedPath("auth/", "allow", "Yetkilendirme kodunu içerdiği için korunur."),
            ProtectedPath("payments/", "deny", "Finansal yan etki riski taşıyan işlemleri içerir."),
        ),
    )

    report = validate_contract(invalid)

    assert "Korumalı dosyalar en az 3 yol içermelidir." in report.errors
    assert "Korumalı alan 1 yalnızca ask veya deny kararı kullanmalıdır." in report.errors


@pytest.mark.parametrize(
    ("limits", "expected"),
    [
        (
            LoopLimits("Yalnız test.", "En çok üç deneme yapılır.", "Sentetik veri kullanılır."),
            "Loop yetki sınırı somut bir cümleyle yazılmalıdır.",
        ),
        (
            LoopLimits(
                "Döngü yalnızca yerel test komutunu çalıştırabilir.",
                "Her çalışma dar bir maliyet tavanıyla sınırlıdır.",
                "Döngü yalnızca sentetik vardiya kayıtlarına erişebilir.",
            ),
            "Loop maliyet sınırı sayısal bir tavan içermelidir.",
        ),
    ],
)
def test_loop_limits_require_concrete_sentences_and_numeric_cost(limits, expected):
    report = validate_contract(replace(REPRESENTATIVE_CONTRACT, loop_limits=limits))

    assert expected in report.errors


def test_contract_requires_a_chapter_14_section_reference():
    report = validate_contract(
        replace(
            REPRESENTATIVE_CONTRACT,
            reference_note="Secret sızıntısında önce rotasyon yapılır.",
        )
    )

    assert "Sözleşme Bölüm 14'teki en az bir alt başlığa başvurmalıdır." in report.errors


@pytest.mark.parametrize(
    ("field", "items", "expected"),
    [
        (
            "data_rules",
            (
                *REPRESENTATIVE_CONTRACT.data_rules,
                REPRESENTATIVE_CONTRACT.data_rules[0],
            ),
            "Aynı veri türü birden fazla kez sınıflandırılmamalıdır.",
        ),
        (
            "permission_rules",
            (
                *REPRESENTATIVE_CONTRACT.permission_rules,
                REPRESENTATIVE_CONTRACT.permission_rules[0],
            ),
            "Aynı işlem izin listesinde birden fazla kez yazılmamalıdır.",
        ),
        (
            "protected_paths",
            (
                *REPRESENTATIVE_CONTRACT.protected_paths,
                REPRESENTATIVE_CONTRACT.protected_paths[0],
            ),
            "Aynı korumalı yol birden fazla kez yazılmamalıdır.",
        ),
    ],
)
def test_duplicate_decisions_are_rejected(field, items, expected):
    report = validate_contract(replace(REPRESENTATIVE_CONTRACT, **{field: items}))

    assert expected in report.errors


@pytest.mark.parametrize(
    "unsafe_text",
    [
        "İletişim kişisi kisi@example.com adresidir.",
        "API_KEY=EXAMPLE_SECRET_VALUE",
    ],
)
def test_sensitive_data_patterns_are_rejected(unsafe_text):
    rules = list(REPRESENTATIVE_CONTRACT.data_rules)
    rules[0] = replace(rules[0], reason=unsafe_text)

    report = validate_contract(
        replace(REPRESENTATIVE_CONTRACT, data_rules=tuple(rules))
    )

    assert any("yalnızca temsilî veri kullanın" in error for error in report.errors)


def test_contract_can_be_loaded_from_json_mapping():
    loaded = contract_from_mapping(asdict(REPRESENTATIVE_CONTRACT))

    assert loaded == REPRESENTATIVE_CONTRACT
    assert validate_contract(loaded).is_valid


def test_cli_returns_one_for_invalid_json_contract(tmp_path, capsys):
    contract_file = tmp_path / "sozlesme.json"
    contract = asdict(REPRESENTATIVE_CONTRACT)
    contract["reference_note"] = "Alt başlık referansı yok."
    contract_file.write_text(json.dumps(contract, ensure_ascii=False), encoding="utf-8")

    exit_code = main([str(contract_file)])

    assert exit_code == 1
    assert "Kabul kriteri karşılanmadı" in capsys.readouterr().out


def test_html_is_balanced_and_contains_required_context_and_links():
    html_path = Path(__file__).with_name("security_contract_lab.html")
    html = html_path.read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)

    assert parser.stack == []
    assert "Kavram — Güvenlik Sözleşmesi" in html
    assert "Temsilîlik Notu" in html
    assert "volume: 2" in html
    assert "chapter: 14" in html
    assert 'last_verified: "2026-07"' in html
    assert 'id="validateBtn"' in html
    assert "github.com/adeministratorr/ai-uretim-muhendisligi-companion/blob/main" in html
    assert "github.com/adeministratorr/ai-uretim-muhendisligi-companion/tree/main" in html
    assert "Kitap Destek Deposu ana sayfasına" in html
