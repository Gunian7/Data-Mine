"""
Main pipeline orchestration for the project.
"""
import yaml
import pandas as pd
from pathlib import Path

from .data_collection import load_news_csv, load_company_list_csv
from .preprocess import Preprocessor
from .sentiment import load_lexicon_csv, LexiconSentimentAnalyzer
from .supervision import compute_media_supervision
from .aggregation import aggregate_news_by_company_year, match_with_esg
from .validation import describe_variables
from .config import DEFAULT_DICT_PATH, DEFAULT_MEDIA_WEIGHTS


def run_pipeline(config_path: str):
    config = yaml.safe_load(open(config_path, 'r', encoding='utf-8'))
    # load settings
    news_path = config.get('news_csv')
    company_list = config.get('company_csv')
    esg_csv = config.get('esg_csv')
    dict_path = config.get('dict_path') or str(DEFAULT_DICT_PATH)
    media_weights_path = config.get('media_weights') or DEFAULT_MEDIA_WEIGHTS

    # load data
    news_df = load_news_csv(news_path)
    company_df = load_company_list_csv(company_list)
    if esg_csv:
        esg_df = pd.read_csv(esg_csv)
    else:
        esg_df = pd.DataFrame()

    # preprocess
    from .preprocess import Preprocessor
    pre = Preprocessor()
    news_df['content_clean'] = news_df['content'].fillna('').astype(str)

    # load lexicon
    lex = load_lexicon_csv(dict_path)
    analyzer = LexiconSentimentAnalyzer(lex)

    # score
    def score_row(row):
        r = analyzer.score_text(row['content_clean'])
        label = analyzer.classify(r['score'])
        return pd.Series({'sentiment_score': r['score'], 'pos_count': r['pos_count'], 'neg_count': r['neg_count'], 'sentiment_label': label})

    scored = news_df.apply(score_row, axis=1)
    news_df = pd.concat([news_df, scored], axis=1)

    # compute media supervision
    import yaml
    media_weights = None
    if media_weights_path:
        try:
            media_weights = yaml.safe_load(open(media_weights_path, 'r', encoding='utf-8'))
        except Exception:
            media_weights = None

    supervision_df = compute_media_supervision(news_df, media_weights=media_weights)

    # aggregate
    summary = aggregate_news_by_company_year(news_df)

    # match with esg
    # build company name -> ticker map if possible
    company_map = None
    if 'company_name' in company_df.columns and 'ticker' in company_df.columns:
        company_map = dict(zip(company_df['company_name'], company_df['ticker']))

    merged = match_with_esg(summary, esg_df, company_map=company_map)

    # describe
    desc = describe_variables(merged)

    # save outputs
    out_dir = Path(config.get('output_dir', './output'))
    out_dir.mkdir(parents=True, exist_ok=True)
    news_df.to_csv(out_dir / 'scored_news.csv', index=False, encoding='utf-8-sig')
    summary.to_csv(out_dir / 'news_summary_company_year.csv', index=False, encoding='utf-8-sig')
    merged.to_csv(out_dir / 'merged_with_esg.csv', index=False, encoding='utf-8-sig')
    desc.to_csv(out_dir / 'descriptive_stats.csv', encoding='utf-8-sig')

    return {
        'news': news_df,
        'summary': summary,
        'merged': merged,
        'desc': desc,
    }


if __name__ == '__main__':
    import sys
    run_pipeline(sys.argv[1])
