from pathlib import Path


class CodeLoader:

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".java",
        ".js",
        ".ts",
        ".cs",
        ".sql",
        ".json",
        ".yaml",
        ".yml",
        ".xml",
        ".properties"
    }

    IGNORE_FOLDERS = {
        "__pycache__",
        ".git",
        ".idea",
        ".vscode",
        "venv",
        ".venv",
        "node_modules",
        "dist",
        "build",
        "target"
    }

    def load_project(self, project_path):

        project_path = Path(project_path)

        if not project_path.exists():
            raise FileNotFoundError(
                f"Project folder '{project_path}' does not exist."
            )

        files = []

        for file in project_path.rglob("*"):

            if not file.is_file():
                continue

            if any(folder in file.parts for folder in self.IGNORE_FOLDERS):
                continue

            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            files.append({
                "name": file.name,
                "path": str(file),
                "extension": file.suffix.lower(),
                "size": file.stat().st_size
            })

        return files