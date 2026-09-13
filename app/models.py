from pydantic import BaseModel

class Article(BaseModel):
    id: int
    ticker: str = ""
    summary: str = ""
    headline: str = ""
    @property
    def embedding_text(self) -> str:
        h = self.headline.strip()
        s = self.summary.strip()
        if s:
            return f"{h} - {s}"
        return h