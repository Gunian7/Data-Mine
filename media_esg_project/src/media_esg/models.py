from dataclasses import dataclass
from typing import Optional
import pandas as pd

@dataclass
class NewsRecord:
    news_id: str
    title: str
    content: str
    publish_date: str
    media: str
    company: Optional[str] = None  # company name or code
    raw: Optional[dict] = None

    def to_dict(self) -> dict:
        return {
            "news_id": self.news_id,
            "title": self.title,
            "content": self.content,
            "publish_date": self.publish_date,
            "media": self.media,
            "company": self.company,
        }

@dataclass
class CompanyRecord:
    company_name: str
    ticker: str
    industry: Optional[str] = None
    raw: Optional[dict] = None

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame([{
            "company_name": self.company_name,
            "ticker": self.ticker,
            "industry": self.industry,
        }])
