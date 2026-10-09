import os

import boto3
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "sofia")
MODEL_ID = os.getenv("MODEL_ID", "openai.gpt-oss-120b-1:0")


def get_bedrock_client():
    """Crea un cliente de Amazon Bedrock Runtime."""
    session = boto3.Session(
        profile_name=AWS_PROFILE,
        region_name=AWS_REGION,
    )

    return session.client("bedrock-runtime")


def ask_bedrock(question: str) -> str:
    """Envía una pregunta al modelo y devuelve su respuesta."""
    client = get_bedrock_client()

    response = client.converse(
        modelId=MODEL_ID,
        messages=[
            {
                "role": "user",
                "content": [{"text": question}],
            }
        ],
        inferenceConfig={
            "maxTokens": 1000,
            "temperature": 0.2,
        },
    )

    content = response["output"]["message"]["content"]

    # Algunos modelos pueden devolver bloques de razonamiento
    # además del texto visible de la respuesta.
    for block in content:
        if "text" in block:
            return block["text"]

    raise RuntimeError("El modelo no devolvió texto en su respuesta.")