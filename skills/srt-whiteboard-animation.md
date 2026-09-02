---
title: SRT 白板手绘动画
description: 将 SRT 字幕转为按叙事顺序绘制的白板手绘视频,分区遮罩编排 + 流式笔迹绘制,逐步添彩,最终导出 MP4。
category: 视频制作
tags: [白板动画, 手绘视频, SRT, 字幕, 视频生成]
title_en: SRT Whiteboard Animation
description_en: Turn SRT subtitles into whiteboard hand-drawn videos that follow the narrative order, with zoned mask orchestration, streaming strokes and step-by-step coloring, then export to MP4.
category_en: Video Creation
tags_en: [Whiteboard Animation, Hand-drawn Video, SRT, Subtitles, Video Generation]
badge_en: ""
repo: https://github.com/geeklee/srt-whiteboard-animation
video:
  platform: bilibili
  url: https://www.bilibili.com/video/BV1jv3c6tEbJ
  title: SRT 白板手绘动画 视频讲解
---

## 功能介绍

将 SRT 字幕转为按叙事顺序绘制的白板手绘视频 Skill。它结合了分区遮罩编排与流式笔迹绘制:每个元素跟随字幕依次出场,笔尖在区域内连续落墨,再逐步添彩,最终导出 MP4。

核心能力:

- 解析 SRT 字幕,按建议的 25–35 秒时长拆分场景,先输出分镜与配图策略
- 按字幕事件而非画面坐标,为元素建立语义化的绘制顺序
- 用 `annotation.json` 管理区域、时序、字幕关联和重叠保护区
- 每个区域采用连续流式笔迹:先 ink 铺线稿,再 color 添彩
- 支持浏览器预览台调整区域、顺序、时间和字幕关联
- 支持逐幕渲染与多幕合并,输出完整 MP4

视觉规范:暖米黄色纸张背景(建议 `#F5EBD7`),深灰色素描线条,红、橙、蓝仅作少量概念性点缀;极简手绘、干净背景与充足留白。

## 使用场景

- 知识讲解视频:把课程、科普内容做成手绘展开的动画
- 故事口播:为口播稿配上随叙事推进的白板绘制画面
- 课程字幕可视化:直接利用现成的 SRT 字幕驱动出场顺序
- 短视频文案:把文案转成吸睛的手绘动画短片

## 使用方法

该 Skill 的关键在于"字幕驱动、逐步确认",每一步完成后等待确认,避免在分镜、线稿或标注尚未定稿时浪费渲染成本:

1. **环境准备**:首次运行 `python scripts/prepare_env.py`,使用独立虚拟环境隔离依赖
2. **解析字幕**:`parse_srt.py` 解析 SRT,输出分镜与配图建议(每幕 25–35 秒)
3. **生成线稿**:确认分镜后,生成统一风格的线稿
4. **创建标注**:结合字幕和原图生成 `annotation.json`,载入浏览器预览台 `preview.html`,调整区域、叙事顺序、时序和字幕关联
5. **逐幕渲染**:`render_stream_whiteboard.py` 按流式笔迹渲染每幕 MP4(先 ink 铺线稿,再 color 添彩)
6. **合并成片**:`merge_scenes.py` 将多幕按字幕分镜顺序合并为完整 MP4

项目地址:[geeklee/srt-whiteboard-animation](https://github.com/geeklee/srt-whiteboard-animation)
