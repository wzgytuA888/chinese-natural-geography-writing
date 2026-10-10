---
name: chinese-natural-geography-writing
description: 根据用户数据、图表、模型结果或稿件，撰写和修改中文自然地理学、生态系统服务及资源环境论文的结果、分析、讨论、摘要与结论；校准句法、学术用词、数值口径、证据强度和段落逻辑，适用于地理学报与生态学报相关研究。
metadata:
  version: "2.0.0"
---

# 中文自然地理与生态系统服务论文写作

目标是把真实数据转为概念准确、论证清楚、语言自然的分析文字。保留原有 37 篇语料的提炼结构，本次核验《地理学报》《生态学报》各 50 篇、共 1,485 页；两批未做跨批唯一文献去重。52 类范式按需加载，新增规则和统计依据见 [references/distillation-evidence.md](references/distillation-evidence.md)。

## 先做正确的判断

1. **事实先于句式**。识别研究问题、论文部分、指标定义、单位、尺度、时间、比较基准，以及观测/模型/情景类型。信息足够时直接完成任务；只询问会改变当前结论的缺项。
2. **计算先于修辞**。核对变化量、相对增幅、百分点、总量与强度、净转移与总转移。未给检验不写显著；只有两端点不写持续增长、波动或突变。
3. **按模型本义解释**。q 是空间分异解释力，特征重要性是预测重要性，路径系数受设定路径约束。它们不能自动成为物理贡献率、作用方向或因果效应。
4. **条件决定措辞**。空间正相关不能推出时间共增；产水不等于所有涵养功能；供需盈余不等于服务已流动；高耦合不等于良性协调；情景优势须有目标与基准。
5. **结果与解释有边界**。结果报告数据内判断、分解与已有模型检验；讨论解释候选过程、文献差异与限制。未检验的机制明确标为推测，不虚构引文或实测中介。
6. **结构服从信息**。每段通常以中心发现起，接代表性证据、对照或例外。用户未给空间格局、驱动或情景时，无须补齐固定骨架。
7. **语言服务推理**。句子保留明确主语与主判断；“其中、而、因此、进而”各有逻辑条件。统计频次和句长是描述，不能变成词汇禁令或字数配额。

## 按当前任务加载

| 任务 | 必需/相关参考 |
|---|---|
| 给数据写结果或分析 | 先读 [data-to-prose](references/data-to-prose.md)，再读 [grammar-and-collocations](references/grammar-and-collocations.md) |
| 讨论、机制、比较文献、形成启示 | [argumentation-and-boundaries](references/argumentation-and-boundaries.md)；按需读 [logic-templates](references/logic-templates.md) |
| 润色句法、选词、衔接 | [grammar-and-collocations](references/grammar-and-collocations.md)；按需读 [glossary](glossary.md)、[sentence-templates](references/sentence-templates.md) |
| 摘要、引言、方法、结论 | [workflows](references/workflows.md) 中对应部分 |
| 服务、土地利用、供需、权衡、情景 | [ecosystem-services-playbook](references/ecosystem-services-playbook.md) 中对应问题 |
| 指定两刊风格或提供范文 | [journal-calibration](references/journal-calibration.md)；统计依据读 [corpus-findings](references/corpus-findings.md) |
| 找相关研究或范式 | [chapter-index](references/chapter-index.md) 按主题路由；[papers-index](knowledge/papers-index.md) 找论文后核验原文，不自动引用继承卡片的数字 |
| 理解方法和参数的写法 | [method-parameters](knowledge/method-parameters.md)，具体阈值核验用户采用的方法与来源 |
| 示范或行为评估 | [worked-analysis-examples](references/worked-analysis-examples.md)、[quality-rubric](references/quality-rubric.md) |

## 工作与交付

生成时先在内部建立“事实—来源—条件”台账，选择中心发现，组织段落，再逐句回查数字、方向和推断范围。可按需运行 [build_evidence_ledger.py](scripts/build_evidence_ledger.py) 核算明确序列。数字保留用户精度，不补造图号、年份、样本量或 P 值。

润色时保留原事实、术语与引文编号；先修逻辑和证据越级，再改用词与节奏。需要改变实质判断时简短说明依据。结论逐项回应研究问题，不引入正文未论证的新结果。

默认输出用户需要的、自然成段的正文，避免“总体—空间—归因”反复套句。重大缺项可另附一句说明；台账、自检过程和评分只在用户需要时附上。数据不足时交付能够成立的段落，不用华丽措辞掩盖缺项。

局限：skill 提供写作与核验方法，语言接近期刊不等于研究设计和贡献已达到录用标准。语料只支持本样本中的风格归纳；不承诺所有输入均产生专家认定的同等质量。

本地语料处理沿用用户指定环境并使用多 worker；图默认只输出 PNG，Word 公式须用可编辑公式对象。跨设备使用时由当前用户环境覆盖这些本地偏好。
