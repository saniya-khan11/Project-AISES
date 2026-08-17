from app.git.changed_node_analyzer import ChangedNodeAnalyzer


def main():

    print()
    print("=" * 60)
    print("CHANGED NODE ANALYSIS")
    print("=" * 60)

    analyzer = ChangedNodeAnalyzer()

    result = analyzer.analyze(
        git_diff_path="outputs/git_diff.json",
        repository_path=(
          r"C:\Users\lenovo\Desktop\test-git-repos\calculator"
        ),
    )

    analyzer.save_result(
        result,
        "outputs/changed_nodes.json",
    )

    for file_result in result["files"]:

        print()
        print(
            "File:",
            file_result["file"],
        )

        print(
            "Change Type:",
            file_result["change_type"],
        )

        print(
            "Added Lines:",
            file_result["added_lines"],
        )

        print(
            "Deleted Lines:",
            file_result["deleted_lines"],
        )

        print(
            "Status:",
            file_result["status"],
        )

        print("Changed Nodes:")

        changed_nodes = (
            file_result[
                "changed_nodes"
            ]
        )

        if not changed_nodes:
            print("  None")

        for node in changed_nodes:

            print(
                f"  {node['node']} "
                f"({node['start_line']}-"
                f"{node['end_line']})"
            )

    print()
    print("=" * 60)
    print(
        "Output: "
        "outputs/changed_nodes.json"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()