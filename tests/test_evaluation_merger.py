from app.git.evaluation_merger import EvaluationMerger


BASE_COMMIT = (
    "76dc6ae7cc1376ea67f8ad3f06125489e2e4888a"
)

TARGET_COMMIT = (
    "0a15a7fd7b030b9a06d511cd9d6add62259e8932"
)


def test_evaluation_merger():

    merger = EvaluationMerger()

    result = merger.merge(
        base_evaluation_path=(
            f"outputs/commits/"
            f"{BASE_COMMIT}/"
            f"validated_evaluation.json"
        ),

        target_evaluation_path=(
            f"outputs/commits/"
            f"{TARGET_COMMIT}/"
            f"reevaluation/"
            f"validated_evaluation.json"
        ),

        selection_path=(
            "outputs/evaluation_selection.json"
        ),
    )

    output_path = (
        f"outputs/commits/"
        f"{TARGET_COMMIT}/"
        f"validated_evaluation.json"
    )

    merger.save_result(
        result,
        output_path,
    )

    print()
    print("=" * 70)
    print("TARGET EVALUATION MERGE")
    print("=" * 70)

    reused = 0
    reevaluated = 0

    for evaluation in result:

        source = evaluation.get(
            "evaluation_source"
        )

        print(
            f"{evaluation.get('ac_id')}: "
            f"{source}"
        )

        if source == "REUSED_FROM_BASE":
            reused += 1

        elif source == "REEVALUATED_TARGET":
            reevaluated += 1

    print()
    print("Summary")
    print("-" * 70)

    print(
        "Total:",
        len(result),
    )

    print(
        "Reused:",
        reused,
    )

    print(
        "Re-evaluated:",
        reevaluated,
    )

    print()
    print("=" * 70)

    print(
        "Output:",
        output_path,
    )

    print("=" * 70)


if __name__ == "__main__":
    test_evaluation_merger()