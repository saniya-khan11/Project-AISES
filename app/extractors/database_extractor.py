import re


class DatabaseExtractor:
    """
    Extracts basic database operations from Python source code.
    Supports:
    - SQLAlchemy
    - SQL queries
    """

    SQL_KEYWORDS = {

        "SELECT",

        "INSERT",

        "UPDATE",

        "DELETE",

    }

    ORM_PATTERN = re.compile(
        r"\bquery\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)"
    )

    SQL_PATTERN = re.compile(
        r"(SELECT|INSERT|UPDATE|DELETE)",
        flags=re.IGNORECASE
    )

    def extract(self, source_code, functions):

        lines = source_code.splitlines()

        for function in functions:

            start = function.start_line - 1

            end = function.end_line

            for line in lines[start:end]:

                orm_match = self.ORM_PATTERN.search(line)

                if orm_match:

                    table = orm_match.group(1)

                    if table not in function.database_tables:

                        function.database_tables.append(table)

                sql_match = self.SQL_PATTERN.search(line)

                if sql_match:

                    operation = sql_match.group(1).upper()

                    if operation not in function.database_operations:

                        function.database_operations.append(operation)

        return functions