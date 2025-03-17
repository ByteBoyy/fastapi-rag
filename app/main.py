import utils.transport
import utils.session
from fastapi import FastAPI
from app.routes import user_routes, rag_routes, general_routes

app = FastAPI(title="FastAPI AI-RAG Service")

app.include_router(general_routes.router)
app.include_router(user_routes.router)
app.include_router(rag_routes.router)
