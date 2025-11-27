# 脚本工作流说明

### 运行前说明
cd "F:\Code\Data Mine\media_esg_project"
python -m venv venv
.\venv\Scripts\Activate

### 主要脚本
1. run_pipeline.py：整个流水线的入口，按步骤执行：加载数据 -> 预处理 -> 情感打分 -> 媒体监督变量计算 -> 聚合 -> 输出
   
2. 其他脚本主要是用于词典处理、标注任务生成与合并、计算标注一致性等辅助功能 

### 脚本详细功能说明

#### scripts/run_pipeline.py

职责：整个流水线的入口（按 config 加载各模块），按步骤执行：加载数据 -> 预处理 -> 情感打分 -> 媒体监督变量计算 -> 聚合 -> 输出。
输入：config YAML（news_csv, company_csv, dict_path, media_weights 等）
输出：公司年度面板 csv、日志与中间文件（preprocessed_news.csv、scored_news.csv）
关键点：若使用领域词典，把 final_env_lexicon.csv 指定为 dict_path。

#### scripts/convert_dlut.py

职责：把 DLUT Excel 转换成标准 CSV（字段映射、编码处理、score 预处理）
输入：dlut 原始 Excel
输出：dlut_sentiment_lexicon.csv（或 processed.csv，如果 normalize 被启用）
参数示例：--input, --output, --normalize

#### scripts/postprocess_lexicon.py

职责：对 CSV 做标准化清洗（仅中文、归一化 score、分出 polarity/abs_score）、写出 json 和按 polarity 分片文件。
输入：dlut_sentiment_lexicon.csv
输出：dlut_sentiment_lexicon_processed.csv / .json / _positive/.csv
参数示例：--only_chinese, --threshold

#### scripts/extract_env_lexicon_v2.py

职责：从 processed lexicon 里抽取“环保候选词”，用关键词+模糊匹配/语料出现频次约束生成 domain candidate（v2 更严格）
输入：processed lexicon、新闻语料或句子集
输出：dlut_env_candidates_v2.csv
参数示例：--fuzzy --fuzzy_threshold 60 --strict

#### scripts/filter_env_candidates.py

职责：更简单的过滤（环保关键词匹配或 score 阈值）产出用于人工标注的子集
输入：dlut_env_candidates_v2.csv
输出：dlut_env_candidates_v2_filtered.csv
参数示例：--score_thresh 0.2

#### scripts/generate_annotation_tasks.py

职责：为候选词抓取上下文示例句子，生成标注任务 CSV（word, sample_sentence, candidate_score, source）
输入：候选词 csv（dlut_env_candidates_v2.csv）和句子语料（句子 CSV 包含 news_id、sentence、company）
输出：annotation_tasks.csv（Label Studio/Doccano / Excel 可导入）
参数示例：--n_contexts 3 --fuzzy_threshold

#### scripts/compute_iaa.py

职责：计算两位/多位标注者一致性（Cohen / Fleiss Kappa）
输入：标注者导出的 CSV（ann_a.csv, ann_b.csv）
输出：Kappa 指标打印与日志
用途：校验标注指南与标注质量

#### scripts/merge_annotations.py

职责：把多名标注者的 CSV 合并为最终词典（多数投票决定 polarity，intensity 取平均），同时生成待裁决（冲突）项
输入：annotator CSV 文件夹
输出：final_env_lexicon.csv（word, polarity, intensity, aspect, relevance）

#### scripts/export_lexicon_for_pipeline.py

职责：将合并后/经过人工校验的词典转换为 pipeline 需要的最小字段（word, polarity:int, intensity:float）
输出：dlut_env_final_lexicon.csv（可直接作为情感字典）

#### scripts/explore_lexicon.py

职责：生成字典统计（正/负/中性计数），写出 lexicon_summary.txt 便于审阅
输入：任意 lexicon file
输出：lexicon_summary.txt