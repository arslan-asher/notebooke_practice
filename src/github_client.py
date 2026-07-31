from github import Github

from .schemas import ReviewOutput


class GitHubClient:
    def __init__(self, token: str, repo_name: str, pr_number: int):
        self.token = token
        self.gh = Github(token)
        self.repo = self.gh.get_repo(repo_name)
        self.pr = self.repo.get_pull(pr_number)

    def get_pr_diff(self) -> str:
        """Fetches the raw diff of the pull request."""
        diff_text = ""
        files = self.pr.get_files()
        for f in files:
            diff_text += f"File: {f.filename}\nStatus: {f.status}\n"
            if f.patch:
                diff_text += f"Patch:\n{f.patch}\n"
            diff_text += "-" * 40 + "\n"
        return diff_text

    def post_coderabbit_review(self, review: ReviewOutput):
        # 1. Post top-level PR summary & walkthrough
        body = f"## 🤖 AI Code Review Summary\n\n{review.summary}\n\n"
        body += "### 📋 Walkthrough\n"
        for item in review.walkthrough:
            body += f"- {item}\n"

        if review.key_findings:
            body += "\n### 🔍 Key Findings\n"
            for finding in review.key_findings:
                body += f"- {finding}\n"

        self.pr.create_issue_comment(body)

        # 2. Post inline comments on PR commit diff (if any exist)
        latest_commit = list(self.pr.get_commits())[-1]
        for inline in review.inline_comments:
            try:
                self.pr.create_review_comment(
                    body=inline.suggestion,
                    commit=latest_commit,
                    path=inline.path,
                    line=inline.line,
                )
            except Exception as e:
                print(f"Skipping inline comment on {inline.path}:{inline.line} - {e}")