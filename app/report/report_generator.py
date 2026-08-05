import json
from pathlib import Path


class ReportGenerator:
    """
    Generates the final AISES report in JSON format.
    """

    def generate(

        self,

        requirements_file,

        mapping_file,

        evaluation_file,

        output_file="outputs/report.json"

    ):

        print("=" * 80)
        print("AISES REPORT GENERATOR")
        print("=" * 80)

        with open(requirements_file, encoding="utf-8") as fp:
            requirements = json.load(fp)

        with open(mapping_file, encoding="utf-8") as fp:
            mappings = json.load(fp)

        with open(evaluation_file, encoding="utf-8") as fp:
            evaluations = json.load(fp)

        ########################################################

        total = len(requirements["acceptance_criteria"])

        implemented = 0

        partial = 0

        not_implemented = 0

        report = []

        ########################################################

        evaluation_lookup = {

            item["ac_id"]: item

            for item in evaluations

        }

        mapping_lookup = {

            item["ac_id"]: item

            for item in mappings

        }

        ########################################################

        for requirement in requirements["acceptance_criteria"]:

            ac_id = requirement["ac_id"]

            evaluation = evaluation_lookup.get(ac_id)

            mapping = mapping_lookup.get(ac_id)

            if evaluation is None:

                continue

            status = evaluation["status"]

            if status == "Implemented":

                implemented += 1

            elif status == "Partially Implemented":

                partial += 1

            else:

                not_implemented += 1

            report.append({

                "ac_id": ac_id,

                "requirement_title": requirement["requirement_title"],

                "description": requirement["description"],

                "status": evaluation["status"],

                "confidence": evaluation["confidence"],

                "coverage": evaluation["coverage"],

                "matched_files": mapping.get(

                    "matched_files",

                    []

                ),

                "strengths": evaluation.get(

                    "strengths",

                    []

                ),

                "issues": evaluation.get(

                    "issues",

                    []

                ),

                "recommendations": evaluation.get(

                    "recommendations",

                    []

                )

            })

        ########################################################

        compliance = round(

            (

                implemented

                +

                0.5 * partial

            )

            /

            total

            * 100,

            2

        )

        ########################################################

        final_report = {

            "summary": {

                "total_requirements": total,

                "implemented": implemented,

                "partially_implemented": partial,

                "not_implemented": not_implemented,

                "overall_compliance": compliance

            },

            "requirements": report

        }

        ########################################################

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

                final_report,

                fp,

                indent=4,

                ensure_ascii=False

            )

        print()

        print(f"Saved : {output_file}")

        return final_report