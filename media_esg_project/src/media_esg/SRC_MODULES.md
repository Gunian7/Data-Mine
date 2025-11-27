# src 模块说明（SRC_MODULES.md）

以下文档描述 `src/media_esg` 内各 Python 文件的职责、关键函数、输入/输出与运行示例，便于理解项目实现与扩展。

---

## 主要模块
1. config.py：项目常量定义、默认设置(包括数据目录、字典路径等)
2. 文本预处理（preprocess.py）
3. 字典法情感分析（sentiment.py）（还需要加上领域字典）
4. 媒体监督指标（supervision.py）（未测试）
5. 数据聚合（aggregation.py）（未测试）
6. 验证与稳健性检验（validation.py）（尚未完成）

## config.py

职责：定义项目常量路径与默认设置（数据目录、字典位置、停用词路径、默认输出目录）。

关键常量：
- `BASE_DIR`：项目根目录
- `DATA_DIR`：数据目录（`/data`）
- `DICT_DIR`：字典目录（`/data/dictionaries`）
- `DEFAULT_DICT_PATH`：默认情感词典（现指向 `dlut_sentiment_lexicon_processed.csv`）
- `STOPWORDS_PATH`：停用词路径
- `DEFAULT_OUTPUT_DIR`：默认输出文件夹

用途：在 pipeline 和工具中引用来加载字典和写出结果，便于统一配置。

---

## models.py

职责：定义数据结构类（数据类），对入库/传输的数据做最小包装。

关键类：
- `NewsRecord`（news_id, title, content, publish_date, media, company）
- `CompanyRecord`（company_name, ticker, industry）

输入/输出：
- 将单条记录封装为 dataclass，对上层函数友好（如 `to_dict()`/`to_frame()` 聚合）。

常见用途：
- 从爬虫或 CSV 加载新闻数据后，转为 `NewsRecord` 对象用于进一步处理或导出。 

---

## utils.py

职责：提供工具函数（文本清理、分块批处理等）。

关键函数：
- `clean_text(text)`：基本清理（去多余空白、修整等）。
- `chunk_iterable(seq, size)`：将长列表分块处理，便于批量调用或并行化。

输入/输出：字符串、可迭代对象

用途：常被 preprocess、scoring 和爬虫脚本调度调用。

---

## data_collection.py

职责：提供新闻/公司数据的加载函数和爬虫/API 客户端模板（占位）。

关键函数：
- `load_news_csv(path: str) -> pd.DataFrame`：读取 CSV（期望列： news_id, title, content, publish_date, media, company ）
- `load_company_list_csv(path: str) -> pd.DataFrame`：读取公司清单（company_name,ticker,industry）
- `sample_web_scraper(url: str) -> List[dict]`：爬虫模板（site-specific implement）

输入/输出：CSV -> pandas.DataFrame

注意：
- 在生产环境中建议把更复杂爬虫逻辑分离到 `src/media_esg/scrapers/`。

---

## preprocess.py

职责：文本预处理（中文分词、POS、停用词过滤、同义词归并等）。

关键类 / 方法：
- `Preprocessor`：带 stopwords 与 synonyms 字典，支持：
  - `tokenize(text)`：jieba 分词（去停用词）
  - `tokenize_pos(text)`：jieba posseg（词与词性）
  - `normalize_synonyms(tokens)`：同义词映射
  - `preprocess(text, do_pos=False)`：统一接口

输入/输出：字符串 -> token 列表 / (word,pos) 列表

建议：
- 根据研究需要替换 / 扩展分词器（HanLP/pkuseg）以提升词性识别。

---

## sentiment.py

职责：字典法情感分析核心模块，且支持从 CSV 加载词典、否定/程度副词处理与文本级评分。

关键类与函数：
- `LexiconSentimentAnalyzer`：
  - `__init__(lexicon, negations=None, degree_dict=None)`：初始化词典、否定词和程度词
  - `score_text(text) -> dict`：对单条文本打分，返回 {score, pos_count, neg_count, token_count}
  - `classify(score, threshold=0.1) -> 'positive'|'negative'|'neutral'`
- `load_lexicon_csv(path: str) -> Dict[str,float]`：加载不同 header 形式的 CSV

输入/输出：
- 输入：字符串或预处理后的 token 列表
- 输出：score（浮点）、pos/neg token counts

注意：
- loader 增强了头字段兼容（word/词语/token 与 score/情感等）以防数据源差异。
- 支持 degree adverb 和 negation 检测（基于窗口和 token 索引），需按项目扩展词表。

建议：
- 若后续加入基于模型的情感分析（BERT 等），可在此包裹或添加新实现类（ModelSentimentAnalyzer），并在 pipeline 中复选。

---

## supervision.py

职责：构建媒体监督指标（新闻篇数、负面篇数、负面比例、媒体权重加权情绪等）。

