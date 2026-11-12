from pydantic import ValidationError
from app.models import Article


def format_news(companies: list[dict],ticker: str) -> list[Article]:
    result: list[Article] = []
    all_headlines = set()
    for company in companies:
        headline = (company.get('headline','') or "").strip()
        if headline and headline not in all_headlines:
            try:
                news = Article(id=company.get('id'),
                               ticker=ticker,
                               headline=headline,
                               summary=(company.get("summary", "") or "").strip(),
                               publish_timestamp=company.get('datetime')
                               )
            except ValidationError:
                continue
            all_headlines.add(headline)
            result.append(news)
    return result
