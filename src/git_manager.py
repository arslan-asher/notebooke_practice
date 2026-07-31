import os
import subprocess

class GitManager:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path

    def _run(self, command):
        result = subprocess.run(
            command, shell=True, cwd=self.repo_path, capture_output=True, text=True
        )
        return result.stdout.strip()

    def setup_and_merge(self, head_branch: str, base_branch: str = "main"):
        # Fetch remote updates safely without refspec collisions
        self._run("git fetch origin --prune")
        
        # Checkout the PR head branch cleanly
        self._run(f"git checkout -B {head_branch} origin/{head_branch}")
        
        # Attempt non-commit merge against base branch
        self._run(f"git merge origin/{base_branch} --no-commit --no-ff")
        
        # Return porcelain status to check for conflict markers
        return self._run("git status --porcelain")