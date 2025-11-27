"""
Preprocessing: tokenization, stopwords removal, POS tagging, synonym merging
"""
from typing import List, Tuple
import jieba
import jieba.posseg as pseg


class Preprocessor:
    def __init__(self, stopwords: set = None, synonyms: dict = None):
        self.stopwords = stopwords or set()
        self.synonyms = synonyms or {}

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text using jieba"""
        tokens = [tok for tok in jieba.cut(text) if tok.strip() and tok not in self.stopwords]
        return tokens

    def tokenize_pos(self, text: str) -> List[Tuple[str, str]]:
        return [(w.word, w.flag) for w in pseg.cut(text) if w.word.strip()]

    def normalize_synonyms(self, tokens: List[str]):
        return [self.synonyms.get(t, t) for t in tokens]

    def preprocess(self, text: str, do_pos: bool = False):
        if do_pos:
            return self.tokenize_pos(text)
        return self.tokenize(text)
