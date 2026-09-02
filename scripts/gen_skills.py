#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 skills/ 目录的 Markdown 文件生成:
  1. docs/zh/index.md          —— Skills 导航首页(分类侧栏 + 搜索 + 卡片网格 + 视频弹窗)
  2. docs/zh/skills/<slug>.md  —— 每个 Skill 的详情页(自动内嵌视频播放器)
  3. docs/static/covers/       —— 构建时自动抓取的视频封面(卡片显示封面,点击弹窗播放)

用法: python scripts/gen_skills.py
Skill 文件规范见 SKILL_SPEC.md。
"""

import html
import json
import re
import sys
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("缺少 PyYAML,请先执行: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
DOCS_ZH = ROOT / "docs" / "zh"
DOCS_EN = ROOT / "docs" / "en"
OUT_DIR = DOCS_ZH / "skills"
COVERS_DIR = ROOT / "docs" / "static" / "covers"

_HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Accept": "*/*",
}


def _http_get(url: str, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers=_HTTP_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_video_cover(slug: str, video: dict) -> str:
    """构建时抓取视频封面到 docs/static/covers/{slug}.jpg,返回站点路径;失败返回空。

    - bilibili: 官方 view API 取 `pic` 封面(图床有 Referer 防盗链,必须下载到本地)
    - douyin: 分享页解析 og:image(图片 CDN 链接带时效签名,同样必须本地化)
    已有本地封面时直接使用(可手动放置封面图),保证离线/CI 构建稳定。
    """
    dest = COVERS_DIR / f"{slug}.jpg"
    if dest.exists() and dest.stat().st_size > 0:
        return f"/static/covers/{slug}.jpg"
    platform = str(video.get("platform") or "").lower()
    url = str(video.get("url") or "")
    img_url = ""
    if platform == "bilibili":
        m = re.search(r"(BV\w+)", url)
        if m:
            try:
                data = json.loads(
                    _http_get(f"https://api.bilibili.com/x/web-interface/view?bvid={m.group(1)}").decode("utf-8")
                )
                img_url = str((data.get("data") or {}).get("pic") or "")
            except Exception:
                img_url = ""
    elif platform == "douyin":
        m = re.search(r"video/(\d+)", url) or re.search(r"modal_id=(\d+)", url)
        if m:
            try:
                page = _http_get(f"https://www.iesdouyin.com/share/video/{m.group(1)}/").decode("utf-8", "ignore")
                mm = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', page) or re.search(
                    r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"', page
                )
                if mm:
                    img_url = html.unescape(mm.group(1))
            except Exception:
                img_url = ""
    if not img_url:
        return ""
    try:
        dest.write_bytes(_http_get(img_url))
        return f"/static/covers/{slug}.jpg"
    except Exception:
        return ""


REQUIRED_FIELDS = ("title", "description", "category")


def _as_list(v) -> list:
    """标量或列表统一转成去空白的字符串列表。"""
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    s = str(v).strip()
    return [s] if s else []

# 徽章样式:中英文徽章值都映射到同一套样式类
BADGE_CLASS = {"热门": "os-badge--hot", "推荐": "os-badge--rec", "Hot": "os-badge--hot", "Featured": "os-badge--rec"}

# 首页界面文案(英文缺失的字段自动回退中文)
UI_TEXT = {
    "zh": {
        "all_cats": "全部 Skills",
        "side_title": "分类",
        "result_count": '共 <b id="os-count">{total}</b> 个结果',
        "search_ph": "搜索你想要的 Skill...",
        "hot_search": "热门搜索",
        "empty": "没有找到匹配的 Skill,换个关键词试试",
        "try_btn": "一键试用",
        "repo_btn": "项目地址",
        "play_aria": "播放视频讲解",
        "watch_on": "在{platform}观看 ↗",
        "close": "关闭",
        "platform_names": {"bilibili": "B站", "douyin": "抖音", "youtube": "YouTube"},
    },
    "en": {
        "all_cats": "All Skills",
        "side_title": "Categories",
        "result_count": '<b id="os-count">{total}</b> results',
        "search_ph": "Search skills...",
        "hot_search": "Popular",
        "empty": "No matching skills found, try another keyword",
        "try_btn": "Try it",
        "repo_btn": "GitHub",
        "play_aria": "Play video",
        "watch_on": "Watch on {platform} ↗",
        "close": "Close",
        "platform_names": {"bilibili": "Bilibili", "douyin": "Douyin", "youtube": "YouTube"},
    },
}


def parse_skill(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: 缺少 Front Matter(--- ... ---)")
    fm = yaml.safe_load(m.group(1)) or {}
    for field in REQUIRED_FIELDS:
        if not fm.get(field):
            raise ValueError(f"{path.name}: 缺少必填字段 `{field}`")
    # 英文正文:可选的 <slug>.en.md(纯 Markdown 正文),缺失时英文详情页回退中文正文
    en_body_path = SKILLS_DIR / f"{path.stem}.en.md"
    body_en = en_body_path.read_text(encoding="utf-8").strip() if en_body_path.exists() else ""
    cats = _as_list(fm["category"])
    if not cats:
        raise ValueError(f"{path.name}: category 不能为空")
    return {
        "slug": path.stem,
        "title": str(fm["title"]),
        "description": str(fm["description"]),
        "category": cats[0],
        "categories": cats,
        "categories_en": _as_list(fm.get("category_en")),
        "tags": [str(t) for t in (fm.get("tags") or [])],
        "title_en": str(fm["title_en"]) if fm.get("title_en") else "",
        "description_en": str(fm["description_en"]) if fm.get("description_en") else "",
        "category_en": str(fm["category_en"]) if fm.get("category_en") else "",
        "tags_en": [str(t) for t in (fm.get("tags_en") or [])],
        "badge_en": str(fm["badge_en"]) if fm.get("badge_en") else "",
        "badge": str(fm["badge"]) if fm.get("badge") else "",
        "order": int(fm.get("order") or 999),
        "cover": str(fm.get("cover") or ""),
        "cover_auto": "",
        "repo": str(fm.get("repo") or ""),
        "video": fm.get("video") or None,
        "body": m.group(2).strip(),
        "body_en": body_en,
    }


def localized(s: dict, lang: str, field: str) -> str:
    """取本地化字段,英文缺失时回退中文。"""
    if lang == "en":
        v = s.get(f"{field}_en") or ""
        if v:
            return v
    return s[field]


def skill_cats(s: dict, lang: str) -> list:
    """取本地化分类列表,英文缺失时回退中文。"""
    return (s["categories_en"] or s["categories"]) if lang == "en" else s["categories"]


def iframe(src: str, title: str) -> str:
    return (
        f'<div class="os-video"><iframe src="{html.escape(src)}" title="{html.escape(title)}" '
        f'loading="lazy" scrolling="no" frameborder="0" allowfullscreen '
        f'allow="autoplay; fullscreen; picture-in-picture"></iframe></div>'
    )


def video_embed(video: dict, skill_title: str) -> str:
    """按平台把视频链接转成内嵌播放器;无法识别时返回跳转链接。"""
    platform = str(video.get("platform") or "").lower()
    url = str(video.get("url") or "")
    title = str(video.get("title") or f"{skill_title} 视频讲解")
    if not url:
        return ""

    if platform == "bilibili":
        m = re.search(r"(BV\w+)", url)
        if m:
            src = f"https://player.bilibili.com/player.html?bvid={m.group(1)}&autoplay=0&high_quality=1&danmaku=0"
            return iframe(src, title)
    elif platform == "youtube":
        m = re.search(r"(?:v=|youtu\.be/|embed/)([\w-]{6,})", url)
        if m:
            return iframe(f"https://www.youtube.com/embed/{m.group(1)}", title)
    elif platform == "douyin":
        m = re.search(r"video/(\d+)", url) or re.search(r"modal_id=(\d+)", url)
        if m:
            # 抖音官方嵌入式播放器(share 链接在 iframe 中会被平台拒绝)
            return iframe(f"https://open.douyin.com/player/video?vid={m.group(1)}&autoplay=0", title)
    elif platform == "local":
        return (
            f'<div class="os-video"><video controls preload="metadata" width="100%">'
            f'<source src="{html.escape(url)}" type="video/mp4">您的浏览器不支持视频播放。</video></div>'
        )

    # 兜底:无法内嵌时给出原站链接
    return (
        f'<p class="os-video-link"><a href="{html.escape(url)}" target="_blank" rel="noopener">'
        f"观看视频讲解:{html.escape(title)}</a></p>"
    )


def render_card(s: dict, lang: str = "zh") -> str:
    t = UI_TEXT[lang]
    slug = s["slug"]
    title = localized(s, lang, "title")
    desc = localized(s, lang, "description")
    cats = skill_cats(s, lang)
    cat = " · ".join(cats)
    tags = (s["tags_en"] or s["tags"]) if lang == "en" else s["tags"]
    badge = (s.get("badge_en") or s["badge"]) if lang == "en" else s["badge"]
    badge_html = ""
    if badge:
        badge_cls = BADGE_CLASS.get(badge, "")
        badge_html = f'<span class="os-badge {badge_cls}">{html.escape(badge)}</span>'
    search_text = html.escape(
        " ".join([title, desc, cat, *tags, s["title"], s["description"], *s["tags"]]).lower()
    )
    repo_html = ""
    if s.get("repo"):
        repo_html = (
            f'<a class="os-btn os-btn--ghost" href="{html.escape(s["repo"])}" target="_blank" rel="noopener">{t["repo_btn"]}</a>')
    else:
        repo_html = ""
    # 有视频:封面(手动 cover > 自动抓取 > 深色占位)+ 中央播放三角,点击弹窗放大播放;纯文字 Skill 不显示封面
    cover_html = ""
    if s["video"]:
        img = s.get("cover") or s.get("cover_auto") or ""
        orient = "os-cover--vertical" if str(s["video"].get("platform") or "").lower() == "douyin" else ""
        img_html = (
            f'<img src="{html.escape(img)}" alt="{html.escape(title)}" loading="lazy">' if img else ""
        )
        play = (
            '<span class="os-play" aria-hidden="true">'
            '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.5v13l11-6.5z"/></svg></span>'
        )
        cover_html = (
            f'<button class="os-cover os-cover--video {orient}" type="button" '
            f'aria-label="{t["play_aria"]}" onclick="osOpenVideo(\'{slug}\')">{img_html}{play}</button>'
        )
    elif s["cover"]:
        cover_html = (
            f'<div class="os-cover"><img src="{html.escape(s["cover"])}" '
            f'alt="{html.escape(title)}" loading="lazy"></div>'
        )

    return f"""
      <article class="os-card" data-cat="{html.escape("|".join(cats))}" data-search="{search_text}">
        <a class="os-card-main" href="skills/{slug}/">
          <div class="os-card-head">
            <span class="os-card-cat">{html.escape(cat)}</span>
            {badge_html}
          </div>
          <h3 class="os-card-title">{html.escape(title)}</h3>
          <p class="os-card-desc">{html.escape(desc)}</p>
        </a>
        {cover_html}
        <div class="os-card-foot">
          <a class="os-btn" href="skills/{slug}/">{t["try_btn"]}</a>
          {repo_html}
        </div>
      </article>"""


def render_homepage(skills: list, lang: str = "zh") -> str:
    t = UI_TEXT[lang]
    categories: dict = {}
    for s in skills:
        for cat in skill_cats(s, lang):
            categories.setdefault(cat, []).append(s)

    total = len(skills)
    cat_items = [
        '<button class="os-cat active" data-cat="all" type="button">'
        f'<span class="os-cat-name">{t["all_cats"]}</span><span class="os-cat-count">{total}</span></button>'
    ]
    for cat, items in categories.items():
        cat_items.append(
            f'<button class="os-cat" data-cat="{html.escape(cat)}" type="button">'
            f'<span class="os-cat-name">{html.escape(cat)}</span>'
            f'<span class="os-cat-count">{len(items)}</span></button>'
        )

    # 热门搜索:取出现频率最高的 6 个标签(英文站优先用英文标签,缺失回退中文)
    tag_freq: dict = {}
    for s in skills:
        tags = (s["tags_en"] or s["tags"]) if lang == "en" else s["tags"]
        for tg in tags:
            tag_freq[tg] = tag_freq.get(tg, 0) + 1
    hot_tags = sorted(tag_freq, key=lambda tg: -tag_freq[tg])[:6]
    hot_html = "".join(
        f'<button class="os-hot-tag" type="button">{html.escape(tg)}</button>' for tg in hot_tags
    )

    cards = "\n".join(render_card(s, lang) for s in skills)
    sidebar = "".join(cat_items)

    def _video_tpl(s: dict) -> str:
        v = s["video"]
        p = str(v.get("platform") or "").lower()
        url = str(v.get("url") or "")
        ext_url = url if p in t["platform_names"] else ""
        vert = ' data-vertical="1"' if p == "douyin" else ""
        return (
            f'<template id="os-video-{s["slug"]}"{vert} data-url="{html.escape(ext_url, quote=True)}" '
            f'data-platform="{t["platform_names"].get(p, "原平台" if lang == "zh" else "platform")}">{video_embed(v, s["title"])}</template>'
        )

    video_templates = "\n".join(_video_tpl(s) for s in skills if s["video"])

    if lang == "en":
        hero_title = 'Discover &amp; Use<br>Powerful <span class="os-grad">Agent Skills</span>'
        hero_sub = "Explore, learn and launch AI skills in one click to make your Agent stronger"
    else:
        hero_title = '发现与使用<br>强大的 <span class="os-grad">Agent Skills</span>'
        hero_sub = "探索、学习并一键使用各类 AI 技能,让你的 Agent 更强大"
    watch_tpl = t["watch_on"]

    return f"""---
