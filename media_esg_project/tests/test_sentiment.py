from media_esg.sentiment import load_lexicon_csv, LexiconSentimentAnalyzer


def test_load_lexicon(tmp_path):
    # Use existing dictionary
    path = 'data/dictionaries/dlut_sentiment_lexicon_processed.csv'
    lex = load_lexicon_csv(path)
    assert '污染' in lex


def test_analyzer_simple():
    lex = {'污染': -1.2, '环保': 0.6, '优秀': 1.0}
    analyzer = LexiconSentimentAnalyzer(lex)
    text = '公司环保表现优秀'
    res = analyzer.score_text(text)
    assert res['score'] > 0

    text2 = '公司因污染被罚'
    res2 = analyzer.score_text(text2)
    assert res2['score'] < 0
