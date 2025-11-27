"""
Aggregation & matching with ESG data: merge company-year-level features with ESG panel data
"""
from typing import Dict
import pandas as pd


def aggregate_news_by_company_year(news_df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate news-level sentiment into company-year-level summary.
    Input must have: publish_date, company, sentiment_score, sentiment_label
    Output: company, year, mean_sentiment, total_count, negative_ratio, weighted_sentiment
    """
    news_df['publish_date'] = pd.to_datetime(news_df['publish_date'])
    news_df['year'] = news_df['publish_date'].dt.year

    # Example aggregate features
    gb = news_df.groupby(['company', 'year'])
    summary = gb.agg(
        mean_sentiment=('sentiment_score', 'mean'),
        total_count=('news_id', 'count'),
        negative_count=('sentiment_label', lambda s: (s=='negative').sum()),
        weighted_sentiment=('sentiment_score', 'sum')
    ).reset_index()
    summary['negative_ratio'] = summary['negative_count'] / summary['total_count'].replace(0, 1)
    return summary


def match_with_esg(summary_df: pd.DataFrame, esg_df: pd.DataFrame, company_map: Dict[str,str] = None) -> pd.DataFrame:
    """
    Match company-year aggregated news features with ESG panel data by company ticker/name
    company_map: optional mapping from news company name -> esg ticker
    """
    # Apply company_map if available
    if company_map:
        summary_df['ticker'] = summary_df['company'].map(company_map)
    else:
        summary_df['ticker'] = summary_df['company']

    merged = pd.merge(summary_df, esg_df, left_on=['ticker', 'year'], right_on=['ticker', 'year'], how='left')
    return merged
