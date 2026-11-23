from dotenv import load_dotenv
from fastapi import FastAPI

from src.config import load_api_key
from user_operations.auth import router


load_dotenv()
FINNHUB_API_KEY = load_api_key('FINNHUB_API_KEY')

app = FastAPI()
app.include_router(router)
