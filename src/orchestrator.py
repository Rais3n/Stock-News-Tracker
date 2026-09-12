from src.api_client import get_company_news
from src.processor import format_news

def clean_news_orchestrator(ticker: str,date_from: str,date_to: str):
    raw_data = get_company_news(ticker,date_from,date_to)
    clean_data = format_news(raw_data,ticker)
    return clean_data