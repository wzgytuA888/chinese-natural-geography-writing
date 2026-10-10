# 中文自然地理与生态系统服务写作 Skill

根据数据、图表、模型输出或稿件，撰写和修改自然地理、生态系统服务、土地利用与资源环境论文的结果、分析和讨论。重点是数据口径、中心判断、句法搭配、比较逻辑和推论边界。

本次 v2.0 更新保留 52 类写作范式，核验用户提供的《地理学报》《生态学报》各 50 篇文献，共 1,485 页；全量抽取统计，并对 24 篇的相关结构与片段定向核读。原有 37 篇语料与本批未跨批去重，不宣称 137 篇独立文献。详见 [证据和覆盖边界](references/distillation-evidence.md)。

## 安装

```bash
npx skills add https://github.com/wzgytuA888/chinese-natural-geography-writing --skill chinese-natural-geography-writing
```

也可克隆到当前 Agent 的 skills 目录；每个安装位置保持完整目录。更新后按宿主的发现机制重新载入或开启新会话。

## 使用

```text
使用 $chinese-natural-geography-writing，依据下面的数据写结果与分析。
目标：《生态学报》相关研究的表达风格。
指标：模型估算碳储量，单位万t；研究区：某流域。
2000年120，2020年132；只有两期，无显著性检验。
请先核对计算与证据范围，正文自然成段。
```

最好给出：指标定义和单位、时空范围与尺度、观测/模型/情景类型、比较基准、已有统计检验与图表定位。数据少时仍可完成有依据的段落，skill 不以模板补造缺失发现。

## 本轮重点

- 从数据到正文的证据台账和段落决策。
- 主语、指代、并列对照、限定和因果连接的句法规则。
- 总量/强度、百分比/百分点、净变化/总转移、空间关系/时间变化的区分。
- 产水/涵养、静态供需/服务流、q/重要性/因果贡献的概念边界。
- 两刊风格的任务校准、可复算语料统计、原创案例与独立行为演练。

## 文件

| 位置 | 用途 |
|---|---|
| SKILL.md | 精简入口与按任务加载 |
| references/ | 数据写作、句法、论证、期刊校准、证据和示例 |
| chapters/ | 52 类范式；索引见 references/chapter-index.md |
| knowledge/ | 书目、聚合统计、继承卡片与方法口径 |
| scripts/ | 多进程语料统计与数值台账工具 |
| evals/ | 原创测试输入、程序验证及行为评估记录 |

## 本地工具

数值台账只需 Python 标准库：

```bash
python scripts/build_evidence_ledger.py evals/ledger-input.json --output /tmp/ledger.json
python scripts/validate_bundle.py
```

语料统计需 PyMuPDF。提取全文缓存必须在仓库外；压缩包需含本批格式的论文清单 CSV：

```bash
python scripts/distill_corpus.py "论文.pdf.zip" --cache "/private/corpus" --output knowledge --workers 8
```

## 质量与来源

写作规律是综合归纳，不是逐篇原文复刻；示例与测试使用原创模拟数据。仓库不包含 PDF、压缩包、抽取全文或 OCR 页面。书目元数据来自用户清单；引用继承卡片的具体数字前须回查原文。统计口径及限制见 [corpus-findings](references/corpus-findings.md)。

本轮按 [skill-creator](https://github.com/openai/skills/tree/main/skills/.system/skill-creator) 的渐进加载与验证方法，以及 [book-to-skill](https://github.com/virgiliojr94/book-to-skill) 的结构蒸馏方法组织。

skill 能改善写作决策和核验，不能保证任意输入产生与发表论文完全等同的研究质量或获得期刊录用。演练结果只描述所测案例，见 [评估记录](evals/behavioral-evaluation.md)。
