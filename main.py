import argparse
import os
import sys

from src.analyzer import CodeAnalyzer
from src.git_manager import GitManager
from src.github_client import GitHubClient


def bad_func( a,b ):
    x=1; y=2 # Multiple statements on one line
    return a+b
def main():
    parser = argparse.ArgumentParser(description="AI Code Reviewer & Auto-Fixer")
    parser.add_argument("--mode", choices=["review", "autofix", "resolve-conflicts"], default="review")
    parser.add_argument("--target-branch", default="main")
    args = parser.parse_args()

    gh_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_num = os.getenv("PR_NUMBER")

    analyzer = CodeAnalyzer()
    git_mgr = GitManager()

    if args.mode == "resolve-conflicts":
        print("Checking for merge conflicts...")
        conflicts = git_mgr.check_and_get_conflicts(target_branch=args.target_branch)
        if not conflicts:
            print("No merge conflicts found.")
            return

        for filepath, content in conflicts.items():
            print(f"Resolving conflict in {filepath}...")
            res = analyzer.resolve_conflict(filepath, content)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(res.resolved_code)
        
        git_mgr.commit_and_push(commit_message="fix: resolve merge conflicts via AI [skip ci]")
        print("Conflicts resolved and pushed back successfully.")
        return

    if args.mode == "review":
        if not (gh_token and repo_name and pr_num):
            print("Missing GitHub environment variables for review mode.")
            sys.exit(1)

        gh_client = GitHubClient(gh_token, repo_name, int(pr_num))
        
        # Read linter log if available (from static analysis step)
        linter_output = ""
        if os.path.exists("linter_output.txt"):
            with open("linter_output.txt", "r") as f:
                linter_output = f.read()

        diff = gh_client.get_pr_diff()  # Assuming get_pr_diff is implemented in github_client
        review_result = analyzer.review_code(diff, linter_output)
        gh_client.post_coderabbit_review(review_result)
        print("Review posted successfully.")

if __name__ == "__main__":
    main()



