import json
from pathlib import Path


class CandidateRetriever:
    """
    Retrieves candidate files for each Acceptance Criterion.

    Output:
        candidate_cst.json

    Stores only references (file_id + score),
    not the complete file contents.
    """

    def retrieve(
        self,
        requirements_file,
        project_file,
        output_file="outputs/candidate_cst.json"
    ):

        with open(requirements_file, encoding="utf-8") as fp:
            requirements = json.load(fp)

        with open(project_file, encoding="utf-8") as fp:
            project = json.load(fp)

        candidates = []

        for ac in requirements.get("acceptance_criteria", []):

            keywords = [
                str(keyword).lower()
                for keyword in ac.get("keywords", [])
                if str(keyword).strip()
            ]

            ranked_files = []

            for file in project.get("files", []):

                if file.get("parse_status") != "SUCCESS":
                    continue

                if "source_code" not in file or "cst" not in file:
                    continue

                score = self.calculate_score(
                    file,
                    keywords
                )

                if score > 0:

                    ranked_files.append({

                        "file_id": file.get("file_id"),

                        "filename": file.get("filename"),

                        "score": score

                    })

            ranked_files.sort(
                key=lambda item: item["score"],
                reverse=True
            )

            candidates.append({

                "ac_id": ac.get("ac_id"),

                "requirement_id": ac.get("requirement_id"),

                "candidate_files": ranked_files[:5]

            })

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
                candidates,
                fp,
                indent=4,
                ensure_ascii=False
            )

        print(f"Saved : {output_file}")

        return candidates

    def calculate_score(self, file, keywords):

        score = 0

        source = str(
            file.get("source_code", "")
        ).lower()

        for keyword in keywords:

            if keyword in source:
                score += 2

        cst = file.get("cst")

        if cst:
            score += self.score_cst(
                cst,
                keywords
            )

        return score

    def score_cst(self, node, keywords):

        if not isinstance(node, dict):
            return 0

        score = 0

        text = str(
            node.get("text", "")
        ).lower()

        node_type = str(
            node.get("type", "")
        )

        for keyword in keywords:

            if keyword not in text:
                continue

            if node_type in {
                "function_definition",
                "method_declaration"
            }:
                score += 5

            elif node_type in {
                "class_definition",
                "class_declaration"
            }:
                score += 4

            elif node_type == "identifier":
                score += 3

            else:
                score += 1

        for child in node.get("children", []):

            score += self.score_cst(
                child,
                keywords
            )

        return score