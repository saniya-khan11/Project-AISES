import json
from pathlib import Path


class RequirementFilter:
    """
    Filters the base requirement set and keeps only
    requirements that must be re-evaluated for the
    target commit.

    Important:
    The output keeps the SAME schema as the normal
    requirements.json produced by RequirementGenerator.

    Input:
    - base requirements.json
    - evaluation_selection.json

    Output:
    - target_requirements.json
    """

    def filter(
        self,
        requirements_path,
        selection_path,
    ):
        requirements_data = self._load_json(
            requirements_path
        )

        selection = self._load_json(
            selection_path
        )

        reevaluate_ac_ids = set(
            selection.get(
                "reevaluate_ac_ids",
                [],
            )
        )

        requirement_items = (
            self._extract_requirement_items(
                requirements_data
            )
        )

        filtered_requirements = []

        for requirement in requirement_items:

            if not isinstance(
                requirement,
                dict,
            ):
                continue

            ac_id = requirement.get(
                "ac_id"
            )

            if ac_id in reevaluate_ac_ids:
                filtered_requirements.append(
                    requirement
                )

        found_ids = {
            requirement.get("ac_id")
            for requirement
            in filtered_requirements
        }

        missing_ids = [
            ac_id
            for ac_id in reevaluate_ac_ids
            if ac_id not in found_ids
        ]

        if missing_ids:
            raise ValueError(
                "The following requirements selected "
                "for re-evaluation were not found in "
                f"the base requirements file: {sorted(missing_ids)}"
            )

        return {
            "project_name": requirements_data.get(
                "project_name",
                "",
            ),
            "project_description": requirements_data.get(
                "project_description",
                "",
            ),
            "acceptance_criteria": filtered_requirements,
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

    def _extract_requirement_items(
        self,
        requirements_data,
    ):
        """
        Supports:

        {
            "acceptance_criteria": [...]
        }

        {
            "requirements": [...]
        }

        or a direct list.
        """

        if isinstance(
            requirements_data,
            list,
        ):
            return requirements_data

        if isinstance(
            requirements_data,
            dict,
        ):
            return requirements_data.get(
                "acceptance_criteria",
                requirements_data.get(
                    "requirements",
                    [],
                ),
            )

        return []