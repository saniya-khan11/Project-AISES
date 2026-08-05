import re


class APIExtractor:
    """
    Extracts REST API information from Python source code.
    Currently supports FastAPI decorators.

    Future support:
    - Flask
    - Django
    - Spring Boot
    - ExpressJS
    - ASP.NET
    """

    ROUTE_PATTERN = re.compile(
        r'@app\.(get|post|put|delete|patch)\("([^"]+)"\)',
        flags=re.IGNORECASE
    )

    def extract(self, source_code, functions):

        lines = source_code.splitlines()

        for function in functions:

            start = max(0, function.start_line - 4)
            end = function.start_line - 1

            for i in range(start, end):

                line = lines[i].strip()

                match = self.ROUTE_PATTERN.search(line)

                if match:

                    function.http_method = match.group(1).upper()

                    function.api_endpoint = match.group(2)

                    break

        return functions