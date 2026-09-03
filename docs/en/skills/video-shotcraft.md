---
title: Video ShotCraft
not_in_nav: true
---

# Video ShotCraft

<div class="os-detail-meta"><span class="os-detail-cat">Video Creation</span><span class="os-tag">Product Promo</span><span class="os-tag">Motion Design</span><span class="os-tag">Remotion</span><span class="os-tag">Shot Recipes</span><span class="os-tag">Beat Sync</span><span class="os-tag">Product Video</span></div>

> Turn Claude Code / Codex into a motion studio — 152 shot recipe cards + Remotion to auto-produce product promos with camera moves, transitions and cinematic sound design.

## Video Demo

<div class="os-video"><iframe src="https://open.douyin.com/player/video?vid=7662394154408639844&amp;autoplay=0" title="我的宣传片动效 Skill - 已开源" loading="lazy" scrolling="no" frameborder="0" allowfullscreen allow="autoplay; fullscreen; picture-in-picture"></iframe></div>

[Watch on the original platform ↗](https://www.douyin.com/video/7662394154408639844){ target="_blank" }

## Introduction

Video ShotCraft is an AI Agent Skill that turns Claude Code / Codex into a motion design studio: point it at your product and it uses [Remotion](https://www.remotion.dev/) to handle storyboarding, animation and sound design, producing cinematic product promos, marketing videos, launch videos or demos — with real page screenshots, 2.5D camera moves, beat-synced editing and cinematic sound.

Core assets:

- **152 shot recipe cards**: organized into 10 functional categories, annotated with usage, pacing, suggested duration, parameters, implementation notes and common pitfalls
- **209 motion styles**: all with online gallery previews, searchable and filterable, referenced by name
- **Complete video template Ink Press**: a proven 36.2s, 1920×1080, 30fps, 10-shot product promo — replace the screenshots and copy to reproduce the same quality
- **Audio library**: 149 sound effects (organized into 16 scene categories) + 5 BGM tracks; pick a scene category first, then a texture
- **Production methodology**: a complete workflow covering asset collection, visual direction, storyboarding, sound design, BGM sync and final QA
- **JianYing export**: export the final cut as a JianYing draft for fine editing; per-shot speed, subtitles and audio tracks stay editable

## Use Cases

- Product promos: launch-event quality promo videos for desktop/web products
- Feature demos: showcase new features with specific shot cards (e.g. deck-deal-flyin, row-embed)
- Brand & marketing: title cards, 2.5D page camera moves, flash cuts, number roll-ups and more ready-made sequences
- Motion asset reuse: call a single shot recipe card to add professional motion to any video project

## Usage

The most direct way is to hand the repo link to your Agent:

1. **Install**: in Claude Code / Codex say `Install this skill for me: https://github.com/Vincentwei1021/video-shotcraft`, or run `npx skills add Vincentwei1021/video-shotcraft`; you can also clone it manually and link it into `~/.claude/skills/` or `~/.codex/skills/`
2. **Generate a promo**: say `Use video-shotcraft to create a promo for my desktop product.` — when no shot is specified, the Skill introduces the built-in templates first and asks
3. **Use the template**: say `Use video-shotcraft to make a promo for my product with the Ink Press template.` — the Agent replaces your screenshots, copy and branding for the fastest path to a final cut
4. **Specify shots**: say `Use the deck-deal-flyin and row-embed shot cards to present this feature.`, or pick shot cards in the [Gallery](https://vincentwei1021.github.io/video-shotcraft/) first

Project: [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)

---

[:material-arrow-left: Back to Skills](../index.md)
