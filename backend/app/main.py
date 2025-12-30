from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="LLM Real-Time DB Query Engine")
app.include_router(router)
