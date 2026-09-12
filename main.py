from src.orchestrator import clean_news_orchestrator

if __name__ == "__main__":
    test_news = clean_news_orchestrator("UBER", "2026-09-01", "2026-09-12")
    print(f"Results: {len(test_news)}")
    if test_news:
        print("First result:", test_news[0])