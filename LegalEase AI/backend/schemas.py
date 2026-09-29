from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=5000)
    terms: str = Field(..., min_length=2, max_length=10000)
    dates: str = Field(..., min_length=2, max_length=500)
    jurisdiction: str = Field(
        default="Not specified",
        max_length=300,
    )
    additional_instructions: str = Field(
        default="",
        max_length=5000,
    )


class DocumentResponse(BaseModel):
    document_type: str
    content: str