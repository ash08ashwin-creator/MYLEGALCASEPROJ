import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)


class GeminiGenerator:
    def __init__(self):
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set in the .env file."
            )

        self.client = genai.Client(api_key=api_key)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        jurisdiction: str,
        additional_instructions: str = "",
    ) -> str:

        prompt = f"""
You are a legal document drafting assistant.

Prepare a professional draft of the following document.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS:
{terms}

DATES:
{dates}

JURISDICTION:
{jurisdiction}

ADDITIONAL INSTRUCTIONS:
{additional_instructions}

Requirements:
1. Create a clear professional legal-document draft.
2. Use numbered clauses.
3. Include appropriate headings.
4. Include signature sections.
5. Use placeholders for information that was not provided.
6. Do not invent missing personal information.
7. Do not return JSON.
8. Return only the document text.
9. Include a short disclaimer that the document is a draft and should be reviewed by a qualified legal professional.
"""

        max_retries = 4

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )

                text = getattr(response, "text", None)

                if not text:
                    raise RuntimeError(
                        f"Gemini returned no text. Response: {response!r}"
                    )

                return text.strip()

            except Exception as e:
                error_text = str(e)

                if "503" in error_text or "UNAVAILABLE" in error_text:
                    if attempt < max_retries - 1:
                        wait_time = 5 * (2 ** attempt)

                        print(
                            f"Gemini temporarily unavailable. "
                            f"Retry {attempt + 1}/{max_retries - 1} "
                            f"in {wait_time} seconds..."
                        )

                        time.sleep(wait_time)
                        continue

                raise RuntimeError(
                    f"Gemini API request failed: {e}"
                ) from e