title: Skills
hide:
  - navigation
  - toc
---

<div class="os-home">
  <section class="os-hero">
    <div class="os-hero-inner">
      <div class="os-hero-text">
        <div class="os-eyebrow">OpenSkill &middot; Agent Skills Directory</div>
        <h1>{hero_title}</h1>
        <p class="os-hero-sub">{hero_sub}</p>
        <div class="os-search">
          <input id="os-search-input" type="search" placeholder="{t["search_ph"]}" autocomplete="off">
          <span class="os-search-hint" aria-hidden="true">&#8984;K</span>
        </div>
        <div class="os-hot"><span>{t["hot_search"]}</span>{hot_html}</div>
      </div>
      <div class="os-hero-stage" aria-hidden="true">
        <div class="os-stage" id="os-stage">
          <div class="os-ring os-ring--1"></div>
          <div class="os-ring os-ring--2"></div>
          <div class="os-ring os-ring--3"></div>
          <div class="os-orb"></div>
          <div class="os-glow"></div>
          <div class="os-beam os-beam--1"></div>
          <div class="os-beam os-beam--2"></div>
          <div class="os-beam os-beam--3"></div>
        </div>
      </div>
    </div>
  </section>

  <div class="os-layout">
    <aside class="os-side">
      <div class="os-side-title">{t["side_title"]}</div>
      <nav class="os-cats">{sidebar}</nav>
    </aside>
    <section class="os-main">
      <div class="os-main-head">
        <span class="os-main-count">{t["result_count"].format(total=total)}</span>
      </div>
      <div class="os-grid" id="os-grid">
{cards}
      </div>
      <div class="os-empty" id="os-empty" hidden>{t["empty"]}</div>
    </section>
  </div>
