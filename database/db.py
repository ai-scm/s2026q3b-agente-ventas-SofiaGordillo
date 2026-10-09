import os

import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """Establece una conexión con la base de datos de ventas."""
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", "3307")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        cursorclass=pymysql.cursors.DictCursor,
        charset="utf8mb4",
    )


def get_sales():
    """Obtiene los registros de la tabla ventas."""
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ventas ORDER BY id")
            return cursor.fetchall()
    finally:
        connection.close()