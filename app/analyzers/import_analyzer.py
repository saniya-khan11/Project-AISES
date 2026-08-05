from app.models.finding import Finding


class ImportAnalyzer:
    """
    Analyzes project imports.
    """

    def analyze(self, graph):

        findings = []

        for edge in graph.import_edges:

            module = edge["target"]

            if module in graph.file_index:

                findings.append(
                    Finding(
                        rule="IMPORT_PROJECT_MODULE",
                        severity="INFO",
                        file=edge["source"],
                        message=f"Imports project module '{module}'.",
                        evidence={
                            "module": module
                        }
                    ).to_dict()
                )

            else:

                findings.append(
                    Finding(
                        rule="IMPORT_EXTERNAL_OR_MISSING",
                        severity="INFO",
                        file=edge["source"],
                        message=f"Imports external or unresolved module '{module}'.",
                        evidence={
                            "module": module
                        }
                    ).to_dict()
                )

        return findings