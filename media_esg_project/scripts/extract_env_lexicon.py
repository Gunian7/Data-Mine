import pandas as pd
from pathlib import Path
import jieba
from rapidfuzz import fuzz

# Expanded set of environment-related keywords and synonyms
ENV_KEYWORDS = [
    '污染', '排污', '排放', '废水', '废气', '废弃物', '固废', '污染物', '污染源', '整改', '罚款', '环保', '环境', '绿色',
    '排放超标', '超标', '清洁生产', '排污口', '污水', '危险废物', '废渣', '废液', '废气排放', '大气污染', '水污染', '噪声'
]


def extract_env_lexicon(input_csv: str, output_csv: str = None, keywords: list = None, fuzzy: bool = False, fuzzy_threshold: int = 80, use_segmentation: bool = True):
    keywords = keywords or ENV_KEYWORDS
    df = pd.read_csv(input_csv)

    # Keep words that match any keyword via substring, segmentation, or fuzzy matching (if enabled)
    def contains_keyword(w):
        w = str(w)
        # direct substring
        for k in keywords:
            if k in w:
                return True
        # segmentation: check tokens
        if use_segmentation:
            tokens = list(jieba.cut(w))
            for t in tokens:
                for k in keywords:
                    if t == k or k in t:
                        return True
        # fuzzy match
        if fuzzy:
            for k in keywords:
                if fuzz.partial_ratio(w, k) >= fuzzy_threshold:
                    return True
        return False

    df_candidate = df[df['word'].apply(contains_keyword)].copy()
    outdir = Path(input_csv).resolve().parent
    if output_csv is None:
        output_csv = outdir / 'dlut_env_candidates.csv'
    else:
        output_csv = Path(output_csv)

    df_candidate.to_csv(output_csv, index=False, encoding='utf-8-sig')
    print(f'Saved {len(df_candidate)} environment-related candidates to {output_csv}')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=False, default='data/dictionaries/dlut_sentiment_lexicon_processed.csv')
    parser.add_argument('--output', '-o', required=False, default=None)
    parser.add_argument('--keywords', '-k', nargs='*', help='Override env keywords', default=None)
    parser.add_argument('--fuzzy', action='store_true', help='Enable fuzzy matching (rapidfuzz)')
    parser.add_argument('--fuzzy_threshold', type=int, default=80, help='Fuzzy matching threshold (0-100)')
    parser.add_argument('--no_seg', dest='use_segmentation', action='store_false', help='Disable segmentation matching')
    args = parser.parse_args()

    extract_env_lexicon(args.input, args.output, args.keywords, fuzzy=args.fuzzy, fuzzy_threshold=args.fuzzy_threshold, use_segmentation=args.use_segmentation)
