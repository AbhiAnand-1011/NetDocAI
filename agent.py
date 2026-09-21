import os
import sys
from typing import Any, TypedDict

from google.genai import types
from gemini import generate_content
from langgraph.graph import END, START, StateGraph
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from prompts import SYSTEM_PROMPT, build_user_prompt
from report import build_report


MAX_STEPS = 8


class AgentState(TypedDict):
    problem: str
    history: list[dict[str, Any]]
    tool_definitions: list[dict[str, Any]]
    pending_calls: list[dict[str, Any]]
    observations: list[dict[str, Any]]
    hypothesis: str
    response: str
    steps: int


def build_mcp_tools(
    tool_definitions: list[dict[str, Any]],
) -> list[types.Tool]:
    declarations = []

    for tool in tool_definitions:
        declarations.append(
            types.FunctionDeclaration(
                name=tool["name"],
                description=tool["description"],
                parameters_json_schema=tool["input_schema"],
            )
        )

    return [types.Tool(function_declarations=declarations)]


async def get_tool_definitions() -> list[dict[str, Any]]:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.list_tools()

            return [
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "input_schema": tool.input_schema,
                }
                for tool in result.tools
            ]


async def plan(state: AgentState) -> AgentState:
    contents = [
        types.Content.model_validate(message)
        for message in state["history"]
    ]

    gemini_tools = build_mcp_tools(state["tool_definitions"])

    response = await generate_content(
        contents=contents,
        config=types.GenerateContentConfig(
            tools=gemini_tools,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )

    function_calls = response.function_calls

    if not function_calls:
        print("[Agent] Finalizing diagnosis...")

        report = build_report(
            problem=state["problem"],
            observations=state["observations"],
            hypothesis=state["hypothesis"],
            conclusion=response.text or "",
        )

        return {
            **state,
            "response": report,
            "pending_calls": [],
        }

    model_content = response.candidates[0].content

    updated_history = [
        *state["history"],
        model_content.model_dump(exclude_none=True),
    ]

    pending_calls = [
        {
            "name": call.name,
            "args": call.args or {},
        }
        for call in function_calls
    ]

    print(
        "[Agent] "
        + ", ".join(call["name"] for call in pending_calls)
    )

    return {
        **state,
        "history": updated_history,
        "pending_calls": pending_calls,
        "steps": state["steps"] + 1,
    }


async def execute_tools(state: AgentState) -> AgentState:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
        env=os.environ.copy(),
    )

    updated_history = list(state["history"])
    observations = list(state["observations"])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            for call in state["pending_calls"]:
                name = call["name"]
                arguments = call["args"]

                print(f"[Tool] Executing {name}...")

                result = await session.call_tool(
                    name,
                    arguments=arguments,
                )

                result_text = "\n".join(
                    content.text
                    for content in result.content
                    if hasattr(content, "text") and content.text
                )

                if not result_text:
                    result_text = "Tool returned no text result."

                print(f"[Tool] {name} completed.")

                observations.append(
                    {
                        "tool": name,
                        "arguments": arguments,
                        "result": result_text,
                    }
                )

                function_response = types.Part.from_function_response(
                    name=name,
                    response={"result": result_text},
                )

                updated_history.append(
                    types.Content(
                        role="user",
                        parts=[function_response],
                    ).model_dump(exclude_none=True)
                )

    return {
        **state,
        "history": updated_history,
        "observations": observations,
        "pending_calls": [],
    }


async def assess(state: AgentState) -> AgentState:
    observation_text = "\n\n".join(
        f"Tool: {item['tool']}\n"
        f"Arguments: {item['arguments']}\n"
        f"Result:\n{item['result']}"
        for item in state["observations"]
    )

    prompt = f"""
You are assessing an ongoing network troubleshooting investigation.

Problem:
{state["problem"]}

Observed evidence:
{observation_text}

Current hypothesis:
{state["hypothesis"] or "None yet."}

Based only on the available evidence:

1. State the most likely current hypothesis.
2. Identify the strongest supporting evidence.
3. Identify what remains uncertain.
4. Do not claim that a test was performed unless it appears in the evidence.

Keep the assessment concise.
"""

    response = await generate_content(
        contents=prompt,
        config=types.GenerateContentConfig(),
    )

    return {
        **state,
        "hypothesis": response.text or "",
    }


async def finalize(state: AgentState) -> dict[str, Any]:
    report = build_report(
        problem=state["problem"],
        observations=state["observations"],
        hypothesis=state["hypothesis"],
        conclusion=(
            "The investigation reached the maximum number of diagnostic "
            "steps before a final diagnosis was produced."
        ),
    )

    return {
        "response": report,
    }


def route_after_plan(state: AgentState) -> str:
    if state["response"]:
        return "done"

    if state["steps"] > MAX_STEPS:
        return "finalize"

    return "execute"


graph_builder = StateGraph(AgentState)

graph_builder.add_node("plan", plan)
graph_builder.add_node("execute_tools", execute_tools)
graph_builder.add_node("assess", assess)
graph_builder.add_node("finalize", finalize)

graph_builder.add_edge(START, "plan")

graph_builder.add_conditional_edges(
    "plan",
    route_after_plan,
    {
        "execute": "execute_tools",
        "finalize": "finalize",
        "done": END,
    },
)

graph_builder.add_edge("execute_tools", "assess")
graph_builder.add_edge("assess", "plan")
graph_builder.add_edge("finalize", END)

graph = graph_builder.compile()


async def run_agent(problem: str) -> str:
    tool_definitions = await get_tool_definitions()

    initial_history = [
        {
            "role": "user",
            "parts": [
                {
                    "text": (
                        f"{SYSTEM_PROMPT}\n\n"
                        f"{build_user_prompt(problem)}"
                    )
                }
            ],
        }
    ]

    result = await graph.ainvoke(
        {
            "problem": problem,
            "history": initial_history,
            "tool_definitions": tool_definitions,
            "pending_calls": [],
            "observations": [],
            "hypothesis": "",
            "response": "",
            "steps": 0,
        }
    )

    return result["response"]
