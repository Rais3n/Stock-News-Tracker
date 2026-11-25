from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
import logging

from src.config import load_api_key
from user_operations.auth import router
from rag.qdrant_store import QdrantStore
from src.summary import ticker_summary
from app.exceptions import ArticlesNotFoundError
from app.models import TickerSummary

load_dotenv()
FINNHUB_API_KEY = load_api_key("FINNHUB_API_KEY")
OPENROUTER_API_KEY = load_api_key("OPENROUTER_API_KEY")
AI_MODEL = "nvidia/nemotron-3.5-super-vl:free"
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(router)

qdrant = QdrantStore()


@app.get("/summary/{ticker}")
def get_summary(ticker: str) -> TickerSummary:
    ticker = ticker.upper().strip()
    try:
        result = ticker_summary(
            qdrant, ticker, FINNHUB_API_KEY, OPENROUTER_API_KEY, AI_MODEL
        )
    except ArticlesNotFoundError as e:
        raise HTTPException(
            status_code=404, detail=f"No recent news found for ticker {ticker}."
        ) from e
    except RuntimeError as e:
        logger.exception("Summary failed for ticker %s", ticker)
        raise HTTPException(
            status_code=502, detail="Upstream service error. Please try again later."
        ) from e
    return result
