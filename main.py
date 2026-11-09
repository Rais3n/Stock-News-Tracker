from fastapi import FastAPI

from src.api_client import load_finnhub_key
from user_operations.auth import router

FINNHUB_API_KEY = load_finnhub_key()

app = FastAPI()
app.include_router(router)
