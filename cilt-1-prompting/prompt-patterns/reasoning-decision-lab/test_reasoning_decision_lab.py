from reasoning_decision_lab import (
    ControlThreshold,
    DecisionBranch,
    PilotPlan,
    build_pilot_plan,
    build_pilot_plan_prompt,
    build_tree_of_thoughts_prompt,
    has_number,
    rank_branches,
    recommended_branch,
    score_branch,
    validate_pilot_plan,
)


def test_tree_of_thoughts_prompt_names_branches_and_criteria():
    prompt = build_tree_of_thoughts_prompt()

    assert "Tree of Thoughts" in prompt
    assert "Sefer sıklığını artır" in prompt
    assert "Hattı ikiye böl" in prompt
    assert "Besleyici hat ekle" in prompt
    assert "sefer sıklığı" in prompt
    assert "mahalle erişimi" in prompt
    assert "bütçe kısıtı" in prompt


def test_ranking_prefers_feeder_line_for_default_case():
    evaluations = rank_branches()
    choice = recommended_branch(evaluations)

    assert choice.branch.key == "C"
    assert choice.branch.title == "Besleyici hat ekle"
    assert choice.is_actionable


def test_budget_violation_is_reported_as_blocker():
    branch = DecisionBranch(
        key="D",
        title="Tüm günü sıklaştır",
        description="Sabah ve akşam için çok sayıda ek sefer koy.",
        scores={"peak_load": 5, "access": 1, "budget_fit": 1},
        resources={"vehicles": 3, "drivers": 6},
    )

    evaluation = score_branch(branch)

    assert "araç kısıtı aşıldı: 3/2" in evaluation.blockers
    assert "şoför kısıtı aşıldı: 6/4" in evaluation.blockers
    assert not evaluation.is_actionable


def test_missing_criterion_is_reported():
    branch = DecisionBranch(
        key="E",
        title="Eksik dal",
        description="Kriterlerden biri yazılmamış örnek.",
        scores={"peak_load": 4, "budget_fit": 3},
        resources={"vehicles": 1, "drivers": 2},
    )

    evaluation = score_branch(branch)

    assert evaluation.missing_criteria == ("access",)
    assert not evaluation.is_actionable


def test_pilot_plan_has_measurable_thresholds_and_prompt_sections():
    choice = recommended_branch(rank_branches())
    plan = build_pilot_plan(choice.branch)
    prompt = build_pilot_plan_prompt(plan)

    assert validate_pilot_plan(plan) == []
    assert all(has_number(threshold.target) for threshold in plan.thresholds)
    assert "Plan" in prompt
    assert "Uygulama Sırasında İzlenecek Veri" in prompt
    assert "Kontrol Adımı" in prompt


def test_validation_rejects_vague_threshold_and_missing_failure_action():
    plan = PilotPlan(
        branch_key="C",
        duration_weeks=4,
        plan="Besleyici hat pilotu.",
        data_to_track=("şikâyet sayısı",),
        thresholds=(
            ControlThreshold(
                metric="şikâyet sayısı",
                target="iyileşme olursa",
                failure_action="",
            ),
        ),
    )

    errors = validate_pilot_plan(plan)

    assert "şikâyet sayısı için sayısal eşik bulunmalıdır." in errors
    assert "şikâyet sayısı için karşılanmazsa adımı bulunmalıdır." in errors
