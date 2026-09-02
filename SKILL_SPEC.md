# Skill 内容规范

本站以「一个 Markdown 文件 = 一个 Skill」的方式维护内容。你只需要在 `skills/` 目录下新增/修改 `.md` 文件,首页卡片、分类统计、详情页、视频内嵌播放器全部由 `scripts/gen_skills.py` 在构建时自动生成。

## 1. 文件位置与命名

```
skills/
├── web-search.md        # 文件名即 URL slug,用小写英文+连字符
├── doc-summary.md
└── qagent-office.md
```

- 文件名规则:小写字母、数字、连字符,如 `web-search.md`。构建后详情页地址为 `https://openskill.top/skills/web-search/`(中文为默认语言,位于根路径;英文版在 `/en/skills/web-search/`)。
- 文件名即排序依据之一(见 `order` 字段)。

## 2. 文件结构

每个 Skill MD 由 **Front Matter(元信息)** + **正文(自由 Markdown)** 两部分组成。

```markdown
---
title: 联网搜索
description: 实时搜索互联网,获取最新、最相关信息,并返回结构化结果。
category: 信息获取
tags: [搜索, 联网, 实时信息]
badge: 热门
order: 1
cover: /static/skills/web-search.png
video:
  platform: bilibili
  url: https://www.bilibili.com/video/BV1xx411c7mD
  title: 3 分钟上手联网搜索
---

## 功能介绍

这个 Skill 能做什么、解决什么问题……

## 使用场景

- 场景一:……
- 场景二:……

## 使用方法

1. 安装/启用方式……
2. 调用示例……
```

## 3. Front Matter 字段说明

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `title` | ✅ | Skill 名称,显示在卡片与详情页标题 |
| `description` | ✅ | 一句话介绍,显示在卡片上,建议 ≤ 50 字 |
| `category` | ✅ | 所属分类,决定首页左侧分类栏的聚合与计数;可写列表让 Skill 同时归入多个分类,如 `category: [图片制作, 新媒体创作]` |
| `tags` | 否 | 关键词列表,用于首页搜索匹配 |
| `badge` | 否 | 角标,可选值:`热门` / `推荐`;不填则无角标 |
| `order` | 否 | 排序权重,数字越小越靠前;不填默认 999 |
| `cover` | 否 | 卡片封面图路径(放在 `docs/static/` 下);不填则用渐变占位图 |
| `video` | 否 | 视频讲解,见第 4 节;不填则卡片无播放按钮 |

## 4. 视频讲解(可选)

视频通常是第三方平台(B 站、抖音等)上已有博主的介绍视频,**只需粘贴链接**,构建时会自动转成内嵌播放器,访客无需跳转即可观看。

```yaml
video:
  platform: bilibili   # 可选:bilibili / douyin / youtube / local
  url: https://www.bilibili.com/video/BV1xx411c7mD
  title: 视频标题(可选)
```

各平台链接格式:

- **bilibili**:`https://www.bilibili.com/video/BVxxxxxxxx`(推荐,内嵌体验最好)
- **douyin**:`https://www.douyin.com/video/73xxxxxxxxx`(必须用完整链接;手机分享的 `v.douyin.com/xxx` 短链不支持,请先在浏览器打开短链、再复制地址栏的完整链接)
- **youtube**:`https://www.youtube.com/watch?v=xxxx` 或 `https://youtu.be/xxxx`
- **local**:站内自有视频,`url` 填站内路径,如 `/static/posts/qagent/one-minute.mp4`

没有视频的 Skill 直接省略 `video` 字段即可。

## 5. 正文规范

正文为自由 Markdown,建议保持以下结构(均为可选,但保持一致体验更好):

1. `## 功能介绍` — 是什么、解决什么问题
2. `## 使用场景` — 典型使用场景列表
3. `## 使用方法` — 如何安装、启用、调用

正文中的图片请放在 `docs/static/` 下并以 `/static/...` 绝对路径引用。

## 6. 推荐分类(可扩展)

约定俗成的分类名(新分类直接写即可,会自动出现在首页侧栏):

- 信息获取
- 内容创作
- 数据分析
- 效率工具
- 开发与编程
- 图像与设计
- 音频与视频
- 视频制作
- 商业与营销
- 科研教育
- 生活与娱乐

## 7. 完整示例

见 [skills/qagent-office.md](skills/qagent-office.md)(含站内视频)与 [skills/web-search.md](skills/web-search.md)。
