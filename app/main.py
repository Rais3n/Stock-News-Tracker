import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FINNHUB_API_KEY")

if not api_key:
    print("Error: FINNHUB_API_KEY is not found in file .env")
    exit(1)

def get_company_news(ticker: str,date_from: str,date_to: str):
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

def format_news(companies: list,ticker: str):
    result = []
    all_headlines = set()
    for company in companies:
        headline = company.get('headline','').strip()
        if headline and headline not in all_headlines:
            all_headlines.add(headline)
            result.append({'id': company.get('id', ''),
                        'ticker': ticker,
                        'headline': headline,
                        'summary':company.get('summary','')})
    return result

def clean_news_orchestrator(ticker: str,date_from: str,date_to: str):
    raw_data = get_company_news(ticker,date_from,date_to)
    clean_data = format_news(raw_data,ticker)
    return clean_data

if __name__ == "__main__":
    test_news = clean_news_orchestrator("UBER", "2026-09-01", "2026-09-12")
    print(f"Results: {len(test_news)}")
    if test_news:
        print("First result:", test_news[0])