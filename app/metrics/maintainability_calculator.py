from radon.metrics import mi_visit
from radon.raw import analyze


class MaintainabilityCalculator:
    """
    Calculates maintainability metrics using Radon.
    """

    def calculate(self, source_code):

        if not source_code.strip():
            return {}

        try:

            maintainability_index = mi_visit(
                source_code,
                multi=True
            )

            raw = analyze(source_code)

            return {

                "maintainability_index": round(
                    maintainability_index,
                    2
                ),

                "loc": raw.loc,

                "sloc": raw.sloc,

                "lloc": raw.lloc,

                "comments": raw.comments,

                "blank_lines": raw.blank

            }

        except Exception:

            return {}