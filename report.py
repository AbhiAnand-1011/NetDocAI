from typing import Any


def build_report(
    problem: str,
    observations: list[dict[str, Any]],
    hypothesis: str,
    conclusion: str,
) -> str:
    network_observations = []
    knowledge_sources = []

    for observation in observations:
        tool = observation["tool"]
        result = observation["result"]

        if tool == "search_docs":
            for section in result.split("\n\n---\n\n"):
                lines = section.splitlines()

                if lines and lines[0].startswith("SOURCE:"):
                    source = lines[0].replace("SOURCE:", "", 1).strip()

                    if source not in knowledge_sources:
                        knowledge_sources.append(source)
        else:
            network_observations.append(
                f"- {tool}: {result}"
            )

    lines = [
        "===================================",
        "       NETDOCAI DIAGNOSTIC REPORT",
        "===================================",
        "",
        "Problem",
        "-------",
        problem,
        "",
        "Network Observations",
        "--------------------",
    ]

    if network_observations:
        lines.extend(network_observations)
    else:
        lines.append("- No network observations recorded.")

    lines.extend(
        [
            "",
            "Knowledge Retrieved",
            "-------------------",
        ]
    )

    if knowledge_sources:
        for source in knowledge_sources:
            lines.append(f"- {source}")
    else:
        lines.append("- No knowledge-base documents used.")

    lines.extend(
        [
            "",
            "Current Assessment",
            "------------------",
            hypothesis or "No explicit hypothesis was formed.",
            "",
            "Diagnosis",
            "---------",
            conclusion or "No final diagnosis was produced.",
            "",
            "===================================",
        ]
    )

    return "\n".join(lines)