from mcp.server.fastmcp import FastMCP

from app.agent import validate_sql
from database.db import get_connection


mcp = FastMCP("sales-database")


@mcp.tool()
def consultar_ventas(sql: str) -> dict:
    """
    Ejecuta una consulta SQL de solo lectura sobre la tabla ventas.

    Args:
        sql: Consulta SELECT que utiliza exclusivamente la tabla ventas.

    Returns:
        Diccionario con los resultados o un mensaje de error.
    """
    try:
        # Validar la consulta antes de acceder a MySQL.
        consulta_validada = validate_sql(sql)

        # Ejecutar la consulta validada.
        connection = get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(consulta_validada)
                resultados = cursor.fetchall()

            return {
                "success": True,
                "rows": resultados,
                "count": len(resultados),
            }

        finally:
            connection.close()

    except ValueError as error:
        return {
            "success": False,
            "error": str(error),
        }

    except Exception:
        # Evitar exponer detalles internos de la conexión.
        return {
            "success": False,
            "error": "No fue posible consultar la base de datos.",
        }


if __name__ == "__main__":
    mcp.run(transport="stdio")