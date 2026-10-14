import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


DEFAULT_GEMINI_MODEL = "gemini-3.6-flash"

CONFIG_DIR = (
    Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    .expanduser()
    / "netdocai"
)

MODEL_FILE = CONFIG_DIR / "model"


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

        model = os.getenv("GEMINI_MODEL", "").strip()

        if not model and MODEL_FILE.is_file():
            model = MODEL_FILE.read_text(encoding="utf-8").strip()

        if not model:
            model = DEFAULT_GEMINI_MODEL

        return cls(
            gemini_api_key=api_key,
            gemini_model=model,
        )


class LazySettings:
    def __getattr__(self, name: str):
        return getattr(Settings.from_env(), name)


settings = LazySettings()

__all__ = ["Settings", "settings", "DEFAULT_GEMINI_MODEL"]