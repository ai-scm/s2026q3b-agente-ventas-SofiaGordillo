import asyncio
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from app.agent import generate_sql
from app.mcp_client import consultar_ventas_mcp


class SalesAgentState(TypedDict):
    """Estado compartido durante la ejecución del agente."""

    question: str
    sql: str
    results: list[dict[str, Any]]
    response: str
    error: str


def generate_query(state: SalesAgentState) -> dict:
    """Genera una consulta SQL a partir de la pregunta."""

    sql = generate_sql(state["question"])

    if sql == "NO_SE_PUEDE_RESPONDER":
        return {
            "sql": "",
            "results": [],
            "response": (
                "No puedo responder esa pregunta con los datos "
                "disponibles en la tabla de ventas."
            ),
            "error": "",
        }

    return {
        "sql": sql,
        "results": [],
        "response": "",
        "error": "",
    }


def execute_query(state: SalesAgentState) -> dict:
    """Ejecuta la consulta SQL mediante el servidor MCP."""

    try:
        resultado = asyncio.run(
            consultar_ventas_mcp(state["sql"])
        )

        if not resultado.get("success"):
            return {
                "results": [],
                "response": "No fue posible consultar las ventas.",
                "error": resultado.get(
                    "error",
                    "Error al ejecutar la consulta.",
                ),
            }

        filas = resultado.get("rows", [])

        return {
            "results": filas,
            "response": (
                f"La consulta se ejecutó correctamente. "
                f"Se encontraron {len(filas)} resultados."
            ),
            "error": "",
        }

    except Exception:
        return {
            "results": [],
            "response": "Ocurrió un error al consultar las ventas.",
            "error": "No fue posible completar la consulta.",
        }


def build_graph():
    """Construye el flujo de trabajo del agente de ventas."""

    workflow = StateGraph(SalesAgentState)

    workflow.add_node("generate_query", generate_query)
    workflow.add_node("execute_query", execute_query)

    workflow.add_edge(START, "generate_query")

    workflow.add_conditional_edges(
        "generate_query",
        lambda state: (
            "finish" if not state["sql"] else "execute"
        ),
        {
            "finish": END,
            "execute": "execute_query",
        },
    )

    workflow.add_edge("execute_query", END)

    return workflow.compile()


sales_graph = build_graph()


def ask_sales_agent(question: str) -> dict:
    """Procesa una pregunta en lenguaje natural."""

    initial_state: SalesAgentState = {
        "question": question,
        "sql": "",
        "results": [],
        "response": "",
        "error": "",
    }

    return sales_graph.invoke(initial_state)