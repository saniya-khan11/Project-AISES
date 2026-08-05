from app.models.finding import Finding


class DocumentationAnalyzer:
    """
    Purpose:
        Analyzes source code documentation by inspecting module,
        class, function, and method docstrings.

    Responsibilities:
        - Detect missing module docstrings.
        - Detect missing class docstrings.
        - Detect missing function docstrings.
        - Detect missing method docstrings.

    Input:
        ProjectKnowledgeGraph

    Output:
        List[Finding]
    """

    def analyze(self, graph):

        findings = []

        for filename, file in graph.files.items():

            # ---------------------------------------------
            # Module Docstring
            # ---------------------------------------------
            if filename.endswith(".py"):

                if not file.get("module_docstring"):

                    findings.append(
                        Finding(
                            rule="MISSING_MODULE_DOCSTRING",
                            severity="INFO",
                            file=filename,
                            line=1,
                            message="Module is missing a docstring.",
                            evidence={}
                        ).to_dict()
                    )

            # ---------------------------------------------
            # Functions
            # ---------------------------------------------
            for function in file.get("functions", []):

                if not function.get("docstring"):

                    findings.append(
                        Finding(
                            rule="MISSING_FUNCTION_DOCSTRING",
                            severity="INFO",
                            file=filename,
                            line=function["line"],
                            message=f"Function '{function['name']}' is missing a docstring.",
                            evidence={
                                "function": function["name"]
                            }
                        ).to_dict()
                    )

            # ---------------------------------------------
            # Classes
            # ---------------------------------------------
            for cls in file.get("classes", []):

                if not cls.get("docstring"):

                    findings.append(
                        Finding(
                            rule="MISSING_CLASS_DOCSTRING",
                            severity="INFO",
                            file=filename,
                            line=cls["line"],
                            message=f"Class '{cls['name']}' is missing a docstring.",
                            evidence={
                                "class": cls["name"]
                            }
                        ).to_dict()
                    )

            # ---------------------------------------------
            # Methods
            # ---------------------------------------------
            for class_name, methods in file.get("methods", {}).items():

                for method in methods:

                    if not method.get("docstring"):

                        findings.append(
                            Finding(
                                rule="MISSING_METHOD_DOCSTRING",
                                severity="INFO",
                                file=filename,
                                line=method["line"],
                                message=f"Method '{method['name']}' in class '{class_name}' is missing a docstring.",
                                evidence={
                                    "class": class_name,
                                    "method": method["name"]
                                }
                            ).to_dict()
                        )

        return findings