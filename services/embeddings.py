from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536

def generate_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Text for embedding cannot be empty")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    embedding = response.data[0].embedding

    # Safety check
    if len(embedding) != EMBEDDING_DIM:
        raise RuntimeError("Embedding dimension mismatch")
    return embedding


# embedding is also a kind of its own service therefore it should also be in its own file 
# This is a external service and now it can be tested independently 
