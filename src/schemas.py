from typing import List, Optional
from pydantic import BaseModel, Field


class InlineComment(BaseModel):
    path: str = Field(description="The relative path to the file being reviewed.")
    line: int = Field(description="The line number where the comment applies.")
    body: str = Field(description="The review comment or suggestion.")


class ReviewResult(BaseModel):
    summary: str = Field(description="A high-level summary of the code review.")
    comments: List[InlineComment] = Field(
        default_factory=list,
        description="A list of specific inline review comments.",
    )