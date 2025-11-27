import pandas as pd
import sys
from pathlib import Path

def convert_dlut(input_path, output_path):
    print(f"Reading from {input_path}...")
    try:
        # DLUT excel usually has headers. We need to inspect columns.
        # Common columns: '词语', '词性种类', '词义数', '词义序号', '情感分类', '强度', '极性'
        df = pd.read_excel(input_path)
        
        # Normalize column names if needed (strip whitespace)
        df.columns = df.columns.str.strip()
        
        required_cols = ['词语', '强度', '极性']
        if not all(col in df.columns for col in required_cols):
            print(f"Error: Missing required columns. Found: {df.columns.tolist()}")
            # Try to guess if names are slightly different
            return

        records = []
        for _, row in df.iterrows():
            word = row['词语']
            intensity = row['强度']
            polarity = row['极性']
            
            # Polarity: 0=Neutral, 1=Positive, 2=Negative
            # Intensity: 1 to 9 usually
            
            score = 0.0
            try:
                intensity = float(intensity)
                polarity = int(polarity)
            except ValueError:
                continue

            if polarity == 1:
                score = intensity
            elif polarity == 2:
                score = -intensity
            else:
                score = 0.0
            
            # Optional: Normalize score to -1 to 1 range? 
            # DLUT intensity is 1-9. Let's keep it raw or normalize. 
            # For this project, let's normalize by dividing by 9.0 to keep it roughly -1 to 1
            score = score / 9.0
            
            if score != 0:
                records.append({'word': word, 'score': score})
        
        out_df = pd.DataFrame(records)
        # Handle duplicates: average score or take max? 
        # Some words have multiple entries for different meanings.
        # Let's take the mean score for duplicates.
        out_df = out_df.groupby('word', as_index=False)['score'].mean()
        
        print(f"Converted {len(out_df)} unique words.")
        out_df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_dlut.py <input_excel> <output_csv>")
        # Default paths for convenience in this workspace
        base_dir = Path(__file__).resolve().parent.parent
        default_input = base_dir / "data/dictionaries/大连理工大学情感词汇本体库.xlsx"
        default_output = base_dir / "data/dictionaries/dlut_sentiment_lexicon.csv"
        
        if default_input.exists():
            print(f"Using default paths:\nInput: {default_input}\nOutput: {default_output}")
            convert_dlut(default_input, default_output)
        else:
            sys.exit(1)
    else:
        convert_dlut(sys.argv[1], sys.argv[2])
