from app.bedrock import ask_bedrock


if __name__ == "__main__":
    respuesta = ask_bedrock(
        "Explica en una sola frase qué es un agente inteligente de análisis de ventas."
    )

    print("\nRespuesta de Amazon Bedrock:")
    print(respuesta)