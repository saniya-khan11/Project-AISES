
import json
from pathlib import Path

from app.git.git_repository import GitRepository

class DiffAnalyzer:
    """
    Compares two Git commits and identifies:
    - changed files
    - change type
    - added line ranges
    - deleted line ranges
    """

    STATUS_MAP = {
        "A": "added",
        "M": "modified",
        "D": "deleted",
        "R": "renamed",
        "C": "copied",
        "T": "type_changed",
    }

    def __init__(self, repository_path):
        self.repository = GitRepository(repository_path)

    def analyze(self, base_commit, target_commit):
        base_sha = self.repository.resolve_commit(base_commit)
        target_sha = self.repository.resolve_commit(target_commit)

        name_status_output = self.repository._run_git_command(
            [
                "diff",
                "--name-status",
                "--find-renames",
                "--find-copies",
                base_sha,
                target_sha,
            ]
        )

        changes = self._parse_name_status(name_status_output)

        for change in changes:
            line_changes = self._get_line_changes(
                base_sha,
                target_sha,
                change,
            )

            change["added_lines"] = line_changes["added_lines"]
            change["deleted_lines"] = line_changes["deleted_lines"]

        return {
            "base_commit": base_sha,
            "target_commit": target_sha,
            "changed_file_count": len(changes),
            "changes": changes,
        }
    def save_result(self, result, output_path):
        """
    Save Git diff analysis result to a JSON file.
    """

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
        exist_ok=True,
    )

        with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
            json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False,
        )

    def _parse_name_status(self, diff_output):
        changes = []

        if not diff_output:
            return changes

        for line in diff_output.splitlines():
            parts = line.split("\t")

            raw_status = parts[0]
            status_code = raw_status[0]

            change_type = self.STATUS_MAP.get(
                status_code,
                "unknown",
            )

            if status_code in {"R", "C"}:
                old_path = parts[1]
                new_path = parts[2]

                similarity = None
                similarity_text = raw_status[1:]

                if similarity_text.isdigit():
                    similarity = int(similarity_text)

                changes.append(
                    {
                        "change_type": change_type,
                        "old_path": old_path,
                        "new_path": new_path,
                        "similarity": similarity,
                    }
                )

            else:
                file_path = parts[1]

                if status_code == "D":
                    old_path = file_path
                    new_path = None

                elif status_code == "A":
                    old_path = None
                    new_path = file_path

                else:
                    old_path = file_path
                    new_path = file_path

                changes.append(
                    {
                        "change_type": change_type,
                        "old_path": old_path,
                        "new_path": new_path,
                    }
                )

        return changes

    def _get_line_changes(
        self,
        base_sha,
        target_sha,
        change,
    ):
        """
        Extract added and deleted line ranges using Git's
        zero-context unified diff.
        """

        file_path = (
            change.get("new_path")
            or change.get("old_path")
        )

        diff_output = self.repository._run_git_command(
            [
                "diff",
                "--unified=0",
                base_sha,
                target_sha,
                "--",
                file_path,
            ]
        )

        added_lines = []
        deleted_lines = []

        for line in diff_output.splitlines():

            if not line.startswith("@@"):
                continue

            old_start, old_count, new_start, new_count = (
                self._parse_hunk_header(line)
            )

            if old_count > 0:
                deleted_lines.append(
                    [
                        old_start,
                        old_start + old_count - 1,
                    ]
                )

            if new_count > 0:
                added_lines.append(
                    [
                        new_start,
                        new_start + new_count - 1,
                    ]
                )

        return {
            "added_lines": added_lines,
            "deleted_lines": deleted_lines,
        }

    def _parse_hunk_header(self, header):
        """
        Parse:

        @@ -3,2 +3,4 @@

        into:

        old_start = 3
        old_count = 2
        new_start = 3
        new_count = 4
        """

        hunk = header.split("@@")[1].strip()

        old_part, new_part = hunk.split(" ")[:2]

        old_start, old_count = self._parse_range(
            old_part
        )

        new_start, new_count = self._parse_range(
            new_part
        )

        return (
            old_start,
            old_count,
            new_start,
            new_count,
        )

    def _parse_range(self, value):
        """
        Examples:

        -3,2  → start=3, count=2
        +5,4  → start=5, count=4
        -3    → start=3, count=1
        +0,0  → start=0, count=0
        """

        value = value[1:]

        if "," in value:
            start, count = value.split(",")
        else:
            start = value
            count = 1

        return int(start), int(count)