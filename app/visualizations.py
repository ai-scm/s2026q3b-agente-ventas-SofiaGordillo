import pandas as pd
import plotly.express as px


def create_chart(df: pd.DataFrame):
    """Crea un gráfico adecuado según las columnas de los resultados."""

    if df.empty or len(df.columns) < 2:
        return None

    # Identificar columnas numéricas, incluso si llegan como texto.
    data = df.copy()

    for column in data.columns:
        converted = pd.to_numeric(data[column], errors="coerce")

        if converted.notna().all():
            data[column] = converted

    numeric_columns = data.select_dtypes(
        include="number"
    ).columns.tolist()

    if not numeric_columns:
        return None

    # Elegir una columna categórica para el eje X.
    category_columns = [
        column
        for column in data.columns
        if column not in numeric_columns
    ]

    if not category_columns:
        return None

    category = category_columns[0]
    value = numeric_columns[0]

    fig = px.bar(
        data,
        x=category,
        y=value,
        title=f"{value.replace('_', ' ').capitalize()} por {category}",
        labels={
            category: category.replace("_", " ").capitalize(),
            value: value.replace("_", " ").capitalize(),
        },
        text=value,
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate="%{x}<br>%{y}<extra></extra>",
    )

    fig.update_layout(
        xaxis_title=category.replace("_", " ").capitalize(),
        yaxis_title=value.replace("_", " ").capitalize(),
        template="plotly_white",
    )

    return fig