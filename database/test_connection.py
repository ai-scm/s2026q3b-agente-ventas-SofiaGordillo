from database.db import get_sales


def main():
    try:
        ventas = get_sales()

        print(f"\nConexión exitosa. Registros encontrados: {len(ventas)}")
        print("\nPrimeros registros:")

        for venta in ventas[:5]:
            print(venta)

    except Exception as error:
        print(f"Error al conectar con MySQL: {error}")


if __name__ == "__main__":
    main()