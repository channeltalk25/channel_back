from fastapi import FastAPI
from core.http import init_http_session, close_http_session
from app.api import cluster_router, chat_router, recommend_router
import time
import uvicorn
from prompts import loader

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    loader.load_prompts()
    print(loader.RECOMMENDER_PROMPT)
    await init_http_session()

@app.on_event("shutdown")
async def shutdown_event():
    await close_http_session()

app.include_router(chat_router)
app.include_router(cluster_router)
app.include_router(recommend_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3100)
    print(time.time())