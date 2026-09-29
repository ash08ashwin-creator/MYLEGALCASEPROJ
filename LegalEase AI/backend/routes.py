from fastapi import APIRouter, HTTPException
from backend.ai_core.gemini_generator import GeminiGenerator
from backend.schemas import DocumentRequest, DocumentResponse

router = APIRouter(tags=["LegalEase"])
generator = GeminiGenerator()


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest) -> DocumentResponse:
    try:
        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
            jurisdiction=request.jurisdiction,
            additional_instructions=request.additional_instructions,
        )

        return DocumentResponse(
            document_type=request.document_type,
            content=content,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}",
        ) from exc