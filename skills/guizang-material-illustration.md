---
title: 歸藏的材质插画
description: 把文章、截图、数据与概念生成带中文标签的歸藏材质插画，让每张配图自己会「讲清楚意思」。
category: [图片制作, 新媒体创作]
tags: [配图, 插画, 图表美化, 解释图, 中文标签]
title_en: Guizang Material Illustration
description_en: Turn articles, screenshots, data and concepts into Guizang-style material illustrations with Chinese labels that actually explain.
category_en: [Image Creation, New Media]
tags_en: [Illustration, Explainer Image, Chart Beautification, Chinese Labels]
repo: https://github.com/op7418/guizang-material-illustration
video:
  platform: douyin
  url: https://www.douyin.com/video/7660055506572119338
  title: 歸藏的材质插画 Skill 介绍
---

## 功能介绍

歸藏的材质插画是一个适配 Claude Code / Codex 等 Agent 环境的配图 Skill，把文章、笔记、图表截图、产品概念、工作汇报、教学材料和人文观点，生成**带中文标签的歸藏材质插画**。

它解决的是「中间那张图」的问题：社交卡片、PPT、文章和文档里经常需要一张能把意思讲清楚的中心配图，而不是一张漂亮但看不懂的装饰图。这个 Skill 专注做三件事：

- **解释图**：把抽象概念、流程、机制、系统关系画成带标签的图
- **图表美化**：从截图或原始数据里抽取语义，重新生成更适合传播的材质化图表
- **参考辅助出图**：遇到冷门概念、品牌、模型、科学装置、历史物件时，先查参考信息和参考图，再统一转成歸藏材质风格

核心特性：

- **图内可以有字**：短标签、箭头、图例和数据标注直接生成在图片里，不把图片降级成无字装饰
- **材质化 3D 图解**：克制的 Swiss editorial 构图、柔和 3D 材质、清楚的空间关系和少量高亮色
- **图表语义重画**：只保留图表类型、标题、数据、坐标、单位、误差线和结论，不复刻原图排版
- **参考搜索辅助**：模型 Logo、技术术语、历史文化物件、科学装置先补事实和视觉线索，再统一风格
- **教育与人文都能接**：小学科学、中学物理、生物化学机制、历史路线、文学意象、社会学概念都可以做成解释图
- **主题色可扩展**：默认 IKB 蓝，也支持柠檬黄、柠檬绿、安全橙、石墨黑等主题方向
- **QA 优先**：交付前检查中文标签、数据、裁切、参考准确性和社交卡片尺寸下的可读性

支持的图解类型：概念拆解图、流程图解、循环机制图、对比图、层级/架构图、场景解释图、科学机制图、人文意象图，以及柱状图、折线图、甘特图、桑基图、热力图、漏斗图等材质化图表。

## 使用场景

- 文章与公众号配图：把长文拆成 1-4 个核心概念，每个概念生成一张带字解释图
- 产品 / 技术说明：先查参考信息，再做流程图、层级图、系统关系图
- 工作汇报配图：用进展、风险、决策、下一步做四象限或流程配图
- 数据图表美化：给糟糕的图表截图换一身体面的材质皮肤，数据和坐标分毫不动
- 教学材料配图：比如给小学科学课文做一张杠杆原理图，图里标出支点、用力点、阻力点和力臂
- 新媒体卡片中心图：先生成中心配图，再交给 Social Card Skill 排成 3:4 小红书卡片

## 使用方法

1. **安装**：执行 `npx skills add https://github.com/op7418/guizang-material-illustration --skill guizang-material-illustration`，或手动 clone 到 `~/.claude/skills/guizang-material-illustration`（Codex 同理）
2. **触发**：直接对 Agent 说「用歸藏的材质插画 skill，帮我把这段产品说明做成一张带中文标签的机制图」，也可以说「做一张带字解释图」「把这张图表美化一下」「这个概念比较冷门，先搜参考信息再生成图」
3. **给出材料**：把文章、截图、数据或说明交给 Agent，Skill 会自动理解材料、判断图型、压缩文案、写生成提示词并调用图像生成能力出图
4. **联动社交卡片**：先让它生成中心图，再把图片交给 `guizang-social-card-skill` 负责标题、正文、主题色和 3:4 / 1:1 / 21:9 尺寸排版

Skill 内部工作流：理解材料 → 内部判断类型 → 必要时查参考 → 压缩文案 → 写生成提示词 → 生成图片 → 检查并重生（中文标签、数据、裁切错了优先重新生成）→ 交付资产。

项目地址：[op7418/guizang-material-illustration](https://github.com/op7418/guizang-material-illustration)
