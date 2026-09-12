# SNT - Stock News Tracker

System monitorowania wiadomości giełdowych, analizy sentymentu rynkowego oraz agregacji raportów dla spółek giełdowych.

## Funkcjonalności
- Pobieranie danych: Finnhub API
- Normalizacja i deduplikacja: format JSON
- Magazyn danych: baza danych
- Analiza LLM: podsumowania i sentyment

## Konfiguracja
1. Klonowanie: git clone https://github.com/Rais3n/Stock-News-Tracker.git
2. Środowisko: python -m venv .venv
3. Aktywacja: .\.venv\Scripts\activate
4. Zależności: pip install -r requirements.txt
5. Zmienne: Skopiuj .env.example do .env i uzupełnij FINNHUB_API_KEY

## Uruchomienie
python main.py