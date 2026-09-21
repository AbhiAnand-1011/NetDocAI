import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

DEFAULT_GEMINI_MODEL = "gemini-3.6-flash"


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str = DEFAULT_GEMINI_MODEL

    @classmethod
    def from_env(cls) -> "Settings":
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError("Missing required environment variable: GEMINI_API_KEY")

        model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)

        return cls(
            gemini_api_key=api_key,
            gemini_model=model,
        )


settings = Settings.from_env()

__all__ = ["Settings", "settings"]