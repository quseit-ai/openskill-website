---
title: Video ShotCraft
description: 把 Claude Code / Codex 变成动效工作室,152 张镜头配方卡 + Remotion,自动产出带镜头运动、转场与电影级音效的产品宣传片。
category: 视频制作
tags: [宣传片, 动效, Remotion, 镜头配方, 卡点, 产品视频]
repo: https://github.com/Vincentwei1021/video-shotcraft
video:
  platform: douyin
  url: https://www.douyin.com/video/7662394154408639844
  title: 我的宣传片动效 Skill - 已开源
---

## 功能介绍

Video ShotCraft 是一个 AI Agent Skill,能让 Claude Code / Codex 变成动效设计工作室:指向你的产品,它就会用 [Remotion](https://www.remotion.dev/) 完成分镜、动画与声音设计,产出电影级的产品宣传片、营销视频、发布视频或 Demo——包含真实页面截图、2.5D 镜头运动、卡点剪辑与电影级音效。

核心资产:

- **152 张镜头配方卡**:按 10 大功能分类,标注用途、节奏、建议时长、参数、实现要点与常见避坑
- **209 种动效样式**:全部提供在线 Gallery 动效预览,可搜索、筛选后按名取用
- **完整视频模板 Ink Press**:经过验证的 36.2 秒、1920×1080、30fps、10 镜头产品宣传片,替换产品截图与文案即可复刻同等质感
- **音频库**:149 个音效(按 16 类场景组织)+ 5 首 BGM,先选场景类别再选音色
- **生产方法论**:素材采集、视觉指导、分镜、声音设计、BGM 卡点、成片 QA 的完整工作流
- **剪映工程导出**:成片可导出为剪映草稿继续精剪,逐镜变速、字幕、音轨均可编辑

## 使用场景

- 产品宣传片:为桌面/Web 产品生成发布会质感的外宣视频
- 功能演示:用指定镜头卡(如 deck-deal-flyin、row-embed)展示新特性
- 品牌与营销片:开场标题卡、2.5D 页面运镜、闪切、数字滚动等成套桥段
- 动效素材复用:单独调用某张镜头配方卡,为任意视频项目补充专业动效

## 使用方法

最直接的方式是把仓库链接交给你的 Agent:

1. **安装**:在 Claude Code / Codex 中说 `Install this skill for me: https://github.com/Vincentwei1021/video-shotcraft`,或执行 `npx skills add Vincentwei1021/video-shotcraft`,也可手动 clone 后链接到 `~/.claude/skills/` 或 `~/.codex/skills/`
2. **生成宣传片**:直接说 `Use video-shotcraft to create a promo for my desktop product.`,未指定镜头时 Skill 会先介绍内置模板并询问
3. **使用模板**:说 `Use video-shotcraft to make a promo for my product with the Ink Press template.`,Agent 会替换你的产品截图、文案与品牌,以最快路径成片
4. **指定镜头**:说 `Use the deck-deal-flyin and row-embed shot cards to present this feature.`,或先在 [Gallery](https://vincentwei1021.github.io/video-shotcraft/) 挑选镜头卡再开工

项目地址:[Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)
