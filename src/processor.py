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
