from pathlib import Path


class SourceReader:

    def read_files(self, files):

        project_files = []

        for file in files:

            try:
                content = Path(file["path"]).read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception as e:

                content = ""
                print(f"Error reading {file['path']}: {e}")

            # Copy existing metadata and add content
            file_data = file.copy()
            file_data["content"] = content

            project_files.append(file_data)

        return project_files