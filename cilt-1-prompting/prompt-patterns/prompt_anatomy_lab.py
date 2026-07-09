"""Cilt 1 Bölüm 3 için prompt anatomisi laboratuvarı.

Gerçek model çağrısı yapmaz. Promptu serbest metin olarak anlamaya çalışmaz;
persona, görev, bağlam, format, kısıt ve başarı kriteri alanlarından oluşan
yapılandırılmış bir tarifi denetler.
"""

from __future__ import annotations

from dataclasses import dataclass
import re


REQUIRED_PARTS = (
    "persona",
    "task",
    "context",
    "output_format",
    "constraints",
    "acceptance_criteria",
)

PART_LABELS = {
    "persona": "persona",
    "task": "görev",
    "context": "bağlam",
    "output_format": "format",
    "constraints": "kısıt",
    "acceptance_criteria": "başarı kriteri",
}

CHECKABLE_MARKERS = (
    "en az",
    "en fazla",
    "her ",
    "hiçbir",
    "yalnızca",
    "olmalı",
    "bulunmalı",
    "geçmemeli",
    "yer almamalı",
)

VARIABLE_PATTERN = re.compile(r"\[([^\[\]]+)\]")


@dataclass(frozen=True)
class PromptRecipe:
    persona: str = ""
    task: str = ""
    context: str = ""
    output_format: str = ""
    constraints: tuple[str, ...] = ()
    acceptance_criteria: tuple[str, ...] = ()
    examples: tuple[str, ...] = ()

    def to_prompt(self) -> str:
        sections = [
            self.persona,
            self.task,
            self.context,
            " ".join(self.constraints),
            self.output_format,
        ]
        if self.examples:
            sections.append("Örnek: " + " ".join(self.examples))
        if self.acceptance_criteria:
            criteria = "; ".join(self.acceptance_criteria)
            sections.append("Kabul kriteri: " + criteria)
        return " ".join(part.strip() for part in sections if part.strip())


@dataclass(frozen=True)
class PromptAudit:
    level: str
    present_parts: tuple[str, ...]
    missing_parts: tuple[str, ...]
    unresolved_variables: tuple[str, ...]
    acceptance_ready: bool


def find_unresolved_variables(text: str) -> tuple[str, ...]:
    found: list[str] = []
    for match in VARIABLE_PATTERN.finditer(text):
        name = match.group(1).strip()
        if name and name not in found:
            found.append(name)
    return tuple(found)


def is_checkable_criterion(text: str) -> bool:
    normalized = text.strip().lower()
    if any(char.isdigit() for char in normalized):
        return True
    return any(marker in normalized for marker in CHECKABLE_MARKERS)


def part_is_present(value: str | tuple[str, ...]) -> bool:
    if isinstance(value, tuple):
        return any(item.strip() for item in value)
    return bool(value.strip())


def recipe_part_map(recipe: PromptRecipe) -> dict[str, str | tuple[str, ...]]:
    return {
        "persona": recipe.persona,
        "task": recipe.task,
        "context": recipe.context,
        "output_format": recipe.output_format,
        "constraints": recipe.constraints,
        "acceptance_criteria": recipe.acceptance_criteria,
    }


def classify_level(present_count: int, acceptance_ready: bool) -> str:
    if present_count <= 1:
        return "zayıf"
    if present_count < len(REQUIRED_PARTS) or not acceptance_ready:
        return "iyi"
    return "profesyonel"


def audit_recipe(recipe: PromptRecipe, rendered_prompt: str = "") -> PromptAudit:
    parts = recipe_part_map(recipe)
    present = tuple(name for name in REQUIRED_PARTS if part_is_present(parts[name]))
    missing = tuple(name for name in REQUIRED_PARTS if name not in present)
    acceptance_ready = bool(recipe.acceptance_criteria) and all(
        is_checkable_criterion(item) for item in recipe.acceptance_criteria
    )

    return PromptAudit(
        level=classify_level(len(present), acceptance_ready),
        present_parts=present,
        missing_parts=missing,
        unresolved_variables=find_unresolved_variables(rendered_prompt),
        acceptance_ready=acceptance_ready,
    )


def render_recipe(recipe: PromptRecipe, values: dict[str, str]) -> str:
    template = recipe.to_prompt()
    variables = find_unresolved_variables(template)
    missing = tuple(name for name in variables if not values.get(name, "").strip())
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Eksik değişken: {joined}")

    rendered = template
    for name in variables:
        rendered = rendered.replace(f"[{name}]", values[name].strip())
    return rendered


def rival_comparison_recipe() -> PromptRecipe:
    return PromptRecipe(
        persona="Bir stratejik danışman gibi değerlendir.",
        task=(
            "[şirket adı] için, [rakip_listesi] rakiplerini "
            "[karşılaştırma_ölçütleri] ölçütlerine göre karşılaştıran bir tablo hazırla."
        ),
        context=(
            "Okuyucu [okuyucu_rolü]; çıktı [kullanım_amacı] için kullanılacak. "
            "Yalnızca [veri_kaynağı] içindeki bilgileri kullan."
        ),
        output_format=(
            "Çıktıyı tablo olarak ver; sütunlar: Rakip, [ölçüt_1], [ölçüt_2], "
            "Tehdit Düzeyi."
        ),
        constraints=(
            "Kaynağı belirsiz sayısal iddia üretme; eksik veri varsa "
            '"veri mevcut değil" yaz.',
            "Tablo bir sayfayı geçmesin, ton nesnel ve kurumsal olsun.",
        ),
        acceptance_criteria=(
            "[rakip_listesi] içindeki her rakip tabloda bir satırla temsil edilmeli.",
            "Her satırda en az bir sayısal veya kaynaklı veri bulunmalı.",
            "Tablo dışında ek metin yer almamalı.",
        ),
    )


def example_values() -> dict[str, str]:
    return {
        "şirket adı": "Şirketimiz",
        "rakip_listesi": "A, B, C, D, E",
        "karşılaştırma_ölçütleri": "fiyat konumu ve pazar payı",
        "okuyucu_rolü": "proje ortağı",
        "kullanım_amacı": "yarınki yönetim toplantısı",
        "veri_kaynağı": "ekteki şirket verisi ve halka açık raporlar",
        "ölçüt_1": "Fiyat Konumu",
        "ölçüt_2": "Pazar Payı",
    }


def weak_recipe() -> PromptRecipe:
    return PromptRecipe(task="Rakip analizi yap.")


def good_recipe() -> PromptRecipe:
    return PromptRecipe(
        task="Beş ana rakibimizi fiyat ve pazar payına göre karşılaştır.",
        output_format="Çıktıyı tablo olarak ver.",
    )


def format_audit(name: str, audit: PromptAudit) -> str:
    missing = ", ".join(PART_LABELS[item] for item in audit.missing_parts) or "yok"
    variables = ", ".join(audit.unresolved_variables) or "yok"
    return "\n".join(
        [
            f"== {name} ==",
            f"Düzey: {audit.level}",
            f"Eksik parçalar: {missing}",
            f"Açık değişken: {variables}",
        ]
    )


def demo() -> None:
    professional = rival_comparison_recipe()
    rendered = render_recipe(professional, example_values())
    scenarios = (
        ("Zayıf tarif", weak_recipe(), ""),
        ("İyi tarif", good_recipe(), ""),
        ("Profesyonel tarif", professional, rendered),
    )

    for name, recipe, text in scenarios:
        print(format_audit(name, audit_recipe(recipe, text)))
        print()


if __name__ == "__main__":
    demo()
