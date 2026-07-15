"""Context iskeleti doğrulayıcısının temel kabul ve ret durumları."""

from dataclasses import replace

import pytest

from context_skeleton import (
    REQUIRED_DOCUMENTS,
    SAMPLE_DOCUMENTS,
    SAMPLE_MEMORY_LABELS,
    build_output_files,
    summary_lines,
    validate_context_skeleton,
    write_context_skeleton,
)


def test_representative_skeleton_meets_acceptance_criteria():
    assert validate_context_skeleton(SAMPLE_DOCUMENTS, SAMPLE_MEMORY_LABELS) == []


def test_skeleton_rejects_a_missing_document():
    incomplete = dict(SAMPLE_DOCUMENTS)
    del incomplete["rules.md"]

    errors = validate_context_skeleton(incomplete, SAMPLE_MEMORY_LABELS)

    assert "rules.md dosyası eksik." in errors


def test_skeleton_rejects_fewer_than_three_items():
    incomplete = dict(SAMPLE_DOCUMENTS)
    incomplete["PRD.md"] = SAMPLE_DOCUMENTS["PRD.md"][:2]

    errors = validate_context_skeleton(incomplete, SAMPLE_MEMORY_LABELS)

    assert "PRD.md en az 3 madde içermelidir." in errors


def test_memory_label_requires_a_valid_layer_and_reason():
    invalid = (
        replace(SAMPLE_MEMORY_LABELS[0], layer="archive", reason="Kısa"),
        *SAMPLE_MEMORY_LABELS[1:],
    )

    errors = validate_context_skeleton(SAMPLE_DOCUMENTS, invalid)

    assert "1. hafıza maddesi hot veya cold olarak etiketlenmelidir." in errors
    assert "1. hafıza maddesi kısa bir gerekçe cümlesi taşımalıdır." in errors


@pytest.mark.parametrize(
    "unsafe_item",
    [
        "İletişim: kisi@example.com.",
        "API_KEY=gercek-oldugu-varsayilan-deger",
    ],
)
def test_skeleton_rejects_sensitive_data_patterns(unsafe_item):
    unsafe = dict(SAMPLE_DOCUMENTS)
    unsafe["CLAUDE.md"] = (*SAMPLE_DOCUMENTS["CLAUDE.md"], unsafe_item)

    errors = validate_context_skeleton(unsafe, SAMPLE_MEMORY_LABELS)

    assert any("örnek veri kullanın" in error for error in errors)


def test_output_builder_creates_four_documents_and_memory_map():
    output = build_output_files(SAMPLE_DOCUMENTS, SAMPLE_MEMORY_LABELS)

    assert set(REQUIRED_DOCUMENTS).issubset(output)
    assert "MEMORY_MAP.md" in output
    assert "- [ ] Randevu oluşturma API" in output["TASKS.md"]


def test_writer_does_not_overwrite_an_existing_file(tmp_path):
    target = tmp_path / "context"
    target.mkdir()
    (target / "PRD.md").write_text("kullanıcı içeriği", encoding="utf-8")

    with pytest.raises(FileExistsError, match="üzerine yazılmadı"):
        write_context_skeleton(target)

    assert (target / "PRD.md").read_text(encoding="utf-8") == "kullanıcı içeriği"
    assert not (target / "TASKS.md").exists()


def test_summary_reports_document_item_and_layer_counts():
    assert summary_lines(SAMPLE_DOCUMENTS, SAMPLE_MEMORY_LABELS) == (
        "Context İskeleti — 4 dosya / 16 madde",
        "Hafıza Etiketleri — 5 madde (hot=4, cold=1)",
        "Kabul kriteri karşılandı: Context iskeleti doğrulandı.",
    )
