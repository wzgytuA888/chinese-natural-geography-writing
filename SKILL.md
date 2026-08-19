---
name: chinese-natural-geography-writing
description: 分析、修改或生成自然地理学与地理科学领域的中文学术论文，重点处理核心期刊风格、科学问题建构、时空格局描述、驱动与机制解释、不确定性表达，以及摘要、引言、结果、讨论和结论之间的逻辑衔接。不用于虚构数据、文献或因果证据。
---

# 中国自然地理学中文论文写作

本 Skill 从 37 篇自然地理学、资源环境与地理科学中文论文中提炼写作规律。只迁移写作方法、表达策略和论证范式，不复述或复制原文。

## 核心原则

1. **证据决定措辞强度**：描述性结果用“呈现、表现为、反映”；统计或模型证据用“表明、显示、支持”；只有机制证据充分时才用“揭示、驱动、导致”。相关关系不得直接写成因果关系。
2. **按科学推理链组织**：现象或格局 → 影响因素 → 作用路径 → 尺度与情景条件 → 地理或生态意义。
3. **机制必须包含中间过程**：不要只写“A 影响 B”，应交代 A 改变了什么状态或过程，该变化如何传递至 B，以及这一作用受何种尺度、阈值或背景约束。
4. **结果与讨论分工明确**：结果回答“发现了什么”；讨论回答“为什么、与谁一致或不同、在何种条件下成立、意味着什么”。
5. **学术化不等于堆砌术语**：优先提高概念精度、关系清晰度和证据匹配度，再考虑词汇升级。
6. **模型贡献不等于物理因果**：特征重要性、相对贡献、探测力、路径系数和空间回归系数分别回答不同问题，必须按其统计含义表述。
7. **串联模型逐级验证**：多源数据、反演、降尺度、过程模型和下游评价串联时，应交代每一级的验证依据及误差可能如何传递。

## 写作决策框架

### 四层证据表达

- **观测层**：呈现、表现为、具有……特征、总体呈……趋势。
- **比较层**：高于、低于、强于、弱于、差异主要集中于。
- **关联层**：与……显著相关、对……具有促进/抑制作用、响应程度存在差异。
- **机制层**：通过改变……，进而调控……；在……约束下形成……路径；该过程可能与……有关。

不得跨越证据层级。例如，仅有空间相关分析时，不得直接使用“导致”或“决定”。

对于特殊模型结果，优先采用其本义：结构方程写“直接/间接效应”，空间模型写“本地/邻近效应”，机器学习写“预测贡献或重要性”，地理探测器写“空间分异解释力”，相对重要性写“模型内解释份额”。

### 五段推理链

1. **事实锚点**：时间、空间、对象、指标或情景。
2. **格局概括**：趋势、分异、集聚、梯度、阶段、转折或阈值。
3. **因素识别**：自然、人类活动、政策、技术或系统内部因素。
4. **机制解释**：说明因素如何改变水热、物质迁移、土地利用、网络联系或系统结构。
5. **意义提升**：落到理论认识、尺度效应、风险治理、资源配置或生态管理。

## 按任务加载参考文件

- 总体风格分析或全文统一：读取 [references/style-summary.md](references/style-summary.md)。
- 构建引言、讨论或全文框架：读取 [references/logic-templates.md](references/logic-templates.md)。
- 润色句子、补写衔接或表达不确定性：读取 [references/sentence-templates.md](references/sentence-templates.md)。
- 撰写摘要、引言、结果、讨论、结论：读取 [references/workflows.md](references/workflows.md) 中对应部分。
- 快速选词：读取 [glossary.md](glossary.md)。
- 查找可复用论证模式：读取 [patterns.md](patterns.md)。
- 写作前自检：读取 [cheatsheet.md](cheatsheet.md)。
- 需要了解某类论文的具体写法时，按下表读取对应语料提炼文件。

## 语料提炼索引

