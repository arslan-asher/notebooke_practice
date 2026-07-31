
from pydantic import BaseModel, Field


class InlineComment(BaseModel):
    path: str = Field(description="File path relative to repository root")
    line: int = Field(description="Line number for the comment")
    suggestion: str = Field(description="Detailed suggestion or markdown code snippet using ```suggestion")

class ReviewOutput(BaseModel):
    summary: str = Field(description="High-level overview of the pull request changes")
    walkthrough: list[str] = Field(description="Step-by-step breakdown of changes per file")
    key_findings: list[str] = Field(description="Key issues, code quality concerns, or security bugs")
    inline_comments: list[InlineComment] = Field(default=[], description="Specific line-by-line code suggestions")

class ConflictResolutionOutput(BaseModel):
    resolved_code: str = Field(description="Full resolved file content with conflict markers removed")
    explanation: str = Field(description="Brief explanation of how the conflict was resolved")