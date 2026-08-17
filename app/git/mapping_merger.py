import json
from pathlib import Path


class MappingMerger:
    """
    Merges base validated mappings with freshly generated
    target mappings.

    SAFE_TO_REUSE:
        use mapping from base commit

    REEVALUATE:
        use mapping from target commit
    """

    def merge(
        self,
        base_mapping_path,
        target_mapping_path,
        selection_path,
    ):
        base_data = self._load_json(
            base_mapping_path
        )

        target_data = self._load_json(
            target_mapping_path
        )

        selection = self._load_json(
            selection_path
        )

        base_items = self._extract_mapping_items(
            base_data
        )

        target_items = self._extract_mapping_items(
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

        # Reuse base mappings
        for ac_id in reuse_ac_ids:

            mapping = base_lookup.get(
                ac_id
            )

            if mapping is None:
                missing_base.append(
                    ac_id
                )
                continue

            merged_item = dict(
                mapping
            )

            merged_item[
                "mapping_source"
            ] = "REUSED_FROM_BASE"

            merged.append(
                merged_item
            )

        # Use target mappings
        for ac_id in reevaluate_ac_ids:

            mapping = target_lookup.get(
                ac_id
            )

            if mapping is None:
                missing_target.append(
                    ac_id
                )
                continue

            merged_item = dict(
                mapping
            )

            merged_item[
                "mapping_source"
            ] = "REMAPPED_TARGET"

            merged.append(
                merged_item
            )

        if missing_base:
            raise ValueError(
                "Missing reusable base mappings "
                f"for AC IDs: {sorted(missing_base)}"
            )

        if missing_target:
            raise ValueError(
                "Missing target mappings "
                f"for AC IDs: {sorted(missing_target)}"
            )

        merged.sort(
            key=self._ac_sort_key
        )

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

    def _extract_mapping_items(
        self,
        data,
    ):
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
            "mappings",
            "requirements",
            "validated_mappings",
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