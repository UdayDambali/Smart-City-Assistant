from app.services.pinecone_client import get_index, NAMESPACE
import json

with open("data/eco_tips.json", "r", encoding="utf-8") as f:
    tips = json.load(f)

records = [{"_id": str(i), "chunk_text": tip["tip"], "category": tip["category"]} for i, tip in enumerate(tips)]

index = get_index()
index.upsert_records(NAMESPACE, records)
print("Eco tips upserted successfully.")
