from pathlib import Path


class ProjectLoader:

    SUPPORTED_EXTENSIONS = {

        ".py": "python",

        ".java": "java",

        ".js": "javascript",

        ".ts": "typescript",

        ".cpp": "cpp",

        ".c": "c",

        ".cs": "c_sharp",

        ".go": "go",

        ".rs": "rust"

    }

    IGNORE = {

        ".git",

        "__pycache__",

        "venv",

        ".venv",

        "node_modules",

        "dist",

        "build",

        "target"

    }

    def load(self, project_path):

        project = Path(project_path)

        files = []

        file_id = 1

        for file in project.rglob("*"):

            if not file.is_file():
                continue

            if any(folder in file.parts for folder in self.IGNORE):
                continue

            extension = file.suffix.lower()

            if extension not in self.SUPPORTED_EXTENSIONS:
                continue

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception:

                source = ""

            files.append({

                "file_id": f"FILE-{file_id:03d}",

                "filename": file.name,

                "path": str(file),

                "extension": extension,

                "language": self.SUPPORTED_EXTENSIONS[extension],

                "size": file.stat().st_size,

                "source_code": source

            })

            file_id += 1

        return files