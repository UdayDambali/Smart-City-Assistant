from fastapi import APIRouter
import json
from pathlib import Path
import logging

router = APIRouter()

@router.get("/get-eco-tips")
async def get_eco_tips():
    print("✅ Eco tips endpoint called")
    try:
        tips_path = Path("data/eco_tips.json")
        print(f"Looking for tips at: {tips_path.resolve()}")
        with open(tips_path, "r", encoding="utf-8") as f:
            tips = json.load(f)
        print(f"✅ Loaded {len(tips)} tips")
        return {"tips": tips}
    except Exception as e:
        logging.error(f"❌ Error loading eco tips: {e}")
        return {"error": str(e)}