关键函数：
- `compute_media_supervision(news_df: pd.DataFrame, media_weights: Dict[str, float] = None) -> pd.DataFrame`：返回公司+年度的监督指标

计算指标举例：
- `total_count`：新闻总数
- `negative_count`：负面新闻条数（label=negative）
- `negative_ratio`：负面占比
- `weighted_sentiment`：使用媒体权重后加权的情绪平均

输入/输出：news_df（新闻级） -> company-year supervision df

建议：
- 扩展可加入文章长度、篇幅/版面权重、媒体来源权重分层（state/major/local）等。

---

## aggregation.py

职责：将新闻/监督指标聚合到公司-年度面板并匹配 ESG 数据。也包含简单预处理（如 year 提取）。

关键函数：
- `aggregate_news_by_company_year(news_df: pd.DataFrame) -> pd.DataFrame`：输出 company/year/mean_sentiment/total_count/negative_count/negative_ratio/weighted_sentiment
- `match_with_esg(summary_df: pd.DataFrame, esg_df: pd.DataFrame, company_map: Dict[str,str] = None) -> pd.DataFrame`：将 summary 和 esg 合并（left join）以形成 panel

输入/输出：
- 输入：news_df (news-level), esg_df (ticker, year, env_score, ...)
- 输出：merged company-year dataset

注意：
- `company_map` 用于将 news 中公司名映射到 esg ticker（模糊匹配/人工对照需在上游完成）。

---

## validation.py

职责：提供描述统计、抽样核查和稳健性方法（如 winsorize、阈值测试）的辅助函数。

关键函数：
- `describe_variables(df, variables)`：返回变量描述性统计
- `sample_for_manual_check(news_df, n_samples, seed)`：随机抽样以便人工核验
- `robustness_checks(df)`：占位函数用于稳健性检验逻辑（可扩展）

用途：
- 在 pipeline 末期做数据质量检查、抽样人审与稳健性分析

---

## pipeline.py

职责：流水线主流程 orchestrator（整合上述模块，按配置执行流程），并写出结果（scored_news.csv / news_summary_company_year.csv / merged_with_esg.csv / descriptive_stats.csv）。

关键步骤：
1. 读取配置 `config_path`
2. 加载新闻 CSV 与公司名单
3. 预处理：tokenize, 去停用词（`pre.process`）并生成 `content_clean`
4. 加载词典（`load_lexicon_csv`），构造 analyzer
5. 对每条新闻 `score_text`，并将 `sentiment_score` 和 `sentiment_label` 写回 news_df
6. 计算媒体监督（`compute_media_supervision`）和汇总（`aggregate_news_by_company_year`）
7. 与 ESG 数据匹配（`match_with_esg`）并导出结果到 `output_dir`

关键函数/位置：
- `run_pipeline(config_path: str)`：入口主函数

参数：
- config 中的 `dict_path`、`news_csv`、`company_csv`、`esg_csv`、`media_weights`、`output_dir`

输出：
- `scored_news.csv`, `news_summary_company_year.csv`, `merged_with_esg.csv`, `descriptive_stats.csv`

扩展点：
- 插入模型预测替代词典打分
- 使用缓存 / 并行化批次打分以提高性能

---

## __init__.py

职责：包导入控制。为避免在导入包时加载 heavy pipeline，再做了 lazy load `run_pipeline()` 的实现（将 `pipeline.run_pipeline` 延迟导入）。

---

## 典型数据格式（对 pipeline/n 模块的输入约定）

`news_df`（必须）列如下：
- `news_id` (str/int)
- `title` (str)
- `content` (str)
- `publish_date` (datetime/string)
- `media` (str)
- `company` (str)

`company_df`（必须）列如下：
- `company_name` (str)
- `ticker` (str)
- `industry` (str, 可选)

`lexicon`：CSV 或 JSON（word -> score）, or final domain lexicon 格式：
- CSV columns: `word,score,polarity,abs_score[,aspect, relevance]`
- For pipeline runtime: `word -> score` dict is expected by `LexiconSentimentAnalyzer`

`esg_df`（可选）列：
- `ticker` (str)
- `year` (int)
- `env_score` (float) or other ESG metrics

---

## 扩展/替换建议
- 若你后期希望用深度学习模型做情感打分，可新增 `src/media_esg/model_sentiment.py` 并在 pipeline 中选择加载该模型而非字典法。
- 公司名称匹配：实现 `fuzzy_match_company()`（rapidfuzz）与 NER 后处理，以提高公司名映射准确率。
- 增加 `scrapers/` 下网站特定爬虫实现，输出规范 CSV 以便 pipeline 统一加载。

---

## 示例（pipeline 运行示例）
```powershell
# 设置环境
cd "F:\Code\Data Mine\media_esg_project"
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
$env:PYTHONPATH = "$pwd/src"

# 编辑 config_example.yml，填入 news_csv / company_csv / dict_path / esg_csv
python .\scripts\run_pipeline.py --config scripts/config_example.yml
```