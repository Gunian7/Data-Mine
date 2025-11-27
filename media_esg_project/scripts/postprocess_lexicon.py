import pandas as pd
import re
import argparse
from pathlib import Path


def is_chinese_word(word: str) -> bool:
    # Return True if the word contains any CJK Unified Ideographs
    return bool(re.search('[\u4e00-\u9fff]', str(word)))


def postprocess(input_csv: str, output_prefix: str = None, only_chinese: bool = True, threshold: float = 0.0):
    df = pd.read_csv(input_csv)
    if 'word' not in df.columns or 'score' not in df.columns:
        raise ValueError("Input CSV must contain 'word' and 'score' columns")

    if only_chinese:
        df = df[df['word'].apply(is_chinese_word)].copy()

    df['polarity'] = df['score'].apply(lambda x: 'positive' if x > threshold else ('negative' if x < -threshold else 'neutral'))
    df['abs_score'] = df['score'].abs()

    outdir = Path(input_csv).resolve().parent
    if output_prefix is None:
        output_prefix = outdir / 'dlut_sentiment_lexicon_processed'
    else:
        output_prefix = Path(output_prefix)

    df.to_csv(str(output_prefix) + '.csv', index=False, encoding='utf-8-sig')
    df[df['polarity'] == 'positive'].to_csv(str(output_prefix) + '_positive.csv', index=False, encoding='utf-8-sig')
    df[df['polarity'] == 'negative'].to_csv(str(output_prefix) + '_negative.csv', index=False, encoding='utf-8-sig')
    df[df['polarity'] == 'neutral'].to_csv(str(output_prefix) + '_neutral.csv', index=False, encoding='utf-8-sig')

    # Save JSON mapping: word -> score
    mapping = dict(zip(df['word'], df['score']))
    import json
    with open(str(output_prefix) + '.json', 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"Processed: {len(df)} rows. Saved to {output_prefix}.csv and subsets.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=False, help='Input CSV', default='data/dictionaries/dlut_sentiment_lexicon.csv')
    parser.add_argument('--out', '-o', required=False, help='Output prefix', default=None)
    parser.add_argument('--only_chinese', action='store_true', help='Keep only entries containing Chinese characters')
    parser.add_argument('--threshold', type=float, default=0.0, help='Threshold for neutral label (default 0.0)')
    args = parser.parse_args()

    postprocess(args.input, args.out, only_chinese=args.only_chinese, threshold=args.threshold)
