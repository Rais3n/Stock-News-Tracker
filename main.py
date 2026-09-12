import os 
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("FINNHUB_API_KEY")

if not api_key:
    print("Error: FINNHUB_API_KEY is not found in file .env")
    exit(1)
