from fastapi import FastAPI
from app.routes import router
from app.websocket import router as websocket_router

app = FastAPI()

app.include_router(router)
app.include_router(websocket_router)
@app.get("/")
async def root():
    return {"status": "Diaster Response API is live"}