import json
from pathlib import Path

from tree_sitter import Language, Parser
import tree_sitter_python


class ChangedNodeAnalyzer:
    """
    Maps Git changed line ranges to structural Python nodes
    from the target Git repository.

    Current strategy:
    - Read changed files from git_diff.json
    - Read the target file directly from repository_path
    - Parse the target file using Tree-sitter
    - Find function/class nodes overlapping changed lines
    - Prefer function-level nodes over containing classes
    """

    TARGET_NODE_TYPES = {
        "function_definition",
        "class_definition",
    }

    def __init__(self):
        language = Language(
            tree_sitter_python.language()
        )

        self.parser = Parser(language)

    def analyze(
        self,
        git_diff_path,
        repository_path,
    ):
        git_diff = self._load_json(
            git_diff_path
        )

        repository_path = Path(
            repository_path
        )

        results = []

        for change in git_diff.get(
            "changes",
            [],
        ):

            change_type = change.get(
                "change_type"
            )

            file_path = (
                change.get("new_path")
                or change.get("old_path")
            )

            if not file_path:
                continue

            file_path = self._normalize_path(
                file_path
            )

            added_ranges = change.get(
                "added_lines",
                [],
            )

            deleted_ranges = change.get(
                "deleted_lines",
                [],
            )

            target_file = (
                repository_path / file_path
            )

            if not target_file.exists():

                results.append(
                    {
                        "file": file_path,
                        "change_type": change_type,
                        "added_lines": added_ranges,
                        "deleted_lines": deleted_ranges,
                        "changed_nodes": [],
                        "status": "FILE_NOT_FOUND",
                    }
                )

                continue

            if target_file.suffix.lower() != ".py":

                results.append(
                    {
                        "file": file_path,
                        "change_type": change_type,
                        "added_lines": added_ranges,
                        "deleted_lines": deleted_ranges,
                        "changed_nodes": [],
                        "status": "UNSUPPORTED_FILE_TYPE",
                    }
                )

                continue

            source_code = target_file.read_bytes()

            tree = self.parser.parse(
                source_code
            )

            changed_nodes = (
                self._find_changed_nodes(
                    tree.root_node,
                    source_code,
                    added_ranges,
                )
            )

            results.append(
                {
                    "file": file_path,
                    "change_type": change_type,
                    "added_lines": added_ranges,
                    "deleted_lines": deleted_ranges,
                    "changed_nodes": changed_nodes,
                    "status": "ANALYZED",
                }
            )

        return {
            "base_commit": git_diff.get(
                "base_commit"
            ),
            "target_commit": git_diff.get(
                "target_commit"
            ),
            "files": results,
        }

    def save_result(
        self,
        result,
        output_path,
    ):
        output_path = Path(
            output_path
        )

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

    def _load_json(
        self,
        path,
    ):
        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(
                file
            )

    def _find_changed_nodes(
        self,
        root_node,
        source_code,
        changed_ranges,
    ):
        if not changed_ranges:
            return []

        candidates = []

        self._walk_tree(
            node=root_node,
            source_code=source_code,
            changed_ranges=changed_ranges,
            candidates=candidates,
            current_class=None,
        )

        return self._select_best_nodes(
            candidates
        )

    def _walk_tree(
        self,
        node,
        source_code,
        changed_ranges,
        candidates,
        current_class,
    ):
        node_type = node.type

        node_name = self._extract_node_name(
            node,
            source_code,
        )

        class_name = current_class

        if (
            node_type == "class_definition"
            and node_name
        ):
            class_name = node_name

        start_line = (
            node.start_point.row + 1
        )

        end_line = (
            node.end_point.row + 1
        )

        if (
            node_type
            in self.TARGET_NODE_TYPES
            and node_name
            and self._overlaps_changed_lines(
                start_line,
                end_line,
                changed_ranges,
            )
        ):

            qualified_name = node_name

            if (
                node_type
                == "function_definition"
                and class_name
            ):
                qualified_name = (
                    f"{class_name}.{node_name}"
                )

            candidates.append(
                {
                    "node": qualified_name,
                    "node_type": node_type,
                    "start_line": start_line,
                    "end_line": end_line,
                }
            )

        for child in node.children:

            self._walk_tree(
                node=child,
                source_code=source_code,
                changed_ranges=changed_ranges,
                candidates=candidates,
                current_class=class_name,
            )

    def _extract_node_name(
        self,
        node,
        source_code,
    ):
        name_node = node.child_by_field_name(
            "name"
        )

        if name_node is None:
            return None

        return source_code[
            name_node.start_byte:
            name_node.end_byte
        ].decode(
            "utf-8"
        )

    def _overlaps_changed_lines(
        self,
        node_start,
        node_end,
        changed_ranges,
    ):
        for line_range in changed_ranges:

            if (
                not isinstance(
                    line_range,
                    list,
                )
                or len(line_range) != 2
            ):
                continue

            changed_start = (
                line_range[0]
            )

            changed_end = (
                line_range[1]
            )

            if (
                node_start <= changed_end
                and node_end >= changed_start
            ):
                return True

        return False

    def _select_best_nodes(
        self,
        candidates,
    ):
        """
        Prefer function nodes when both a class
        and one of its methods contain the change.
        """

        if not candidates:
            return []

        function_nodes = [
            candidate
            for candidate in candidates
            if candidate.get(
                "node_type"
            ) == "function_definition"
        ]

        selected = (
            function_nodes
            if function_nodes
            else candidates
        )

        unique = []
        seen = set()

        for candidate in selected:

            key = (
                candidate.get("node"),
                candidate.get("start_line"),
                candidate.get("end_line"),
            )

            if key in seen:
                continue

            seen.add(
                key
            )

            unique.append(
                candidate
            )

        return unique

    def _normalize_path(
        self,
        path,
    ):
        return (
            str(path)
            .replace("\\", "/")
            .strip()
        )