import sqlglot
from sqlglot import exp

from app.bedrock import ask_bedrock
from app.prompts import SYSTEM_PROMPT


def validate_sql(sql: str) -> str:
    """Valida que una consulta SQL sea de solo lectura."""

    sql = sql.strip()

    # Rechazar respuestas vacías.
    if not sql:
        raise ValueError("La consulta SQL está vacía.")

    # Analizar la consulta con el dialecto MySQL.
    try:
        statements = sqlglot.parse(sql, read="mysql")
    except sqlglot.errors.ParseError as error:
        raise ValueError("La consulta SQL no tiene una sintaxis válida.") from error

    # Debe existir exactamente una instrucción SQL.
    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Solo se permite una consulta SQL por solicitud.")

    statement = statements[0]

    # Permitir únicamente consultas SELECT.
    if not isinstance(statement, exp.Query):
        raise ValueError("Solo se permiten consultas de lectura SELECT.")

    # Permitir únicamente la tabla ventas.
    tables = statement.find_all(exp.Table)

    if not tables:
        raise ValueError("La consulta debe utilizar la tabla ventas.")

    for table in tables:
        if table.name.lower() != "ventas" or table.db or table.catalog:
            raise ValueError("Solo se permite consultar la tabla ventas.")

    # Evitar consultas excesivamente grandes.
    limit = statement.args.get("limit")

    if limit is None:
        statement = statement.limit(100)
    else:
        limit_value = limit.expression

        if not isinstance(limit_value, exp.Literal) or limit_value.is_string:
            raise ValueError("El límite debe ser un número entero.")

        try:
            row_limit = int(limit_value.this)
        except (ValueError, TypeError) as error:
            raise ValueError("El límite debe ser un número entero.") from error

        if row_limit < 1 or row_limit > 100:
            raise ValueError("El límite debe estar entre 1 y 100.")

    return statement.sql(dialect="mysql")


def generate_sql(question: str) -> str:
    """Genera una consulta SQL a partir de una pregunta en lenguaje natural."""

    prompt = f"""
{SYSTEM_PROMPT}

Convierte la pregunta del usuario en una consulta SQL.

Reglas:
- Devuelve únicamente una consulta SQL.
- No incluyas explicaciones ni bloques Markdown.
- Utiliza exclusivamente la tabla ventas y sus columnas.
- Genera solamente consultas SELECT.
- Incluye LIMIT 100 como máximo, o un límite menor si corresponde.
- Si la pregunta no puede responderse con los datos disponibles,
  devuelve exactamente: NO_SE_PUEDE_RESPONDER.

Pregunta del usuario:
{question}
"""

    sql = ask_bedrock(prompt)

    if sql.strip() == "NO_SE_PUEDE_RESPONDER":
        return sql.strip()

    return validate_sql(sql)