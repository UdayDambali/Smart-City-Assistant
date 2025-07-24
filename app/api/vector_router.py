from fastapi import APIRouter, Query
from app.services.pinecone_client import get_index, NAMESPACE

router = APIRouter()

@router.get("/semantic-eco-tips")
async def semantic_eco_tips(query: str = Query(...)):
    try:
        index = get_index()
        results = index.search(
            namespace=NAMESPACE,
            query={
                "top_k": 5,
                "inputs": {"text": query}
            },
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": 5,
                "rank_fields": ["chunk_text"]
            }
        )

        return {
            "results": [
                {
                    "tip": hit["fields"]["chunk_text"],
                    "category": hit["fields"]["category"],
                    "score": hit["_score"]
                }
                for hit in results["result"]["hits"]
            ]
        }
    except Exception as e:
        return {"error": str(e)}