</div>

{video_templates}

<div class="os-modal" id="os-modal" onclick="if(event.target===this)osCloseVideo()">
  <div class="os-modal-inner">
    <div class="os-modal-box">
      <button class="os-modal-close" type="button" aria-label="{t["close"]}" onclick="osCloseVideo()">&times;</button>
      <div class="os-modal-body" id="os-modal-body"></div>
    </div>
    <a class="os-modal-link" id="os-modal-link" href="#" target="_blank" rel="noopener" hidden></a>
  </div>
</div>

<script>
var OS_I18N = {{ watchOn: "{watch_tpl}" }};

(function () {{
  var cards = Array.prototype.slice.call(document.querySelectorAll(".os-card"));
  var cats = Array.prototype.slice.call(document.querySelectorAll(".os-cat"));
  var input = document.getElementById("os-search-input");
  var count = document.getElementById("os-count");
  var empty = document.getElementById("os-empty");
  var currentCat = "all", query = "";

  function apply() {{
    var shown = 0;
    cards.forEach(function (c) {{
      var ok = (currentCat === "all" || c.dataset.cat.split("|").indexOf(currentCat) !== -1) &&
               (!query || c.dataset.search.indexOf(query) !== -1);
      c.style.display = ok ? "" : "none";
      if (ok) shown++;
    }});
    count.textContent = shown;
    empty.hidden = shown !== 0;
  }}

  cats.forEach(function (btn) {{
    btn.addEventListener("click", function () {{
      cats.forEach(function (b) {{ b.classList.remove("active"); }});
      btn.classList.add("active");
      currentCat = btn.dataset.cat;
      apply();
    }});
  }});

  input.addEventListener("input", function () {{
    query = input.value.trim().toLowerCase();
    apply();
  }});

  document.querySelectorAll(".os-hot-tag").forEach(function (btn) {{
    btn.addEventListener("click", function () {{
      input.value = btn.textContent;
      query = btn.textContent.trim().toLowerCase();
      apply();
    }});
  }});

  // 卡片 3D 倾斜效果
  cards.forEach(function (card) {{
    card.addEventListener("mousemove", function (e) {{
      var r = card.getBoundingClientRect();
      var rx = ((e.clientY - r.top) / r.height - 0.5) * -7;
      var ry = ((e.clientX - r.left) / r.width - 0.5) * 9;
      card.style.transform = "perspective(800px) rotateX(" + rx + "deg) rotateY(" + ry + "deg) translateY(-4px)";
    }});
    card.addEventListener("mouseleave", function () {{
      card.style.transform = "";
    }});
  }});

  // Hero 3D 舞台随鼠标视差
  var stage = document.getElementById("os-stage");
  var hero = document.querySelector(".os-hero");
  if (stage && hero) {{
    hero.addEventListener("mousemove", function (e) {{
      var r = hero.getBoundingClientRect();
      var px = (e.clientX - r.left) / r.width - 0.5;
      var py = (e.clientY - r.top) / r.height - 0.5;
      stage.style.transform = "rotateY(" + px * 18 + "deg) rotateX(" + py * -14 + "deg)";
    }});
    hero.addEventListener("mouseleave", function () {{
      stage.style.transform = "";
    }});
  }}
}})();

