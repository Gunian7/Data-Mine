import pandas as pd
from pathlib import Path

path = Path('data/dictionaries/dlut_sentiment_lexicon_processed.csv')
if not path.exists():
    print('Processed DLUT lexicon not found:', path)
else:
    df = pd.read_csv(path)
    print('Total words:', len(df))
    print('Positive:', (df['polarity']=='positive').sum(), 'Negative:', (df['polarity']=='negative').sum(), 'Neutral:', (df['polarity']=='neutral').sum())
    print('\nTop positive sample:')
    print(df[df['polarity']=='positive'].sort_values('abs_score', ascending=False).head(10))
    print('\nTop negative sample:')
    print(df[df['polarity']=='negative'].sort_values('abs_score', ascending=False).head(10))
    print('\nSample neutral:')
    neutral_df = df[df['polarity']=='neutral']
    n = min(10, len(neutral_df)) if len(neutral_df) > 0 else 0
    if n > 0:
        print(neutral_df.sample(n))
    else:
        print('No neutral words to sample')

    # Save summary
    out = path.parent / 'lexicon_summary.txt'
    with open(out, 'w', encoding='utf-8') as f:
        f.write(f"Total words: {len(df)}\n")
        f.write(f"Positive: {(df['polarity']=='positive').sum()}\n")
        f.write(f"Negative: {(df['polarity']=='negative').sum()}\n")
        f.write(f"Neutral: {(df['polarity']=='neutral').sum()}\n")
    print('Saved summary to', out)
