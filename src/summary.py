import time
from datetime import datetime, timezone, timedelta


from src.ingestion import ingest
from rag.qdrant_store import QdrantStore
from app.models import TickerSummary, Source
from app.exceptions import ArticlesNotFoundError
from src.llm_client import ask_llm

CACHE: dict[str, float] = {}
CACHE_TTL_SECONDS = 3600
SUMMARY_SYSTEM_PROMPT = (
    "You are a financial news analyst. "
    "You will receive a list of news articles about one stock ticker. "
    "Write a short summary (4-6 sentences) of what happened with this company "
    "based ONLY on the provided articles. "
    "Mention the most important events and the overall sentiment "
    "(positive, negative or mixed). "
    "If articles contradict each other, say so. "
    "Do not invent facts, numbers or dates that are not in the articles. "
    "Do not give investment advice. "
    "Answer in plain text, without markdown, headings or lists."
)


def ticker_summary(
    qdrant: QdrantStore, ticker: str, finnhub_key: str, openrouter_key: str, model: str
) -> TickerSummary:
    timestamp = time.time()
    now = datetime.now(timezone.utc)
    if timestamp - CACHE.get(ticker, 0) > CACHE_TTL_SECONDS:
        week_ago = (now - timedelta(days=7)).strftime("%Y-%m-%d")
        ingest(
            qdrant,
            ticker,
            date_from=week_ago,
            date_to=now.strftime("%Y-%m-%d"),
            api_key=finnhub_key,
        )
        CACHE[ticker] = timestamp
    records = qdrant.get_by_ticker(ticker, limit=15)
    if not records:
        raise ArticlesNotFoundError(
            f"No news articles found for ticker '{ticker}' in the last 7 days"
        )
    sources = []
    text = []
    for record in records:
        date = record.payload["publish_timestamp"]
        sources.append(
            Source(
                headline=record.payload["headline"],
                url=record.payload["url"],
                date=date,
            )
        )
        text.append(
            f"[{datetime.fromtimestamp(date, tz=timezone.utc).strftime('%Y-%m-%d')}] "
            + record.payload["text"]
        )
    content = "\n".join(text)
    messages = [
        {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
        {"role": "user", "content": f"Ticker: {ticker}\n\n{content}"},
    ]
    summary = ask_llm(messages, model, openrouter_key)
    result = TickerSummary(
        ticker=ticker,
        summary=summary,
        sources=sources,
        generated_at=now,
    )
    return result
