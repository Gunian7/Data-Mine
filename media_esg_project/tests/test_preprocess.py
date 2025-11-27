from media_esg.preprocess import Preprocessor


def test_tokenize_simple():
    text = "公司发布环保声明，积极整改。"
    pre = Preprocessor(stopwords=set(['，', '。']))
    tokens = pre.tokenize(text)
    assert '公司' in tokens
    assert '环保' in tokens


def test_tokenize_pos():
    text = "公司发布环保声明，积极整改。"
    pre = Preprocessor()
    pos = pre.tokenize_pos(text)
    assert len(pos) > 0
