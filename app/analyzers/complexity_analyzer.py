from app.config.config import COMPLEXITY_THRESHOLD
from app.metrics.complexity_calculator import ComplexityCalculator
from app.models.finding import Finding


class ComplexityAnalyzer:
    """
    Purpose:
        Detect symbols with high cyclomatic complexity.

    Responsibilities:
        - Compute cyclomatic complexity using the ComplexityCalculator.
        - Compare complexity against the configured threshold.
        - Produce standardized Finding objects for reporting.
    """

    RULE_HIGH_COMPLEXITY = "HIGH_CYCLOMATIC_COMPLEXITY"

    def __init__(self):

        self.calculator = ComplexityCalculator()

    def analyze(self, graph) -> list[dict]:

        findings: list[dict] = []

        for filename, file in graph.files.items():

            if file.get("extension") != ".py":
                continue

            metrics = self.calculator.calculate(
                file.get("content", "")
            ) or []

            for metric in metrics:

                complexity = metric.get("cyclomatic_complexity", 0)

                if complexity <= COMPLEXITY_THRESHOLD:
                    continue

                findings.append(
                    Finding(
                        rule=self.RULE_HIGH_COMPLEXITY,
                        severity="WARNING",
                        file=filename,
                        line=metric.get("line"),
                        message=(
                            f"{metric.get('symbol_type')} "
                            f"'{metric.get('name')}' has cyclomatic "
                            f"complexity {complexity}, exceeding the "
                            f"configured threshold "
                            f"({COMPLEXITY_THRESHOLD}). "
                            f"Rank: {metric.get('rank')}."
                        ),
                        evidence={
                            "symbol": metric.get("name"),
                            "symbol_type": metric.get("symbol_type"),
                            "cyclomatic_complexity": complexity,
                            "rank": metric.get("rank"),
                            "threshold": COMPLEXITY_THRESHOLD,
                        },
                    ).to_dict()
                )

        return findings