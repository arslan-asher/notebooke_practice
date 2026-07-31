import os
import time
from google import genai
from google.genai.errors import APIError
from src.schemas import ReviewResult


class CodeAnalyzer:

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        self.client = genai.Client(api_key=self.api_key)

    def _call_with_retry(self, model: str, contents: str, config: dict = None, retries: int = 3, delay: int = 5):
        """Helper to call Gemini API with simple retry logic for rate limits (429)."""
        for attempt in range(retries):
            try:
                if config:
                    return self.client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=config,
                    )
                return self.client.models.generate_content(
                    model=model,
                    contents=contents,
                )
            except APIError as e:
                if e.code == 429 and attempt < retries - 1:
                    print(f"Rate limited (429). Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                    time.sleep(delay)
                    delay *= 2
                else:
                    raise e

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

        config = {
            "response_mime_type": "application/json",
            "response_schema": ReviewResult,
        }

        response = self._call_with_retry(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
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

        response = self._call_with_retry(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text.strip()