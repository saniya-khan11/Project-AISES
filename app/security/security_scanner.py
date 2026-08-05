import json
import subprocess
import tempfile
from pathlib import Path


class SecurityScanner:
    """
    Executes Bandit on Python source code and returns
    structured security findings.
    """

    def scan(self, source_code):

        if not source_code.strip():
            return []

        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "temp.py"

            file_path.write_text(
                source_code,
                encoding="utf-8"
            )

            result = subprocess.run(
                [
                    "bandit",
                    "-q",
                    "-f",
                    "json",
                    str(file_path)
                ],
                capture_output=True,
                text=True
            )

            if not result.stdout:
                return []

            try:

                report = json.loads(result.stdout)

            except json.JSONDecodeError:

                return []

            return report.get("results", [])