function osOpenVideo(slug) {{
  var tpl = document.getElementById("os-video-" + slug);
  if (!tpl) return;
  var box = document.querySelector(".os-modal-box");
  var body = document.getElementById("os-modal-body");
  var link = document.getElementById("os-modal-link");
  body.innerHTML = "";
  box.classList.toggle("os-modal-box--vertical", tpl.dataset.vertical === "1");
  body.appendChild(tpl.content.cloneNode(true));
  var u = tpl.dataset.url || "";
  if (u && link) {{
    link.href = u;
    link.textContent = OS_I18N.watchOn.replace("{{platform}}", tpl.dataset.platform || "");
    link.hidden = false;
  }} else if (link) {{
    link.hidden = true;
  }}
  // 抖音竖屏播放器:固定手机视口渲染后缩放铺满弹窗并居中,按最终尺寸重载一次
  if (window.__osDouyinFit) {{
    window.removeEventListener("resize", window.__osDouyinFit);
    window.__osDouyinFit = null;
  }}
  var f = body.querySelector("iframe");
  if (f && box.classList.contains("os-modal-box--vertical")) {{
    f.classList.add("os-douyin-frame");
    var host = f.closest(".os-video") || box;
    var fit = function () {{
      f.style.transform = "translate(-50%, -50%) scale(" + (host.clientHeight / (330 * 16 / 9)) + ")";
    }};
    fit();
    f.src = f.src;
    window.__osDouyinFit = fit;
    window.addEventListener("resize", fit);
  }}
  document.getElementById("os-modal").classList.add("show");
  document.body.style.overflow = "hidden";
}}

