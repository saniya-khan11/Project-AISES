from app.git.requirement_filter import RequirementFilter


def test_requirement_filter():

    requirement_filter = RequirementFilter()

    result = requirement_filter.filter(
        requirements_path=(
            "outputs/commits/"
            "76dc6ae7cc1376ea67f8ad3f06125489e2e4888a/"
            "requirements.json"
        ),
        selection_path=(
            "outputs/evaluation_selection.json"
        ),
    )

    requirement_filter.save_result(
        result,
        "outputs/target_requirements.json",
    )

    criteria = result.get(
        "acceptance_criteria",
        [],
    )

    print()
    print("=" * 60)
    print("TARGET REQUIREMENT FILTER")
    print("=" * 60)

    print()
    print(
        "Requirements selected for re-evaluation:"
    )

    for requirement in criteria:

        print(
            " ",
            requirement.get("ac_id"),
        )

    print()
    print("Total Selected:", len(criteria))

    print()
    print("=" * 60)
    print(
        "Output: outputs/target_requirements.json"
    )
    print("=" * 60)


if __name__ == "__main__":
    test_requirement_filter()