from pydantic import BaseModel
from datetime import datetime


class Article(BaseModel):
    id: int
    ticker: str = ""
    summary: str = ""
    headline: str = ""
    publish_timestamp: int
    url: str
    source: str = ""

    @property
    def embedding_text(self) -> str:
        h = self.headline.strip()
        s = self.summary.strip()
        if s:
            return f"{h} - {s}"
        return h


class Source(BaseModel):
    headline: str
    url: str
    date: datetime


class TickerSummary(BaseModel):
    ticker: str
    summary: str
    sources: list[Source]
    generated_at: datetime
