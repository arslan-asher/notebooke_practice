import os
from google import genai
from src.schemas import ReviewResult


class CodeAnalyzer:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        self.client = genai.Client(api_key=self.api_key)

    def review_code(self, diff: str, linter_output: str) -> ReviewResult:
        prompt = f"""
        You are an expert AI Code Reviewer and Security Auditor.
        Review the following code diff and linter output.

        Linter Output:
        {linter_output}

        Code Diff:
        {diff}

        Provide a structured code review with high-level summary and specific inline code feedback.
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": ReviewResult,
            },
        )

        return ReviewResult.model_validate_json(response.text)

    def resolve_conflict(
        self, base_code: str, compare_code: str, conflict_diff: str
    ) -> str:
        prompt = f"""
        You are an expert Git Conflict Resolver.
        Resolve the merge conflict between the base branch and compare branch.

        Base Branch Version:
        {base_code}

        Compare Branch Version:
        {compare_code}

        Conflict Diff:
        {conflict_diff}

        Return ONLY the clean, merged code without any Markdown formatting or extra text.
        """

        response = self.client.models.generate_content(
            model = "gemini-1.5-flash",
            contents=prompt,
        )

        return response.text.strip()