function osCloseVideo() {{
  document.getElementById("os-modal").classList.remove("show");
  document.getElementById("os-modal-body").innerHTML = "";
  var link = document.getElementById("os-modal-link");
  if (link) link.hidden = true;
  if (window.__osDouyinFit) {{
    window.removeEventListener("resize", window.__osDouyinFit);
    window.__osDouyinFit = null;
  }}
  document.body.style.overflow = "";
}}

document.addEventListener("keydown", function (e) {{
  if (e.key === "Escape") osCloseVideo();
}});
</script>
"""


def render_detail(s: dict, lang: str = "zh") -> str:
    title = localized(s, lang, "title")
    cat = " · ".join(skill_cats(s, lang))
    desc = localized(s, lang, "description")
    tags = (s["tags_en"] or s["tags"]) if lang == "en" else s["tags"]
    body = (s.get("body_en") or s["body"]) if lang == "en" else s["body"]
    if lang == "en":
        video_h = "## Video Demo"
        watch_link = "Watch on the original platform ↗"
        back = "Back to Skills"
    else:
        video_h = "## 视频讲解"
        watch_link = "在平台原站观看 ↗"
        back = "返回 Skills 首页"
    parts = [
        "---",
        f"title: {title}",
        "not_in_nav: true",
        "---",
        "",
        f"# {title}",
        "",
        (
            f'<div class="os-detail-meta"><span class="os-detail-cat">{html.escape(cat)}</span>'
            + "".join(f'<span class="os-tag">{html.escape(tg)}</span>' for tg in tags)
            + "</div>"
        ),
        "",
        f"> {desc}",
        "",
    ]
    if s["video"]:
        parts += [
            video_h,
            "",
            video_embed(s["video"], title),
            "",
        ]
        url = str(s["video"].get("url") or "")
        if url and not url.startswith("/"):
            parts += [f'[{watch_link}]({url}){{ target="_blank" }}', ""]
    parts += [
        body,
        "",
        "---",
        "",
        f"[:material-arrow-left: {back}](../index.md)",
        "",
    ]
    return "\n".join(parts)


def main() -> None:
    if not SKILLS_DIR.is_dir():
        sys.exit(f"未找到目录: {SKILLS_DIR}")

    files = sorted(
        p for p in SKILLS_DIR.glob("*.md")
        if not p.name.startswith("_") and not p.name.endswith(".en.md")
    )
    if not files:
        sys.exit("skills/ 目录下没有任何 .md 文件")

    errors = []
    skills = []
    for f in files:
        try:
            skills.append(parse_skill(f))
        except (ValueError, yaml.YAMLError) as e:
            errors.append(str(e))
    if errors:
        sys.exit("Skill 文件解析失败:\n" + "\n".join(errors))

    skills.sort(key=lambda s: (s["order"], s["slug"]))

    # 构建时抓取视频封面(手动 cover 优先;已有本地文件则跳过下载)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    for s in skills:
        if s["video"] and not s["cover"]:
            s["cover_auto"] = fetch_video_cover(s["slug"], s["video"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_ZH / "index.md").write_text(render_homepage(skills, "zh"), encoding="utf-8")
    for s in skills:
        (OUT_DIR / f"{s['slug']}.md").write_text(render_detail(s), encoding="utf-8")

    # 英文首页 + 英文详情页:与中文同构,文案/内容用英文字段(缺失回退中文)
    EN_OUT_DIR = DOCS_EN / "skills"
    EN_OUT_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_EN / "index.md").write_text(render_homepage(skills, "en"), encoding="utf-8")
    for s in skills:
        (EN_OUT_DIR / f"{s['slug']}.md").write_text(render_detail(s, "en"), encoding="utf-8")

    cats = sorted({c for s in skills for c in s["categories"]})
    print(f"已生成中英双语首页 + {len(skills)} 个 Skill 双语详情页(分类: {', '.join(cats)})")


if __name__ == "__main__":
    main()
