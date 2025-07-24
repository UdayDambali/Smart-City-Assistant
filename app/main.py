# from fastapi import FastAPI
# from app.api import chat_router, feedback_router, eco_tips_router, kpi_upload_router, anomaly_checker, vector_router

# app = FastAPI()

# app.include_router(chat_router.router, prefix="/chat")
# app.include_router(feedback_router.router, prefix="/feedback")
# app.include_router(eco_tips_router.router, prefix="/eco")
# app.include_router(kpi_upload_router.router, prefix="/kpi")
# app.include_router(anomaly_checker.router, prefix="/anomaly")
# app.include_router(vector_router.router, prefix="/vector")


from fastapi import FastAPI
from app.api import chat_router, feedback_router, eco_tips_router, vector_router

app = FastAPI()
app.include_router(chat_router.router)
app.include_router(feedback_router.router)
app.include_router(eco_tips_router.router)
app.include_router(vector_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
