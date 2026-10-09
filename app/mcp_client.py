import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parent.parent


async def consultar_ventas_mcp(sql: str) -> dict:
    """Consulta las ventas mediante el protocolo MCP."""

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "mcp_server.server",
        ],
        cwd=str(PROJECT_ROOT),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            resultado = await session.call_tool(
                "consultar_ventas",
                arguments={"sql": sql},
            )

            if resultado.isError:
                raise RuntimeError("El servidor MCP no pudo completar la consulta.")

            datos = []

            for contenido in resultado.content:
                if contenido.type == "text":
                    try:
                        datos.append(json.loads(contenido.text))
                    except json.JSONDecodeError:
                        datos.append({"text": contenido.text})

            if len(datos) == 1 and isinstance(datos[0], dict):
                return datos[0]

            return {"success": True, "results": datos}