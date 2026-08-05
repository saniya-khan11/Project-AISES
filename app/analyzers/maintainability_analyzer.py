from app.config.config import MIN_MAINTAINABILITY_INDEX
from app.metrics.maintainability_calculator import MaintainabilityCalculator
from app.models.finding import Finding


class MaintainabilityAnalyzer:
    """
    Purpose:
        Evaluate the maintainability of Python source files.

    Responsibilities:
        - Calculate Maintainability Index (MI).
        - Compare MI against the configured threshold.
        - Report files with poor maintainability.
    """

    def __init__(self):

        self.calculator = MaintainabilityCalculator()

    def analyze(self, graph):

        findings = []

        for filename, file in graph.files.items():

            if file.get("extension") != ".py":
                continue

            metrics = self.calculator.calculate(
                file.get("content", "")
            )

            if not metrics:
                continue

            maintainability_index = metrics.get(
                "maintainability_index", 100
            )

            if maintainability_index >= MIN_MAINTAINABILITY_INDEX:
                continue

            findings.append(

                Finding(

                    rule="LOW_MAINTAINABILITY",

                    severity="WARNING",

                    file=filename,

                    line=1,

                    message=(
                        f"Maintainability Index "
                        f"({maintainability_index}) is below the "
                        f"configured threshold "
                        f"({MIN_MAINTAINABILITY_INDEX})."
                    ),

                    evidence={

                        "maintainability_index":
                            maintainability_index,

                        "loc":
                            metrics.get("loc"),

                        "sloc":
                            metrics.get("sloc"),

                        "lloc":
                            metrics.get("lloc"),

                        "comments":
                            metrics.get("comments")

                    }

                ).to_dict()

            )

        return findings