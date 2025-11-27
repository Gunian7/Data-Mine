# 字典说明
本目录下的文件均为用于情感分析的字典文件（之后需要添加领域字典），具体说明如下：

## 主要使用的词典
1. cn_stopwords.txt
2. dlut_sentiment_lexicon_processed.csv
3. dlut_sentiment_lexicon_processed.json (json格式视情况选择)


####  cn_stopwords.txt
作用：中文停用词表，用于文本预处理（去除无意义词、降低噪声）。
使用场景：分词后过滤停用词、构建词频统计和特征提取。
建议：保留并可按研究需要扩展（行业特定停用词）。

#### dlut_sentiment_lexicon.csv
作用：原始从大连理工 Excel 转换得到的 DLUT 词典 CSV（未经或少量处理）。
使用场景：原始数据来源，可以用于复核、对照。
建议：保留备份，不作为 pipeline 的主词典。

#### dlut_sentiment_lexicon_processed.csv
作用：对原始 DLUT 词典做了标准化/清洗后的版本（包含 word、score、polarity、abs_score 等列）。
使用场景：pipeline 主词典（加载到情感分析模块），做情感打分和合并到领域词典。
建议：将此文件设置为默认 dict_path，用作情感打分基础。

#### dlut_sentiment_lexicon_processed_positive.csv / _negative.csv / _neutral.csv
作用：已按情感极性拆分的子集文件（便于逐类快速加载和审查）。
使用场景：如果需要按极性单独分析（比如仅对负面词进行媒体监督变量计数）则直接加载相应文件。
建议：保留以便快速筛选与抽样人工校验。

#### dlut_sentiment_lexicon_processed.json
作用：processed CSV 的 JSON 映射（word -> score / metadata），用于快速运行时加载（内存字典）。
使用场景：情感打分时用作内存加载，提高性能；在 pipeline 中通常作为预加载字典。
建议：生产环境或多次查询时优先使用此文件。

#### dlut_env_candidates.csv / dlut_env_candidates_v2.csv
作用：从 DLUT 中抽取的“环保领域候选词”列表（v2 为更严格/模糊或过滤策略后生成的改进版本）。
使用场景：用于人工标注任务生成（生成上下文例句），用于进一步筛选生成「最终环保词典」。
建议：保留 v2（主候选集），将 v1 备份或删除；用 v2 生成标注任务并做人工核验。

#### lexicon_summary.txt
作用：词典统计汇总（总词数、正/负/中性计数），用于快速检查与报告。
使用场景：开发和验证阶段检查词典分布，做描述性统计与质量控制。
建议：保留并在每次词典变更后更新。
