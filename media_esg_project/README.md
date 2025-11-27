# 媒体环保情绪对企业ESG的影响研究 — 项目代码框架

本项目包含收集、清洗、情感分析与变量构建等模块的代码框架，面向中文新闻文本，使用字典法实现情感倾向计算，并将新闻级别指标聚合到公司年度层面，供后续经济计量分析使用。

## 主要目录

- `src/media_esg/` — 模块源码
- `data/dictionaries/` — 情感词典与媒体权重等配置文件
- `scripts/` — 示例运行脚本
- `notebooks/` — 使用示例与探索
- `tests/` — 单元测试

## 快速开始

1. 创建虚拟环境并安装依赖：

```powershell
python -m venv venv; .\venv\Scripts\Activate; pip install -r requirements.txt
```

2. 准备公司清单和新闻数据（或使用爬虫脚本采集）。在运行流水线前，请在 `scripts/config_example.yml` 中设置 `news_csv` 和 `company_csv` 为数据路径。
3. 运行流水线示例：

```powershell
python scripts/run_pipeline.py --config scripts/config_example.yml
```

注意：若要从包路径导入，需要将 `src` 目录加到 PYTHONPATH，或在项目根目录运行以下命令(Windows PowerShell)：

```powershell
$env:PYTHONPATH = "$pwd/src"; python .\scripts\run_pipeline.py --config scripts/config_example.yml
```

## 主要模块（结构概览）

- `data_collection.py` — 爬取/载入新闻数据、公司名单
- `preprocess.py` — 分词、停用词、词性标注、同义词归并
- `sentiment.py` — 基于情感词典，识别正负词并计算分数，支持否定和程度副词处理
- `supervision.py` — 构建媒体监督指标（新闻量、负面新闻占比、媒体权重加权分数）
- `aggregation.py` — 将新闻级变量按公司与年度聚合，匹配 ESG 数据
- `validation.py` — 描述性统计、随机样本人工核验和稳健性检验

### src 模块详细说明
更多 `src` 模块的详细职责、输入/输出与示例见： `src/media_esg/SRC_MODULES.md`（已添加）。

## 测试

运行所有测试：

```powershell
pip install -r requirements.txt
$env:PYTHONPATH = "$pwd/src"
pytest -q
```

## 自定义词典

将中文情感词典放入 `data/dictionaries/` 目录下（例如使用默认的 `dlut_sentiment_lexicon_processed.csv`，或自定义文件名），CSV 的列必须包含 `word` 和 `score`（score 代表情感值，正数为正向情感，负数为负向情感）。

媒体权重可通过放置自定义 YAML 文件在 `data/dictionaries/` 中并在 `scripts/config_example.yml` 的 `media_weights` 字段中指定来使用；如果不提供，则不使用加权。

## 大连理工字典 (DLUT)

项目包含 DLUT 情感词汇库的原始 Excel（`data/dictionaries/大连理工大学情感词汇本体库.xlsx`）。
我们已提供以下处理脚本：

- `scripts/convert_dlut.py`：从 Excel 转换为 CSV（`word, score`，score 已归一化到 -1..1）。
- `scripts/postprocess_lexicon.py`：对 CSV 进行后处理，支持仅保留中文、按阈值分配正负中性标签，并导出子集（positive/negative/neutral）和 JSON 映射。
- `scripts/explore_lexicon.py`：快速查看词典汇总与样例。

使用示例：

```powershell
# 将 excel 转为 csv（默认路径）
$env:PYTHONPATH = "$pwd/src"; python .\scripts\convert_dlut.py

# 后处理并只保留中文词语（默认输出为 data/dictionaries/dlut_sentiment_lexicon_processed.csv）
python .\scripts\postprocess_lexicon.py --input data/dictionaries/dlut_sentiment_lexicon.csv --only_chinese --threshold 0.01

# 探索词典样例
Push-Location 'f:\Code\Data Mine\media_esg_project'; python .\scripts\explore_lexicon.py; Pop-Location
```

## 抽取环保候选词（示例）

我们提供脚本 `scripts/extract_env_lexicon.py`，用于从 DLUT 处理后的词典中抽取与“环保/污染”相关的候选词。

常用参数说明：
- `--input`：输入 CSV（默认 `data/dictionaries/dlut_sentiment_lexicon_processed.csv`）
- `--output`：输出 CSV 路径（默认 `data/dictionaries/dlut_env_candidates.csv`）
- `--keywords`：自定义关键词列表（如 `污染 排放 罚款`）
- `--fuzzy`：启用模糊匹配（使用快速模糊匹配）
- `--fuzzy_threshold`：模糊匹配阈值（0-100，默认 80）
- `--no_seg`：禁用分词匹配，仅使用子字符串与模糊匹配

示例：

```powershell
 # 执行带模糊匹配的抽取，模糊阈值 70
 $env:PYTHONPATH = "$pwd/src"; Push-Location 'f:\Code\Data Mine\media_esg_project'; python .\scripts\extract_env_lexicon.py --fuzzy --fuzzy_threshold 70; Pop-Location
```

脚本会输出 CSV 文件（默认为 `data/dictionaries/dlut_env_candidates.csv`），你可进一步人工校验、合并到主字典或创建主题子词典（如仅环保正向词或负向词）。

建议工作流程：
1. 使用脚本抽取候选词
2. 人工复核与标注（可在 Excel 或 Google Sheets 中完成）
3. 将已核验词加入到你选择的主词典文件（例如 `data/dictionaries/dlut_sentiment_lexicon_processed.csv` 或自定义文件），并按需调整 `score` 值

后续建议：
- 用领域关键字（如包含“污染、排污、罚款、整改、环保”）进行筛选，并在样本中做人工复核以确保情感方向正确。
- 对情感词进行词性校验（只保留形容词/动词/副词等）或由人工校验后再合并到主字典。

## 注意
- 该仓库提供框架及示例实现；具体数据源与情感字典需要根据研究与数据来源自行补充。
- Chinese NLP: 使用 `jieba` 进行分词与词性标注，或根据需要更换为 `pkuseg` / `HanLP`。

## 关于示例数据文件的说明

为避免误用或测试数据残留，项目中以下示例文件已被移除：

- `data/sample_news.csv`
- `data/company_list_sample.csv`
- `data/dictionaries/zh_sentiment_lexicon.csv`
- `data/dictionaries/media_weights.yml`

请自行准备并放置对应数据文件，并在 `scripts/config_example.yml` 中设置 `news_csv`, `company_csv`, `dict_path`, 与 `media_weights` 的路径。
