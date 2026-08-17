import json
from pathlib import Path


class EvaluationSelector:
    """
    Splits requirements into two groups based on
    impact analysis:

    - AFFECTED / UNCERTAIN -> REEVALUATE
    - SAFE_TO_REUSE -> REUSE
    """

    REEVALUATE_STATUSES = {
        "AFFECTED",
        "UNCERTAIN",
    }

    REUSE_STATUSES = {
        "SAFE_TO_REUSE",
    }

    def select(
        self,
        impact_analysis_path,
    ):
        impact_analysis = self._load_json(
            impact_analysis_path
        )

        reevaluate_ac_ids = []
        reuse_ac_ids = []

        for requirement in impact_analysis.get(
            "requirements",
            [],
        ):
            ac_id = requirement.get("ac_id")
            status = requirement.get("status")

            if not ac_id:
                continue

            if status in self.REEVALUATE_STATUSES:
                reevaluate_ac_ids.append(ac_id)

            elif status in self.REUSE_STATUSES:
                reuse_ac_ids.append(ac_id)

            else:
                # Conservative fallback:
                # unknown statuses should be re-evaluated.
                reevaluate_ac_ids.append(ac_id)

        return {
            "base_commit": impact_analysis.get(
                "base_commit"
            ),
            "target_commit": impact_analysis.get(
                "target_commit"
            ),
            "reevaluate_ac_ids": reevaluate_ac_ids,
            "reuse_ac_ids": reuse_ac_ids,
            "summary": {
                "reevaluate_count": len(
                    reevaluate_ac_ids
                ),
                "reuse_count": len(
                    reuse_ac_ids
                ),
                "total_requirements": (
                    len(reevaluate_ac_ids)
                    + len(reuse_ac_ids)
                ),
            },
        }

    def save_result(
        self,
        result,
        output_path,
    ):
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

    def _load_json(
        self,
        path,
    ):
        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(file)