import re

from app.models.finding import Finding


class NamingAnalyzer:
    """
    Purpose:
        Analyzes source code naming conventions according to
        Python (PEP 8) standards.

    Responsibilities:
        - Validate function names.
        - Validate method names.
        - Validate class names.
        - Validate variable names.

    Input:
        ProjectKnowledgeGraph

    Output:
        List[Finding]
    """

    SNAKE_CASE = re.compile(r"^[a-z_][a-z0-9_]*$")
    PASCAL_CASE = re.compile(r"^[A-Z][A-Za-z0-9]*$")

    def analyze(self, graph):

        findings = []

        for filename, file in graph.files.items():

            # ---------------------------------------------
            # Skip non-Python files
            # ---------------------------------------------

            if file.get("extension") != ".py":
                continue

            # ---------------------------------------------
            # Functions
            # ---------------------------------------------

            for function in file.get("functions", []):

                name = function["name"]

                if not self.SNAKE_CASE.match(name):

                    findings.append(
                        Finding(
                            rule="INVALID_FUNCTION_NAME",
                            severity="WARNING",
                            file=filename,
                            line=function["line"],
                            message=f"Function '{name}' should use snake_case.",
                            evidence={
                                "function": name
                            }
                        ).to_dict()
                    )

            # ---------------------------------------------
            # Classes
            # ---------------------------------------------

            for cls in file.get("classes", []):

                name = cls["name"]

                if not self.PASCAL_CASE.match(name):

                    findings.append(
                        Finding(
                            rule="INVALID_CLASS_NAME",
                            severity="WARNING",
                            file=filename,
                            line=cls["line"],
                            message=f"Class '{name}' should use PascalCase.",
                            evidence={
                                "class": name
                            }
                        ).to_dict()
                    )

            # ---------------------------------------------
            # Methods
            # ---------------------------------------------

            for class_name, methods in file.get("methods", {}).items():

                for method in methods:

                    name = method["name"]

                    if not self.SNAKE_CASE.match(name):

                        findings.append(
                            Finding(
                                rule="INVALID_METHOD_NAME",
                                severity="WARNING",
                                file=filename,
                                line=method["line"],
                                message=f"Method '{name}' in class '{class_name}' should use snake_case.",
                                evidence={
                                    "class": class_name,
                                    "method": name
                                }
                            ).to_dict()
                        )

            # ---------------------------------------------
            # Variables
            # ---------------------------------------------

            for variable in file.get("variables", []):

                name = variable["name"]

                if not self.SNAKE_CASE.match(name):

                    findings.append(
                        Finding(
                            rule="INVALID_VARIABLE_NAME",
                            severity="INFO",
                            file=filename,
                            line=variable["line"],
                            message=f"Variable '{name}' should use snake_case.",
                            evidence={
                                "variable": name
                            }
                        ).to_dict()
                    )

        return findings