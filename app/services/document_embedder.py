from sentence_transformers import SentenceTransformer

class DocumentEmbedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        return self.model.encode(texts)
from pydantic import BaseSettings

class Settings(BaseSettings):
    WATSONX_API_KEY: str
    PROJECT_ID: str
    MODEL_ID: str
    PINECONE_API_KEY: str
    PINECONE_ENV: str

    class Config:
        env_file = ".env"

settings = Settings()