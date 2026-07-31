import os

from google import genai
from google.genai import types

from .schemas import ConflictResolutionOutput, ReviewOutput


class CodeAnalyzer:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"

    def review_code(self, diff: str, linter_output: str = "") -> ReviewOutput:
        prompt = f"""
You are an expert AI code reviewer. Perform a CodeRabbit-style code review.
Analyze the PR diff and static analysis / linter results provided below.

--- PR DIFF ---
{diff}

--- STATIC ANALYSIS / LINTER OUTPUT ---
{linter_output if linter_output else "No linter errors detected."}

Provide:
1. High-level summary.
2. File-by-file walkthrough.
3. Key code quality & security findings.
4. Line-by-line inline code comments using ```suggestion formatting where applicable.
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ReviewOutput,
                temperature=0.2,
            ),
        )
        return ReviewOutput.model_validate_json(response.text)

    def resolve_conflict(self, filepath: str, conflicted_content: str) -> ConflictResolutionOutput:
        prompt = f"""
You are an expert Git merge conflict resolver.
Resolve the merge conflict in file '{filepath}'.
Remove all git conflict markers (<<<<<<<, =======, >>>>>>>) and integrate both sets of changes logically.

--- CONFLICT FILE CONTENT ---
{conflicted_content}
"""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ConflictResolutionOutput,
                temperature=0.1,
            ),
        )
        return ConflictResolutionOutput.model_validate_json(response.text)