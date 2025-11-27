import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DICT_DIR = DATA_DIR / "dictionaries"

DEFAULT_DICT_PATH = DICT_DIR / "dlut_sentiment_lexicon_processed.csv"
# default_media_weights removed to avoid referencing a deleted sample file; users should define their own weights file if needed
DEFAULT_MEDIA_WEIGHTS = None

# Tokenization and preprocessing settings
STOPWORDS_PATH = DICT_DIR / "cn_stopwords.txt"

# Defaults
DEFAULT_OUTPUT_DIR = BASE_DIR / "output"
