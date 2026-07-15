"""PRD ve proje hafızası doğrulayıcısının kabul ve ret durumları."""

from html.parser import HTMLParser
from pathlib import Path

import pytest

from prd_task_memory_lab import (
    REPRESENTATIVE_DECISIONS,
    REPRESENTATIVE_PRD,
    REPRESENTATIVE_TASKS,
    format_report,
    main,
    validate_documents,
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


def test_representative_documents_meet_acceptance_criteria():
    report = validate_documents(
        REPRESENTATIVE_PRD,
        REPRESENTATIVE_TASKS,
        REPRESENTATIVE_DECISIONS,
    )

    assert report.is_valid
    assert report.errors == ()
    assert report.prd_section_count == 6
    assert report.user_story_count == 2
    assert report.task_count == 5
    assert report.completed_task_count == 2
    assert report.decision_count == 2


def test_report_shows_structural_counts_and_result():
    report = validate_documents(
        REPRESENTATIVE_PRD,
        REPRESENTATIVE_TASKS,
        REPRESENTATIVE_DECISIONS,
    )

    output = format_report(report)
    assert "PRD bölümü: 6/6" in output
    assert "TASKS.md görevi: 5 (tamamlandı: 2)" in output
    assert "Kabul kriteri karşılandı" in output


@pytest.mark.parametrize(
    "heading",
    [
        "Amaç",
        "Hedef Kullanıcı",
        "Kapsam",
        "Teknik Kısıtlar",
        "Out-of-Scope",
        "Başarı Kriterleri",
    ],
)
def test_prd_rejects_missing_required_section(heading):
    invalid_prd = REPRESENTATIVE_PRD.replace(f"## {heading}", f"### {heading}")

    report = validate_documents(
        invalid_prd,
        REPRESENTATIVE_TASKS,
        REPRESENTATIVE_DECISIONS,
    )

    assert any(f'"{heading}" başlığı eksik' in error for error in report.errors)


def test_prd_requires_two_complete_user_stories():
    first_story = (
        "- Vardiyalı çalışan olarak, belirli bir tarih için izin talebi "
        "oluşturabilmek istiyorum ki işletme sahibi planlamayı buna göre yapabilsin.\n"
    )
    invalid_prd = REPRESENTATIVE_PRD.replace(first_story, "")

    report = validate_documents(
        invalid_prd,
        REPRESENTATIVE_TASKS,
        REPRESENTATIVE_DECISIONS,
    )

    assert any("en az iki user story" in error for error in report.errors)


def test_prd_requires_out_of_scope_list_item():
    invalid_prd = REPRESENTATIVE_PRD.replace(
        "- İzin talebini onaylama veya reddetme akışı bu çalışmaya dahil değildir.",
        "Bu bölüm daha sonra doldurulacak.",
    )

    report = validate_documents(
        invalid_prd,
        REPRESENTATIVE_TASKS,
        REPRESENTATIVE_DECISIONS,
    )

    assert any("Out-of-Scope" in error and "liste maddesi" in error for error in report.errors)


def test_prd_requires_ears_like_acceptance_criterion():
    invalid_prd = REPRESENTATIVE_PRD.replace("Ne zaman", "Bir durumda")

    report = validate_documents(
        invalid_prd,
        REPRESENTATIVE_TASKS,
        REPRESENTATIVE_DECISIONS,
    )

    assert any("EARS benzeri" in error for error in report.errors)


def test_tasks_require_at_least_five_items():
    invalid_tasks = "\n".join(REPRESENTATIVE_TASKS.splitlines()[:-1])

    report = validate_documents(
        REPRESENTATIVE_PRD,
        invalid_tasks,
        REPRESENTATIVE_DECISIONS,
    )

    assert any("en az beş" in error for error in report.errors)


def test_tasks_reject_unknown_status_marker():
    invalid_tasks = REPRESENTATIVE_TASKS.replace("- [~]", "- [?]", 1)

    report = validate_documents(
        REPRESENTATIVE_PRD,
        invalid_tasks,
        REPRESENTATIVE_DECISIONS,
    )

    assert any("[ ], [~] veya [x]" in error for error in report.errors)


def test_completed_task_requires_verification_note():
    invalid_tasks = REPRESENTATIVE_TASKS.replace(
        " — doğrulama: `test_leave_request_schema`",
        "",
        1,
    )

    report = validate_documents(
        REPRESENTATIVE_PRD,
        invalid_tasks,
        REPRESENTATIVE_DECISIONS,
    )

    assert any("doğrulama notu" in error for error in report.errors)


def test_tasks_reject_duplicate_descriptions():
    duplicate_line = "- [ ] Geçmiş tarih denetimini uygula"
    invalid_tasks = REPRESENTATIVE_TASKS + duplicate_line + "\n"

    report = validate_documents(
        REPRESENTATIVE_PRD,
        invalid_tasks,
        REPRESENTATIVE_DECISIONS,
    )

    assert any("birden fazla kez" in error for error in report.errors)


def test_decisions_require_expected_table_header():
    invalid_decisions = REPRESENTATIVE_DECISIONS.replace("Gerekçe", "Not")

    report = validate_documents(
        REPRESENTATIVE_PRD,
        REPRESENTATIVE_TASKS,
        invalid_decisions,
    )

    assert any("Tarih | Karar | Gerekçe" in error for error in report.errors)


def test_decisions_require_two_records():
    invalid_decisions = REPRESENTATIVE_DECISIONS.rsplit("\n", 2)[0] + "\n"

    report = validate_documents(
        REPRESENTATIVE_PRD,
        REPRESENTATIVE_TASKS,
        invalid_decisions,
    )

    assert any("en az iki karar" in error for error in report.errors)


@pytest.mark.parametrize(
    ("old_text", "new_text", "expected_error"),
    [
        ("2026-06-24", "24.06.2026", "YYYY-AA-GG"),
        (
            "Push bildirimi altyapısı bu aşamada gereksiz maliyet getiriyor.",
            "Maliyet yüksek.",
            "gerekçesi çok kısa",
        ),
    ],
)
def test_decisions_reject_invalid_date_or_short_reason(
    old_text,
    new_text,
    expected_error,
):
    invalid_decisions = REPRESENTATIVE_DECISIONS.replace(old_text, new_text, 1)

    report = validate_documents(
        REPRESENTATIVE_PRD,
        REPRESENTATIVE_TASKS,
        invalid_decisions,
    )

    assert any(expected_error in error for error in report.errors)


def test_main_reads_three_markdown_files(tmp_path, capsys):
    paths = []
    for filename, content in (
        ("PRD.md", REPRESENTATIVE_PRD),
        ("TASKS.md", REPRESENTATIVE_TASKS),
        ("DECISIONS.md", REPRESENTATIVE_DECISIONS),
    ):
        path = tmp_path / filename
        path.write_text(content, encoding="utf-8")
        paths.append(str(path))

    exit_code = main(paths)

    assert exit_code == 0
    assert "Belge üçlüsü yapısal denetimden geçti" in capsys.readouterr().out


def test_html_has_required_blocks_links_metadata_and_balanced_tags():
    html_path = Path(__file__).with_name("prd_task_memory_lab.html")
    html = html_path.read_text(encoding="utf-8")
    parser = BalancedHTMLParser()
    parser.feed(html)
    parser.close()

    assert parser.stack == []
    assert "Kavram — Yazılı Niyet ve Proje Hafızası" in html
    assert "Temsilîlik Notu" in html
    assert "PRD.md" in html and "TASKS.md" in html and "DECISIONS.md" in html
    assert html.count("https://github.com/adeministratorr/") == 3
    assert 'volume: 2' in html
    assert 'chapter: 08' in html
    assert 'last_verified: "2026-07"' in html
