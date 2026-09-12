import os 
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FINNHUB_API_KEY")

if not api_key:
    print("Error: FINNHUB_API_KEY is not found in file .env")
    exit(1)

def get_company_news(ticker,date_from,date_to):
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
        print(f"Error HTTP {data.status_code}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Destination Error: {e}")
    except ValueError:
        print("Error: Destination server response is not correct JSON format")
    return []