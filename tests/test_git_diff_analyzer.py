from app.git.diff_analyzer import DiffAnalyzer


REPOSITORY_PATH = r"C:\Users\lenovo\Desktop\test-git-repos\calculator"

BASE_COMMIT = "76dc6ae"
TARGET_COMMIT = "0a15a7f"


def test_git_diff():

    analyzer = DiffAnalyzer(REPOSITORY_PATH)

    result = analyzer.analyze(
        BASE_COMMIT,
        TARGET_COMMIT,
    )

    analyzer.save_result(
        result,
        "outputs/git_diff.json",
    )

    print("\n" + "=" * 60)
    print("GIT DIFF ANALYSIS")
    print("=" * 60)

    print("\nBase Commit:")
    print(result["base_commit"])

    print("\nTarget Commit:")
    print(result["target_commit"])

    print("\nChanged Files:")
    print(result["changed_file_count"])

    print("\nChanges:")

    for change in result["changes"]:

        print("-" * 60)

        print(
            f"Change Type : {change.get('change_type')}"
        )

        print(
            f"Old Path    : {change.get('old_path')}"
        )

        print(
            f"New Path    : {change.get('new_path')}"
        )

        print(
            f"Added Lines : {change.get('added_lines')}"
        )

        print(
            f"Deleted Lines: {change.get('deleted_lines')}"
        )

        if "similarity" in change:
            print(
                f"Similarity  : {change.get('similarity')}"
            )

    print("\n" + "=" * 60)
    print("Git diff saved successfully")
    print("Output: outputs/git_diff.json")
    print("=" * 60)


if __name__ == "__main__":
    test_git_diff()