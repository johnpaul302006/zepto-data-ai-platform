from pydantic import BaseModel, Field


class SupportRequest(BaseModel):
    query: str = Field(..., min_length=1)


class SupportResponse(BaseModel):
    answer: str
    sources: list[str] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)