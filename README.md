# Chinese Natural Geography Writing Skill

面向自然地理学与地理科学中文论文的 Agent Skill，用于分析、修改和生成符合中文核心期刊表达习惯的摘要、引言、结果、讨论与结论，重点强化科学问题建构、时空格局描述、机制解释、尺度限定和不确定性表达。

本 Skill 依据 16 篇自然地理学、资源环境与地理科学中文论文提炼，并使用 [book-to-skill](https://github.com/virgiliojr94/book-to-skill) 组织为可复用知识结构。仓库内容为对写作方法、语言策略和论证范式的综合归纳，不包含论文全文、原始 PDF 或长段原文复制。

## 安装

```bash
npx skills add https://github.com/wzgytuA888/chinese-natural-geography-writing --skill chinese-natural-geography-writing
```

也可以将本仓库克隆到 Codex 技能目录：

```bash
git clone https://github.com/wzgytuA888/chinese-natural-geography-writing.git ~/.codex/skills/chinese-natural-geography-writing
```

## 内容

- `SKILL.md`：核心写作原则、证据强度和任务路由。
- `chapters/`：16 类地理学论文写法的语料提炼。
- `references/`：风格总结、逻辑模板、句式模板和分部分写作流程。
- `glossary.md`：学术词汇及其证据强度。
- `patterns.md`：可复用的论证模式。
- `cheatsheet.md`：写作决策与交稿前检查表。
- `agents/openai.yaml`：Codex 界面元数据。

## 使用示例

```text
使用 $chinese-natural-geography-writing 润色这段讨论，并检查是否把相关关系误写成因果关系。
```

## 版权说明

本仓库只包含综合提炼后的写作规律和原创组织结构，不提供源论文文本。使用者仍应遵守相关论文、数据和参考文献的版权及引用规范。

