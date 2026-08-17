import subprocess
from pathlib import Path


class GitRepository:
    """
    Handles low-level Git repository operations.

    Responsibilities:
    - Validate Git repository
    - Validate commit IDs
    - Resolve short commit IDs to full SHA
    - Execute Git commands
    """

    def __init__(self, repository_path):
        self.repository_path = Path(repository_path).resolve()

        if not self.repository_path.exists():
            raise FileNotFoundError(
                f"Repository path does not exist: {self.repository_path}"
            )

        if not self.is_git_repository():
            raise ValueError(
                f"Not a valid Git repository: {self.repository_path}"
            )

    def _run_git_command(self, arguments):
        """
        Execute a Git command inside the repository.

        Example:
            _run_git_command(["rev-parse", "HEAD"])
        """

        command = ["git"] + arguments

        try:
            result = subprocess.run(
                command,
                cwd=self.repository_path,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )

            return result.stdout.strip()

        except subprocess.CalledProcessError as exc:

            error_message = exc.stderr.strip()

            raise RuntimeError(
                f"Git command failed: {' '.join(command)}\n"
                f"{error_message}"
            ) from exc

    def is_git_repository(self):
        """
        Check whether the supplied path belongs to a Git repository.
        """

        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.repository_path,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            return (
                result.returncode == 0
                and result.stdout.strip().lower() == "true"
            )

        except FileNotFoundError:
            raise RuntimeError(
                "Git executable was not found. "
                "Make sure Git is installed and available in PATH."
            )

    def commit_exists(self, commit_id):
        """
        Check whether a commit exists in the repository.
        """

        result = subprocess.run(
            [
                "git",
                "cat-file",
                "-e",
                f"{commit_id}^{{commit}}",
            ],
            cwd=self.repository_path,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        return result.returncode == 0

    def validate_commit(self, commit_id):
        """
        Validate that a commit exists.

        Raises:
            ValueError if commit does not exist.
        """

        if not commit_id:
            raise ValueError("Commit ID cannot be empty.")

        if not self.commit_exists(commit_id):
            raise ValueError(
                f"Commit does not exist: {commit_id}"
            )

        return True

    def resolve_commit(self, commit_id):
        """
        Convert a short commit ID or reference into the full commit SHA.

        Example:
            81bc402
                ↓
            81bc402a01c9...
        """

        self.validate_commit(commit_id)

        return self._run_git_command(
            ["rev-parse", f"{commit_id}^{{commit}}"]
        )

    def get_current_commit(self):
        """
        Return the full SHA of HEAD.
        """

        return self.resolve_commit("HEAD")

    def get_commit_parent(self, commit_id):
        """
        Return the first parent of a commit.

        Useful later when the user provides only a target commit.
        """

        self.validate_commit(commit_id)

        parent = self._run_git_command(
            ["rev-parse", f"{commit_id}^"]
        )

        return parent