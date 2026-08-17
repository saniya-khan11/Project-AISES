from app.git.impact_analyzer import ImpactAnalyzer


def test_impact_analyzer():

    analyzer = ImpactAnalyzer()

    result = analyzer.analyze(
        git_diff_path="outputs/git_diff.json",

        mapping_path=(
            "outputs/commits/"
            "76dc6ae7cc1376ea67f8ad3f06125489e2e4888a/"
            "validated_mapping.json"
        ),

        changed_nodes_path="outputs/changed_nodes.json",
    )

    analyzer.save_result(
        result,
        "outputs/impact_analysis.json",
    )

    print()
    print("Requirement Impact Analysis")
    print("-" * 60)

    for requirement in result["requirements"]:

        print(
            f"{requirement['ac_id']}: "
            f"{requirement['status']}"
        )

        print(
            "Reason:",
            requirement["reason"],
        )

        print(
            "Mapped Files:",
            requirement["mapped_files"],
        )

        print(
            "Mapped Nodes:",
            requirement["mapped_nodes"],
        )

        print(
            "Changed File Matches:",
            requirement[
                "matched_changed_files"
            ],
        )

        print(
            "Changed Node Matches:",
            requirement[
                "matched_changed_nodes"
            ],
        )

        print("-" * 60)


if __name__ == "__main__":
    test_impact_analyzer()