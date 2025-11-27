"""
Media supervision metrics: compute counts, negative ratios, weighted media scores
"""
from typing import Dict, List
import pandas as pd


def compute_media_supervision(news_df: pd.DataFrame, media_weights: Dict[str, float] = None) -> pd.DataFrame:
    """
    news_df: should contain columns: publish_date, company, media, sentiment_score, sentiment_label
    Returns a dataframe indexed by company and year with supervision metrics
    Metrics: total_count, negative_count, negative_ratio, weighted_sentiment
    """
    # Ensure publish_date is datetime
    news_df['publish_date'] = pd.to_datetime(news_df['publish_date'])
    news_df['year'] = news_df['publish_date'].dt.year

    def weight_media(media_name: str) -> float:
        if media_weights and media_name in media_weights:
            return media_weights[media_name]
        return 1.0

    news_df['media_weight'] = news_df['media'].apply(weight_media)

    agg = news_df.groupby(['company', 'year']).apply(lambda x: pd.Series({
        'total_count': len(x),
        'negative_count': (x['sentiment_label'] == 'negative').sum(),
        'negative_ratio': (x['sentiment_label'] == 'negative').sum() / max(1, len(x)),
        'weighted_sentiment': (x['sentiment_score'] * x['media_weight']).sum() / max(1, x['media_weight'].sum()),
    }))

    return agg.reset_index()
