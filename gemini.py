import asyncio
from typing import Any

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from config import settings


async def generate_content(
    contents: Any,
    config: types.GenerateContentConfig,
    retries: int = 3,
) -> Any:
    async with genai.Client(api_key=settings.gemini_api_key).aio as client:
        for attempt in range(retries):
            try:
                return await client.models.generate_content(
                    model=settings.gemini_model,
                    contents=contents,
                    config=config,
                )

            except ServerError:
                if attempt == retries - 1:
                    raise

            except ClientError as exc:
                status_code = getattr(exc, "code", None)

                if status_code != 429 or attempt == retries - 1:
                    raise

            delay = 2 ** attempt

            print(
                f"[Gemini] Temporary API failure. "
                f"Retrying in {delay}s..."
            )

            await asyncio.sleep(delay)

    raise RuntimeError("Gemini request failed after all retries.")