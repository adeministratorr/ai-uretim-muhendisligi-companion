"""Rule dosyası doğrulayıcısının kabul ve ret durumları."""

from html.parser import HTMLParser
from pathlib import Path

import pytest

from rule_enforcement_lab import (
    REPRESENTATIVE_RULE_FILE,
    format_report,
    main,
    validate_rule_file,
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


def _replace_section(markdown: str, heading: str, replacement: str) -> str:
    """Bir ikinci düzey başlığın içeriğini test girdisiyle değiştirir."""

    marker = f"## {heading}\n"
    start = markdown.index(marker) + len(marker)
    next_heading = markdown.find("\n## ", start)
    end = len(markdown) if next_heading == -1 else next_heading
    return markdown[:start] + "\n" + replacement.strip() + "\n" + markdown[end:]


def test_representative_rule_file_meets_acceptance_criteria():
    report = validate_rule_file(REPRESENTATIVE_RULE_FILE)

    assert report.is_valid
    assert report.errors == ()
    assert report.summary_count == 2
    assert report.forbidden_count == 3
    assert report.validation_count == 3
    assert report.breaker_count == 1
    assert report.deny_count == 1
    assert report.compiled_count == 2


def test_report_shows_counts_and_success_result():
    output = format_report(validate_rule_file(REPRESENTATIVE_RULE_FILE))

    assert "Yasak işlem: 3 ([deny]: 1)" in output
    assert "Doğrulama adımı: 3 ([compiled]: 2)" in output
    assert "Kabul kriteri karşılandı" in output


@pytest.mark.parametrize(
    "heading",
    [
        "Proje Özeti",
        "Yasak İşlemler",
        "Zorunlu Doğrulama Adımları",
        "PR Devre Kesici",
    ],
)
def test_required_section_cannot_be_missing(heading):
    invalid = REPRESENTATIVE_RULE_FILE.replace(f"## {heading}", f"### {heading}")

    report = validate_rule_file(invalid)

    assert f'"{heading}" başlığı eksik.' in report.errors


@pytest.mark.parametrize(
    "summary",
    [
        "- Yığın: Laravel API kullanılır.",
        """- Yığın: Laravel API kullanılır.
- Mimari: İş mantığı servis katmanında tutulur.
- Dil: Kullanıcı metinleri Türkçedir.
- Test: Her değişiklik yerel olarak sınanır.""",
    ],
)
def test_project_summary_requires_two_or_three_items(summary):
    invalid = _replace_section(REPRESENTATIVE_RULE_FILE, "Proje Özeti", summary)

    report = validate_rule_file(invalid)

    assert "Proje Özeti, 2-3 dolu liste maddesi içermelidir." in report.errors


def test_project_summary_names_stack_and_architecture():
    invalid = _replace_section(
        REPRESENTATIVE_RULE_FILE,
        "Proje Özeti",
        """- Uygulama küçük işletmeler için hazırlanır.
- Kullanıcı metinleri Türkçe yazılır.""",
    )

    report = validate_rule_file(invalid)

    assert "Proje Özeti teknoloji yığınını açıkça belirtmelidir." in report.errors
    assert "Proje Özeti temel mimari kararı açıkça belirtmelidir." in report.errors


def test_forbidden_section_requires_three_rules():
    invalid = _replace_section(
        REPRESENTATIVE_RULE_FILE,
        "Yasak İşlemler",
        """- [deny] `.env` dosyasını okuma veya içeriğini çıktıya yazma.
- [directive] Yeni bir e-posta sağlayıcısı ya da bildirim paketi ekleme.""",
    )

    report = validate_rule_file(invalid)

    assert "Yasak İşlemler en az 3 madde içermelidir." in report.errors


def test_at_least_one_forbidden_rule_uses_deny_layer():
    invalid = REPRESENTATIVE_RULE_FILE.replace("[deny]", "[directive]")

    report = validate_rule_file(invalid)

    assert "En az bir yasak işlem [deny] katmanına bağlanmalıdır." in report.errors


def test_validation_section_requires_three_steps():
    invalid = _replace_section(
        REPRESENTATIVE_RULE_FILE,
        "Zorunlu Doğrulama Adımları",
        """- [compiled] Backend değişikliğinden sonra `php artisan test` komutunu çalıştır.
- [directive] Sonucu sunmadan önce diff'i kapsam açısından incele.""",
    )

    report = validate_rule_file(invalid)

    assert "Zorunlu Doğrulama Adımları en az 3 madde içermelidir." in report.errors


def test_at_least_one_validation_step_uses_compiled_layer():
    invalid = REPRESENTATIVE_RULE_FILE.replace("[compiled]", "[directive]")

    report = validate_rule_file(invalid)

    assert "En az bir doğrulama adımı [compiled] katmanına bağlanmalıdır." in report.errors


def test_rule_requires_an_allowed_layer_tag():
    invalid = REPRESENTATIVE_RULE_FILE.replace(
        "[deny] `.env`", "[compiled] `.env`", 1
    )

    report = validate_rule_file(invalid)

    assert any(
        "Yasak İşlemler 1. maddesi" in error and "[deny]" in error
        for error in report.errors
    )


@pytest.mark.parametrize(
    ("breaker", "expected"),
    [
        (
            "- [pr-stop] Kimlik doğrulama değişiklikleri insan tarafından incelenir.",
            "durma koşulunu açıkça yazmalıdır",
        ),
        (
            "- [pr-stop] Eğer `auth/` altındaki bir dosya değişirse insan incelemesi gerekir.",
            "PR'ın duracağını belirtmelidir",
        ),
    ],
)
def test_pr_breaker_names_condition_and_stop_result(breaker, expected):
    invalid = _replace_section(REPRESENTATIVE_RULE_FILE, "PR Devre Kesici", breaker)

    report = validate_rule_file(invalid)

    assert any(expected in error for error in report.errors)


def test_duplicate_rule_is_rejected():
    duplicate = (
        "- [compiled] Backend değişikliğinden sonra `php artisan test` komutunu çalıştır."
    )
    invalid = _replace_section(
        REPRESENTATIVE_RULE_FILE,
        "PR Devre Kesici",
        "- [pr-stop] Eğer test başarısızsa PR durur.\n" + duplicate,
    )

    report = validate_rule_file(invalid)

    assert "Aynı davranış kuralı birden fazla bölümde yinelenmemelidir." in report.errors


@pytest.mark.parametrize(
    "unsafe_text",
    [
        "Geliştirici: kisi@example.com",
        "API_KEY=gercek-oldugu-varsayilan-deger",
    ],
)
def test_sensitive_data_patterns_are_rejected(unsafe_text):
    invalid = _replace_section(
        REPRESENTATIVE_RULE_FILE,
        "Proje Özeti",
        f"""- Yığın: Laravel API ve React admin paneli kullanılır.
- Mimari: Servis katmanı kullanılır. {unsafe_text}""",
    )

    report = validate_rule_file(invalid)

    assert any("örnek veri kullanın" in error for error in report.errors)


def test_cli_returns_one_for_invalid_file(tmp_path, capsys):
    rule_file = tmp_path / "AGENTS.md"
    rule_file.write_text("# Eksik Rule Dosyası\n", encoding="utf-8")

    exit_code = main([str(rule_file)])

    assert exit_code == 1
    assert "Kabul kriteri karşılanmadı" in capsys.readouterr().out


def test_html_is_balanced_and_contains_required_context_and_links():
    html_path = Path(__file__).with_name("rule_enforcement_lab.html")
    html = html_path.read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)

    assert parser.stack == []
    assert "Kavram — Yönergeden Otomatik Denetime" in html
    assert "Temsilîlik Notu" in html
    assert "volume: 2" in html
    assert "chapter: 09" in html
    assert 'last_verified: "2026-07"' in html
    assert "github.com/adeministratorr/ai-uretim-muhendisligi-companion/blob/main" in html
    assert "github.com/adeministratorr/ai-uretim-muhendisligi-companion/tree/main" in html
    assert "Kitap Destek Deposu ana sayfasına" in html
