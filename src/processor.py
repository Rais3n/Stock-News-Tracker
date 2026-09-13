from app.models import Article

def format_news(companies: list[dict],ticker: str) -> list[Article]:
    result: list[Article] = []
    all_headlines = set()
    for company in companies:
        headline = (company.get('headline','') or "").strip()
        if headline and headline not in all_headlines:
            all_headlines.add(headline)
            news = Article(id=company.get('id'),
                           ticker=ticker,
                           headline=headline,
                           summary=(company.get("summary", "") or "").strip()
                           )
            result.append(news)
    return result
