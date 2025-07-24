import os
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("PINECONE_API_KEY")
if not API_KEY:
    raise ValueError("PINECONE_API_KEY is not set in the environment.")

pc = Pinecone(api_key=API_KEY)

INDEX_NAME = "eco-tips-index"
NAMESPACE = "eco-tips-namespace"


def get_index():
    if not pc.has_index(INDEX_NAME):
        print("Creating Pinecone index...")
        pc.create_index_for_model(
            name=INDEX_NAME,
            cloud="aws",
            region="us-east-1",
            embed={"model": "llama-text-embed-v2", "field_map": {"text": "chunk_text"}}
        )
    else:
        print("Pinecone index already exists.")

    print(f"Index: {INDEX_NAME}, Namespace: {NAMESPACE}")
    return pc.Index(INDEX_NAME)

