import asyncio

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from agent import run_agent


console = Console()


def main() -> None:
    console.print(
        Panel(
            "[bold]NetDocAI[/bold]\n"
            "Autonomous Network Troubleshooter",
            expand=False,
        )
    )

    console.print()

    problem = Prompt.ask(
        "[bold]Describe your network problem[/bold]"
    ).strip()

    if not problem:
        console.print("[red]No problem provided.[/red]")
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
    console.print("[bold cyan]Investigating...[/bold cyan]")
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