| 文件 | 适用写作场景 |
|---|---|
| [ch01](chapters/ch01-urban-network-effects.md) | 网络构建、效应识别、异质性讨论 |
| [ch02](chapters/ch02-review-governance-framework.md) | 综述、概念辨析、多尺度治理框架 |
| [ch03](chapters/ch03-resilience-scenario.md) | 冲击情景、韧性阶段、网络调整 |
| [ch04](chapters/ch04-network-evolution-mechanism.md) | 网络空间演化、影响机制 |
| [ch05](chapters/ch05-model-scenario-optimization.md) | 模型—情景—优化方法论文 |
| [ch06](chapters/ch06-case-process-mechanism.md) | 案例研究、过程分期、质性机制 |
| [ch07](chapters/ch07-method-perspective.md) | 方法探索、学科前沿与研究议程 |
| [ch08](chapters/ch08-concept-direction.md) | 概念阐释、研究方向与战略意义 |
| [ch09](chapters/ch09-concept-discrimination.md) | 跨学科概念辨析、测度边界 |
| [ch10](chapters/ch10-transition-zone-trend.md) | 过渡带识别、趋势预测与启示 |
| [ch11](chapters/ch11-theory-system.md) | 理论体系、属性框架与调控逻辑 |
| [ch12](chapters/ch12-remote-sensing-hydrology.md) | 方法潜力、模型对比与验证 |
| [ch13](chapters/ch13-water-sediment-scale.md) | 尺度效应、替代解释、证据讨论 |
| [ch14](chapters/ch14-coupling-coordination.md) | 耦合协调、时空演化与影响因素 |
| [ch15](chapters/ch15-urban-agglomeration-strategy.md) | 空间结构、网络联系与优化策略 |
| [ch16](chapters/ch16-ecosystem-services-drivers.md) | 生态系统服务、驱动阈值与分区调控 |
| [ch17](chapters/ch17-climate-hiatus-stage.md) | 气候停滞、突变检验与阶段比较 |
| [ch18](chapters/ch18-phenology-thermal-requirement.md) | 物候积温需求、冷激过程与多算法验证 |
| [ch19](chapters/ch19-composite-security-pattern.md) | 综合安全评价、空间集聚与多情景影响 |
| [ch20](chapters/ch20-distance-dynamic-effect.md) | 理论争议、距离动态效应与稳健性 |
| [ch21](chapters/ch21-resource-accessibility.md) | 资源点格局、交通可达性与区位潜力 |
| [ch22](chapters/ch22-resource-economy-matching.md) | 资源—经济匹配、要素弹性与增长阻尼 |
| [ch23](chapters/ch23-multisource-glacier-model.md) | 多源遥感、冰川模型与误差验证链 |
| [ch24](chapters/ch24-climate-season-downscaling.md) | 气候季节划分、降尺度与高海拔误差 |
| [ch25](chapters/ch25-sem-direct-indirect.md) | 结构方程、直接间接效应与路径机制 |
| [ch26](chapters/ch26-mobile-signaling-spatial-types.md) | 手机信令、空间类型归纳与形成因素 |
| [ch27](chapters/ch27-historical-reconstruction-validation.md) | 历史格局重建、串联模型与精度门槛 |
| [ch28](chapters/ch28-gee-crop-disaster.md) | 云平台、作物模型与像元灾损评估 |
| [ch29](chapters/ch29-snowline-remote-monitoring.md) | 雪线遥感提取、阈值率定与代理指标 |
| [ch30](chapters/ch30-environmental-stress-gwr.md) | 环境胁迫、空间溢出与局地回归 |
| [ch31](chapters/ch31-event-process-precipitation.md) | 极端降水事件过程与类型细分 |
| [ch32](chapters/ch32-grass-livestock-scenario-zoning.md) | 草畜平衡、补饲情景与保护分区 |
| [ch33](chapters/ch33-pm25-spatial-spillover.md) | 污染格局、空间溢出与城市群异质性 |
| [ch34](chapters/ch34-relative-importance-productivity.md) | 植被生产力与相对重要性归因 |
| [ch35](chapters/ch35-relational-network-qap.md) | 关系数据、空间网络与QAP机制 |
| [ch36](chapters/ch36-machine-learning-driver-evolution.md) | 机器学习关键因子与阶段演进 |
| [ch37](chapters/ch37-desertification-sensitivity.md) | 沙漠化敏感性、类型转移与驱动探测 |

## 执行要求

1. 先识别用户任务、论文部分、研究对象、数据与证据类型；信息不足时保留限定语，不自行补造。
2. 修改文本时优先修复逻辑断裂、概念漂移、证据越级和结果—讨论混写，再处理词句。
3. 生成内容时维持原有事实、数值、引文编号和研究边界；不得虚构参考文献、统计显著性、样本信息或机制证据。
4. 若用户只要求润色，保留原意和技术含义；若需实质改写，说明关键逻辑调整。
5. 输出应自然、克制、可核验，避免模板机械重复和“显著提升科学性”等空泛表述。

## 质量底线

- 不把“相关”改写为“因果”。
- 不用“揭示机制”替代尚未完成的机制检验。
- 不把政策建议写成脱离结果的口号。
- 不在一个长句中叠加超过三层并列关系；必要时拆成“判断句 + 解释句”。
- 不复制语料论文的连续原句，只使用抽象后的句法与论证结构。
- 不把模型拟合良好写成理论结构得到唯一验证，也不把尺度聚合后的验证外推为更细尺度精度。
