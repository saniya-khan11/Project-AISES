from app.git.evaluation_selector import EvaluationSelector


def test_evaluation_selector():

    selector = EvaluationSelector()

    result = selector.select(
        "outputs/impact_analysis.json"
    )

    selector.save_result(
        result,
        "outputs/evaluation_selection.json",
    )

    print()
    print("=" * 60)
    print("EVALUATION SELECTION")
    print("=" * 60)

    print()
    print("Requirements to Re-evaluate:")

    for ac_id in result["reevaluate_ac_ids"]:
        print(f"  {ac_id}")

    print()
    print("Requirements Safe to Reuse:")

    for ac_id in result["reuse_ac_ids"]:
        print(f"  {ac_id}")

    print()
    print("Summary")
    print("-" * 60)

    print(
        "Re-evaluate:",
        result["summary"]["reevaluate_count"],
    )

    print(
        "Reuse:",
        result["summary"]["reuse_count"],
    )

    print(
        "Total:",
        result["summary"]["total_requirements"],
    )

    print()
    print("=" * 60)
    print(
        "Output: outputs/evaluation_selection.json"
    )
    print("=" * 60)


if __name__ == "__main__":
    test_evaluation_selector()