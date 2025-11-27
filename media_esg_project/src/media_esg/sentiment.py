"""
Sentiment lexicon-based analysis for Chinese text.
Support: negation handling, degree adverbs, simple weightings.
"""
from typing import Dict, List, Tuple

from .preprocess import Preprocessor


class LexiconSentimentAnalyzer:
    def __init__(self, lexicon: Dict[str, float], negations: set = None, degree_dict: Dict[str, float] = None):
        self.lexicon = lexicon  # token -> score (positive/negative floats)
        self.negations = negations or set(["不", "没", "无", "非", "未", "没有"])
        self.degree_dict = degree_dict or {"非常": 1.5, "很": 1.3, "较": 1.2, "稍": 0.8, "略": 0.9}
        self.preprocessor = Preprocessor()

    def score_text(self, text: str) -> Dict[str, float]:
        """Return a dict with detailed scores.
        Basic heuristic:
        - sum sentiment scores of lexicon matches
        - flip sign if negation appears within a window of 3 tokens
        - multiply by degree adverbs if present
        """
        tokens = self.preprocessor.tokenize(text)
        total = 0.0
        pos_count = neg_count = 0
        window = 3
        n = len(tokens)
        for i, token in enumerate(tokens):
            if token in self.lexicon:
                base = self.lexicon[token]
                # Check if preceding tokens contain negation
                left = max(0, i-window)
                neg_found = any(tok in self.negations for tok in tokens[left:i])
                if neg_found:
                    base = -base
                # degree adverb check immediately preceding token
                if i >= 1 and tokens[i-1] in self.degree_dict:
                    base *= self.degree_dict[tokens[i-1]]
                total += base
                if base > 0:
                    pos_count += 1
                elif base < 0:
                    neg_count += 1
        return {
            "score": total,
            "pos_count": pos_count,
            "neg_count": neg_count,
            "token_count": n,
        }

    def classify(self, score: float, threshold: float = 0.1) -> str:
        if score > threshold:
            return "positive"
        elif score < -threshold:
            return "negative"
        else:
            return "neutral"


# Example loader for lexicon CSV file
import csv


def load_lexicon_csv(path: str) -> Dict[str, float]:
    lex = {}
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # robustly handle BOM or alternate header names
        fieldnames = [fn.strip() for fn in (reader.fieldnames or [])]
        word_field = None
        score_field = None
        for fn in fieldnames:
            l = fn.lower()
            if 'word' in l or 'token' in l or '词' in l:
                word_field = fn
            if 'score' in l or 'sentiment' in l or '情感' in l:
                score_field = fn
        # fallbacks
        word_field = word_field or 'word'
        score_field = score_field or 'score'
        for r in reader:
            word = r.get(word_field) or r.get('token') or r.get('词语')
            score = float(r.get(score_field) or r.get('sentiment') or r.get('情感') or 0.0)
            lex[word] = score
    return lex
