from fastapi import FastAPI
from core.http import init_http_session, close_http_session
from app.api import channel_router, cluster_router, group_router, manager_router, user_chat_router, message_router, threads_router
import time
import uvicorn

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await init_http_session()

@app.on_event("shutdown")
async def shutdown_event():
    await close_http_session()

app.include_router(channel_router)
app.include_router(group_router)
app.include_router(manager_router)
app.include_router(user_chat_router)
app.include_router(message_router)
app.include_router(threads_router)
app.include_router(cluster_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3100)
    print(time.time())