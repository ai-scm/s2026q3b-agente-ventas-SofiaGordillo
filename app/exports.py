from io import BytesIO

import pandas as pd


def export_csv(df: pd.DataFrame) -> bytes:
    """Convierte un DataFrame en un archivo CSV descargable."""

    return df.to_csv(
        index=False,
        encoding="utf-8-sig",
    ).encode("utf-8-sig")


def export_excel(df: pd.DataFrame) -> bytes:
    """Convierte un DataFrame en un archivo Excel descargable."""

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Ventas",
        )

    return output.getvalue()