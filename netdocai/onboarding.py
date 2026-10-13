import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

API_KEY_URL = "https://aistudio.google.com/apikey"

CONFIG_DIR = (
    Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    .expanduser()
    / "netdocai"
)

KEY_FILE = CONFIG_DIR / "api_key"


def validate_api_key(api_key: str) -> bool | None:
    try:
        with genai.Client(api_key=api_key) as client:
            client.models.list(config={"page_size": 1}).page

        return True

    except errors.APIError as exc:
        if exc.code in (400, 401, 403):
            console.print(
                "\n[red]API key rejected by Google.[/red]"
            )
            return False

        if exc.code == 429 or exc.code >= 500:
            console.print(
                "\n[yellow]Google's API is temporarily unavailable "
                "or rate-limited. Key validation was inconclusive.[/yellow]"
            )
            return None

        console.print(
            f"\n[red]API validation failed with HTTP {exc.code}.[/red]"
        )
        return False

    except Exception:
        console.print(
            "\n[yellow]Could not reach Google's API to validate "
            "the key. Validation was inconclusive.[/yellow]"
        )
        return None


def save_api_key(api_key: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)

    os.chmod(CONFIG_DIR, 0o700)

    fd = os.open(
        KEY_FILE,
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
        0o600,
    )

    with os.fdopen(fd, "w", encoding="utf-8") as file:
        file.write(api_key)

    os.chmod(KEY_FILE, 0o600)


def get_api_key() -> str:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if api_key:
        return api_key

    if KEY_FILE.is_file():
        api_key = KEY_FILE.read_text(encoding="utf-8").strip()

        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
            return api_key

    console.print(
        Panel(
            "[bold cyan]Welcome to NetDocAI![/bold cyan]\n\n"
            "To get started, you need a Google Gemini API key.\n\n"
            "[bold]Get your API key here:[/bold]\n"
            f"[link={API_KEY_URL}]{API_KEY_URL}[/link]\n\n"
            "[dim]Your API key will be stored locally "
            "on your computer.[/dim]",
            title="First-Time Setup",
            border_style="cyan",
            expand=False,
        )
    )

    while True:
        api_key = Prompt.ask(
            "\n[bold green]Enter your Gemini API key[/bold green]",
            password=True,
        ).strip()

        if not api_key:
            console.print(
                "[red]API key cannot be empty.[/red]"
            )
            continue

        console.print(
            "\n[cyan]Validating Gemini API key...[/cyan]"
        )

        status = validate_api_key(api_key)

        if status is False:
            continue

        if status is None:
            proceed = Prompt.ask(
                "[yellow]Save this unverified key anyway?[/yellow]",
                choices=["y", "n"],
                default="n",
            )

            if proceed == "n":
                continue

        save_api_key(api_key)

        os.environ["GEMINI_API_KEY"] = api_key

        if status is True:
            console.print(
                "\n[bold green]✓ API key verified and saved![/bold green]"
            )
        else:
            console.print(
                "\n[bold yellow]✓ API key saved without verification.[/bold yellow]"
            )

        return api_key