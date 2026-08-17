import json
from pathlib import Path


class EvaluationMerger:
    """
    Merges base evaluation results with freshly
    re-evaluated target results.

    SAFE_TO_REUSE:
        Use evaluation from base commit.

    REEVALUATE:
        Use fresh evaluation from target commit.

    Output format intentionally matches the normal
    validated_evaluation.json schema: a direct list.
    """

    def merge(
        self,
        base_evaluation_path,
        target_evaluation_path,
        selection_path,
    ):
        base_data = self._load_json(
            base_evaluation_path
        )

        target_data = self._load_json(
            target_evaluation_path
        )

        selection = self._load_json(
            selection_path
        )

        base_items = self._extract_evaluation_items(
            base_data
        )

        target_items = self._extract_evaluation_items(
            target_data
        )

        reuse_ac_ids = set(
            selection.get(
                "reuse_ac_ids",
                [],
            )
        )

        reevaluate_ac_ids = set(
            selection.get(
                "reevaluate_ac_ids",
                [],
            )
        )

        base_lookup = {
            item.get("ac_id"): item
            for item in base_items
            if isinstance(item, dict)
            and item.get("ac_id")
        }

        target_lookup = {
            item.get("ac_id"): item
            for item in target_items
            if isinstance(item, dict)
            and item.get("ac_id")
        }

        merged = []

        missing_base = []
        missing_target = []

        ########################################################
        # Reuse safe base evaluations
        ########################################################

        for ac_id in reuse_ac_ids:

            evaluation = base_lookup.get(
                ac_id
            )

            if evaluation is None:
                missing_base.append(
                    ac_id
                )
                continue

            merged_item = dict(
                evaluation
            )

            merged_item[
                "evaluation_source"
            ] = "REUSED_FROM_BASE"

            merged.append(
                merged_item
            )

        ########################################################
        # Use target re-evaluations
        ########################################################

        for ac_id in reevaluate_ac_ids:

            evaluation = target_lookup.get(
                ac_id
            )

            if evaluation is None:
                missing_target.append(
                    ac_id
                )
                continue

            merged_item = dict(
                evaluation
            )

            merged_item[
                "evaluation_source"
            ] = "REEVALUATED_TARGET"

            merged.append(
                merged_item
            )

        ########################################################
        # Safety validation
        ########################################################

        if missing_base:
            raise ValueError(
                "Missing reusable base evaluations "
                f"for AC IDs: {sorted(missing_base)}"
            )

        if missing_target:
            raise ValueError(
                "Missing target evaluations "
                f"for AC IDs: {sorted(missing_target)}"
            )

        ########################################################
        # Sort AC-001, AC-002, ...
        ########################################################

        merged.sort(
            key=self._ac_sort_key
        )

        # IMPORTANT:
        # Return direct list so it matches normal
        # validated_evaluation.json format.
        return merged

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

    def _extract_evaluation_items(
        self,
        data,
    ):
        """
        Supports both direct-list and wrapped
        evaluation structures.
        """

        if isinstance(
            data,
            list,
        ):
            return data

        if not isinstance(
            data,
            dict,
        ):
            return []

        for key in [
            "validated_evaluations",
            "evaluations",
            "requirements",
            "results",
        ]:

            items = data.get(
                key
            )

            if isinstance(
                items,
                list,
            ):
                return items

        return []

    def _ac_sort_key(
        self,
        item,
    ):
        ac_id = item.get(
            "ac_id",
            "",
        )

        try:
            return int(
                ac_id.split("-")[-1]
            )

        except (
            ValueError,
            IndexError,
        ):
            return 999999