import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_GEMINI_MODEL = "gemini-3.6-flash"


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str
    gemini_model: str = DEFAULT_GEMINI_MODEL

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY", "").strip()

        if not api_key:
            raise RuntimeError(
                "Missing required environment variable: GEMINI_API_KEY"
            )

        model = os.getenv(
            "GEMINI_MODEL",
            DEFAULT_GEMINI_MODEL,
        )

        return cls(
            gemini_api_key=api_key,
            gemini_model=model,
        )


class LazySettings:
    def __getattr__(self, name: str):
        return getattr(Settings.from_env(), name)


settings = LazySettings()

__all__ = ["Settings", "settings"]