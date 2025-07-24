from fastapi import APIRouter

router = APIRouter()

@router.get("/feedback/ping")
def feedback_ping():
    return {"message": "Feedback router is working!"}
