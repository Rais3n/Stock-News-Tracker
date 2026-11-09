import os 
import requests
from dotenv import load_dotenv


def load_finnhub_key() -> str:
    load_dotenv()
    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise RuntimeError("FINNHUB_API_KEY is missing or empty in .env")
    return api_key

def get_company_news(ticker: str,date_from: str,date_to: str, api_key: str):
    params = {"symbol": ticker,
              "from": date_from,
              "to": date_to,
              "token": api_key}
    try:
        data = requests.get('https://finnhub.io/api/v1/company-news',timeout=5.0,params=params)
        data.raise_for_status()
        return data.json()
    except requests.exceptions.Timeout:
        print(f"Error: Server has not responded within 5 seconds for {ticker}.")
    except requests.exceptions.HTTPError as e:
        print(f"Error HTTP {e.response.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Destination Error: {e}")
    except ValueError:
        print("Error: Destination server response is not correct JSON format")
    return []