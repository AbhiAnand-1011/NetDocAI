import asyncio
import os
import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from .onboarding import (
    get_api_key,
    get_model,
    save_model,
)


console = Console()


def configure_model_cli() -> None:
    current_model = get_model()

    console.print(
        Panel(
            f"[bold]Current model:[/bold] {current_model}",
            title="Gemini Model Configuration",
            border_style="cyan",
            expand=False,
        )
    )

    model = Prompt.ask(
        "\n[bold green]Enter new Gemini model[/bold green]",
        default=current_model,
    ).strip()

    if not model:
        model = current_model

    save_model(model)

    os.environ["GEMINI_MODEL"] = model

    console.print(
        f"\n[bold green]✓ Model updated successfully: {model}[/bold green]"
    )


def main() -> None:
    args = sys.argv[1:]

    if args:
        if args == ["config", "model"]:
            try:
                configure_model_cli()
            except (KeyboardInterrupt, EOFError):
                console.print(
                    "\n[yellow]Configuration cancelled.[/yellow]"
                )
            except OSError as exc:
                console.print(
                    f"\n[red]Configuration error: {exc}[/red]"
                )

            return

        console.print(
            "[red]Invalid command.[/red]\n\n"
            "[bold]Usage:[/bold]\n"
            "  netdocai\n"
            "  netdocai config model"
        )
        return

    console.print(
        Panel(
            "[bold]NetDocAI[/bold]\n"
            "Autonomous Network Troubleshooter",
            expand=False,
        )
    )

    console.print()

    try:
        get_api_key()
        model = get_model()

        console.print(
            f"\n[dim]Using Gemini model: {model}[/dim]"
        )

    except (KeyboardInterrupt, EOFError):
        console.print(
            "\n[yellow]Setup cancelled.[/yellow]"
        )
        return

    except OSError as exc:
        console.print(
            f"\n[red]Configuration error: {exc}[/red]"
        )
        return

    from .agent import run_agent

    console.print()

    problem = Prompt.ask(
        "[bold]Describe your network problem[/bold]"
    ).strip()

    if not problem:
        console.print(
            "[red]No problem provided.[/red]"
        )
        return

    console.print()

    console.print(
        Panel(
            problem,
            title="Problem",
            expand=False,
        )
    )

    console.print()

    console.print(
        "[bold cyan]Investigating...[/bold cyan]"
    )

    console.print()

    try:
        with console.status(
            "[bold cyan]NetDocAI is investigating...[/bold cyan]",
            spinner="dots",
        ):
            response = asyncio.run(run_agent(problem))

        console.print()

        console.print(
            Panel(
                response,
                title="NetDocAI Diagnostic Report",
                border_style="green",
            )
        )

    except Exception as exc:
        console.print()

        console.print(
            Panel(
                f"[red]{exc}[/red]",
                title="Agent Error",
                border_style="red",
            )
        )


if __name__ == "__main__":
    main()