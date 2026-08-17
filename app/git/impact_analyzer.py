import json
from pathlib import Path


class ImpactAnalyzer:
    """
    Determines which requirements are affected by changes
    between a base commit and a target commit.

    V2 strategy:

    1. No mapped files
       -> UNCERTAIN

    2. Mapped files did not change
       -> SAFE_TO_REUSE

    3. Mapped file changed but requirement has no mapped nodes
       -> UNCERTAIN

    4. Mapped file changed and one of its mapped nodes changed
       -> AFFECTED

    5. Mapped file changed but none of its mapped nodes changed
       -> SAFE_TO_REUSE

    Conservative principle:
    Reuse previous evaluation only when we have enough evidence
    that the requirement was not affected.
    """

    def analyze(
        self,
        git_diff_path,
        mapping_path,
        changed_nodes_path,
    ):
        git_diff = self._load_json(
            git_diff_path
        )

        mappings = self._load_json(
            mapping_path
        )

        changed_nodes_data = self._load_json(
            changed_nodes_path
        )

        changed_paths = self._extract_changed_paths(
            git_diff
        )

        changed_nodes = self._extract_changed_nodes(
            changed_nodes_data
        )

        mapping_items = self._extract_mapping_items(
            mappings
        )

        results = []

        for mapping in mapping_items:

            ac_id = mapping.get("ac_id")

            mapped_files = self._extract_mapped_files(
                mapping
            )

            mapped_nodes = self._extract_mapped_nodes(
                mapping
            )

            # ----------------------------------------
            # CASE 1
            # No previous file mapping
            # ----------------------------------------

            if not mapped_files:

                results.append(
                    {
                        "ac_id": ac_id,
                        "status": "UNCERTAIN",
                        "reason": (
                            "No mapped files were found "
                            "for this requirement."
                        ),
                        "mapped_files": [],
                        "mapped_nodes": mapped_nodes,
                        "matched_changed_files": [],
                        "matched_changed_nodes": [],
                    }
                )

                continue

            # ----------------------------------------
            # Find mapped files that changed
            # ----------------------------------------

            matched_files = [
                file_path
                for file_path in mapped_files
                if file_path in changed_paths
            ]

            # ----------------------------------------
            # CASE 2
            # None of the requirement files changed
            # ----------------------------------------

            if not matched_files:

                results.append(
                    {
                        "ac_id": ac_id,
                        "status": "SAFE_TO_REUSE",
                        "reason": (
                            "None of the mapped files "
                            "changed between the commits."
                        ),
                        "mapped_files": mapped_files,
                        "mapped_nodes": mapped_nodes,
                        "matched_changed_files": [],
                        "matched_changed_nodes": [],
                    }
                )

                continue

            # ----------------------------------------
            # CASE 3
            # File changed but mapping has no nodes
            # ----------------------------------------

            if not mapped_nodes:

                results.append(
                    {
                        "ac_id": ac_id,
                        "status": "UNCERTAIN",
                        "reason": (
                            "A mapped file changed, but "
                            "no mapped nodes are available "
                            "to determine whether this "
                            "requirement was affected."
                        ),
                        "mapped_files": mapped_files,
                        "mapped_nodes": [],
                        "matched_changed_files": matched_files,
                        "matched_changed_nodes": [],
                    }
                )

                continue

            # ----------------------------------------
            # Compare mapped nodes against
            # target changed nodes
            # ----------------------------------------

            matched_nodes = []

            for file_path in matched_files:

                file_changed_nodes = changed_nodes.get(
                    file_path,
                    set(),
                )

                for mapped_node in mapped_nodes:

                    if mapped_node in file_changed_nodes:

                        matched_nodes.append(
                            mapped_node
                        )

            matched_nodes = list(
                dict.fromkeys(
                    matched_nodes
                )
            )

            # ----------------------------------------
            # CASE 4
            # One or more mapped nodes changed
            # ----------------------------------------

            if matched_nodes:

                results.append(
                    {
                        "ac_id": ac_id,
                        "status": "AFFECTED",
                        "reason": (
                            "One or more mapped code nodes "
                            "changed between the commits."
                        ),
                        "mapped_files": mapped_files,
                        "mapped_nodes": mapped_nodes,
                        "matched_changed_files": matched_files,
                        "matched_changed_nodes": matched_nodes,
                    }
                )

            # ----------------------------------------
            # CASE 5
            # File changed but mapped nodes did not
            # ----------------------------------------

            else:

                results.append(
                    {
                        "ac_id": ac_id,
                        "status": "SAFE_TO_REUSE",
                        "reason": (
                            "The mapped file changed, but "
                            "none of this requirement's "
                            "mapped code nodes changed."
                        ),
                        "mapped_files": mapped_files,
                        "mapped_nodes": mapped_nodes,
                        "matched_changed_files": matched_files,
                        "matched_changed_nodes": [],
                    }
                )

        return {
            "base_commit": git_diff.get(
                "base_commit"
            ),
            "target_commit": git_diff.get(
                "target_commit"
            ),
            "requirements": results,
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

    def _extract_changed_paths(
        self,
        git_diff,
    ):
        changed_paths = set()

        for change in git_diff.get(
            "changes",
            [],
        ):

            old_path = change.get(
                "old_path"
            )

            new_path = change.get(
                "new_path"
            )

            if old_path:

                changed_paths.add(
                    self._normalize_path(
                        old_path
                    )
                )

            if new_path:

                changed_paths.add(
                    self._normalize_path(
                        new_path
                    )
                )

        return changed_paths

    def _extract_changed_nodes(
        self,
        changed_nodes_data,
    ):
        """
        Converts changed_nodes.json into:

        {
            "Calculator.py": {
                "Calculator.calculate"
            }
        }
        """

        result = {}

        for file_item in changed_nodes_data.get(
            "files",
            [],
        ):

            file_path = file_item.get(
                "file"
            )

            if not file_path:
                continue

            file_path = self._normalize_path(
                file_path
            )

            result.setdefault(
                file_path,
                set(),
            )

            for node in file_item.get(
                "changed_nodes",
                [],
            ):

                if not isinstance(
                    node,
                    dict,
                ):
                    continue

                node_name = node.get(
                    "node"
                )

                if node_name:

                    result[file_path].add(
                        node_name
                    )

        return result

    def _extract_mapping_items(
        self,
        mappings,
    ):
        if isinstance(
            mappings,
            list,
        ):
            return mappings

        if isinstance(
            mappings,
            dict,
        ):

            return mappings.get(
                "mappings",
                mappings.get(
                    "requirements",
                    [],
                ),
            )

        return []

    def _extract_mapped_files(
        self,
        mapping,
    ):
        mapped_files = []

        files = mapping.get(
            "matched_files",
            [],
        )

        if isinstance(
            files,
            list,
        ):

            mapped_files.extend(
                files
            )

        normalized = []

        for file_path in mapped_files:

            if not isinstance(
                file_path,
                str,
            ):
                continue

            normalized.append(
                self._normalize_path(
                    file_path
                )
            )

        return list(
            dict.fromkeys(
                normalized
            )
        )

    def _extract_mapped_nodes(
        self,
        mapping,
    ):
        nodes = mapping.get(
            "matched_nodes",
            [],
        )

        if not isinstance(
            nodes,
            list,
        ):
            return []

        normalized = []

        for node in nodes:

            if not isinstance(
                node,
                str,
            ):
                continue

            node = node.strip()

            if node:
                normalized.append(
                    node
                )

        return list(
            dict.fromkeys(
                normalized
            )
        )

    def _normalize_path(
        self,
        path,
    ):
        return (
            str(path)
            .replace("\\", "/")
            .strip()
        )