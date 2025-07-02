from fastapi import FastAPI
from app.routes import router

app = FastAPI()

app.include_router(router)
@app.get("/")
async def root():
    return {"status": "Diaster Response API is live"}