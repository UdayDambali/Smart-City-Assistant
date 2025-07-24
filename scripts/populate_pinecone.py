import os
import sys
import json

# Add root path so we can import from app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.pinecone_client import get_index, NAMESPACE

# Load your eco tips JSON file
with open("data/eco_tips.json", "r", encoding="utf-8") as f:
    tips_data = json.load(f)

index = get_index()

# Prepare documents for Pinecone
docs = []
for i, tip in enumerate(tips_data):
    docs.append({
        "id": str(i),
        "values": {
            "chunk_text": tip["tip"],
            "category": tip.get("category", "General")
        }
    })

# Upload to Pinecone (upsert = insert or update)
index.upsert(
    vectors=docs,
    namespace=NAMESPACE
)

print(f"✅ Uploaded {len(docs)} eco tips to Pinecone.")
