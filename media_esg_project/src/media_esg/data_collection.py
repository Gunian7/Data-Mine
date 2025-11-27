"""
Data collection utilities: support loading from CSV/DB and scraping templates
"""
import csv
from typing import List
import pandas as pd


def load_news_csv(path: str) -> pd.DataFrame:
    """Load news data CSV with expected columns: news_id,title,content,publish_date,media,company(optional)"""
    df = pd.read_csv(path)
    return df


def load_company_list_csv(path: str) -> pd.DataFrame:
    """Load company list CSV with columns: company_name,ticker"""
    df = pd.read_csv(path)
    return df


# Template: implement site scrapers in `src/media_esg/scrapers/` if needed

def sample_web_scraper(url: str) -> List[dict]:
    """
    Placeholder for web scraping function. In practice use requests & BeautifulSoup or news API SDK.
    Return list of dicts with keys: news_id, title, content, publish_date, media
    """
    raise NotImplementedError("Implement site-specific scrapers or API clients")
