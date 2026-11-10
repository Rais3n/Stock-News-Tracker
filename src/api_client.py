import os 
import requests
from dotenv import load_dotenv


def load_finnhub_key() -> str:
    load_dotenv()
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise RuntimeError("FINNHUB_API_KEY is missing or empty in .env")
    return api_key

def get_company_news(ticker: str,date_from: str,date_to: str, api_key: str) -> list[dict]:
    params = {"symbol": ticker,
              "from": date_from,
              "to": date_to,
              }
    try:
        data = requests.get('https://finnhub.io/api/v1/company-news',timeout=5.0,params=params,headers={"X-Finnhub-Token": api_key})
        data.raise_for_status()
        return data.json()
    except requests.exceptions.Timeout as e:
        raise RuntimeError(f"Finnhub did not respond within 5 seconds (ticker: {ticker})") from e
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Finnhub returned HTTP {e.response.status_code} for ticker {ticker}") from e
    except requests.exceptions.JSONDecodeError as e:
        raise RuntimeError(f"Finnhub returned invalid JSON for ticker {ticker}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Could not connect to Finnhub ({type(e).__name__}) for ticker {ticker}") from e
