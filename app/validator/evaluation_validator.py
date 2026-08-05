import json
from pathlib import Path


class EvaluationValidator:

    VALID_STATUS = {

        "Implemented",

        "Partially Implemented",

        "Not Implemented"

    }

    def validate(

        self,

        evaluation_file,

        requirements_file,

        output_file="outputs/validated_evaluation.json"

    ):

        with open(evaluation_file, encoding="utf-8") as fp:

            evaluations = json.load(fp)

        with open(requirements_file, encoding="utf-8") as fp:

            requirements = json.load(fp)

        valid_ac = {

            ac["ac_id"]

            for ac in requirements["acceptance_criteria"]

        }

        validated = []

        for item in evaluations:

            ##################################################

            if item["ac_id"] not in valid_ac:

                print(

                    f"[WARNING] Invalid AC removed: {item['ac_id']}"

                )

                continue

            ##################################################

            status = item.get(

                "status",

                ""

            )

            if status not in self.VALID_STATUS:

                print(

                    f"[WARNING] Invalid status for {item['ac_id']}"

                )

                item["status"] = "Not Implemented"

            ##################################################

            confidence = item.get(

                "confidence",

                0

            )

            confidence = max(

                0,

                min(

                    100,

                    confidence

                )

            )

            item["confidence"] = confidence

            ##################################################

            coverage = item.get(

                "coverage",

                0

            )

            coverage = max(

                0,

                min(

                    100,

                    coverage

                )

            )

            item["coverage"] = coverage

            ##################################################

            validated.append(item)

        Path(output_file).parent.mkdir(

            parents=True,

            exist_ok=True

        )

        with open(

            output_file,

            "w",

            encoding="utf-8"

        ) as fp:

            json.dump(

                validated,

                fp,

                indent=4,

                ensure_ascii=False

            )

        print(

            f"Validated evaluation saved to {output_file}"

        )

        return validated