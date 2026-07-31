import os
import subprocess


class GitManager:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def _run(self, cmd: str) -> str:
        result = subprocess.run(cmd, shell=True, cwd=self.repo_path, capture_output=True, text=True)
        return result.stdout.strip()

    def configure_bot_user(self, name: str = "github-actions[bot]", email: str = "github-actions[bot]@users.noreply.github.com"):
        self._run(f'git config user.name "{name}"')
        self._run(f'git config user.email "{email}"')

    def check_and_get_conflicts(self, target_branch: str = "main") -> dict[str, str]:
        """Merges target branch into current branch without committing to detect conflict files."""
        self.configure_bot_user()
        self._run(f"git fetch origin {target_branch}")
        
        # Attempt merge without committing
        subprocess.run(
            f"git merge origin/{target_branch} --no-commit --no-ff",
            shell=True,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        # Check for unmerged files (conflict status UU, AA, or UT)
        status = self._run("git status --porcelain")
        conflicted_files = {}
        for line in status.splitlines():
            if any(line.startswith(flag) for flag in ["UU ", "AA ", "UT ", "DU ", "UD "]):
                filepath = line[3:].strip()
                if os.path.exists(filepath):
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        conflicted_files[filepath] = f.read()
                        
        return conflicted_files

    def commit_and_push(self, commit_message: str = "style: apply AI auto-fixes [skip ci]"):
        """Commits changes and pushes back to remote branch."""
        self.configure_bot_user()
        self._run("git add .")
        status = self._run("git status --porcelain")
        if not status:
            return False
        self._run(f'git commit -m "{commit_message}"')
        self._run("git push")
        return True