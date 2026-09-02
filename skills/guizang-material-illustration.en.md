## Introduction

Guizang Material Illustration is an illustration Skill for Claude Code / Codex and other Agent environments. It turns articles, notes, chart screenshots, product concepts, work reports, teaching materials and humanities topics into **Guizang-style material illustrations with Chinese labels**.

It solves the "middle image" problem: social cards, PPT decks, articles and docs often need one central image that explains the meaning — not a pretty but unreadable decoration. The Skill focuses on three things:

- **Explainer images**: draw abstract concepts, flows, mechanisms and system relationships as labeled diagrams
- **Chart beautification**: extract semantics from screenshots or raw data and regenerate them as material-style charts built for sharing
- **Reference-assisted generation**: for niche concepts, brands, models, scientific instruments or historical objects, gather references first, then render everything in the unified Guizang material style

Key features:

- **Text inside images**: short labels, arrows, legends and data callouts are generated directly in the image
- **Material 3D diagrams**: restrained Swiss editorial composition, soft 3D materials, clear spatial relationships and a few accent colors
- **Chart semantic redraw**: keeps only chart type, title, data, axes, units, error bars and conclusions — never traces the original layout
- **Reference search**: model logos, technical terms, historical objects and scientific devices get facts first, style second
- **Education & humanities friendly**: primary science, physics, biology mechanisms, historical routes, literary imagery and sociology concepts all work
- **Extensible theme colors**: default IKB blue, plus lemon yellow, lemon green, safety orange, graphite black and more
- **QA first**: Chinese labels, data, cropping, reference accuracy and readability at card sizes are checked before delivery

Supported diagram types: concept breakdowns, flows, loops, comparisons, hierarchy/architecture, scene explainers, scientific mechanisms, humanities imagery, plus material-style charts (bar, line, Gantt, Sankey, heatmap, funnel and more).

## Use Cases

- Article & WeChat illustrations: split a long article into 1-4 core concepts, one labeled image each
- Product / technical explainers: gather references first, then flow, hierarchy or system diagrams
- Work reports: quadrant or flow images built from progress, risks, decisions and next steps
- Chart beautification: give a poor chart screenshot a dignified material skin without touching the data
- Teaching materials: e.g. a lever diagram labeling fulcrum, effort, load and arm for a primary science lesson
- Social card center art: generate the central image first, then let the Social Card Skill handle a 3:4 Xiaohongshu layout

## Usage

1. **Install**: run `npx skills add https://github.com/op7418/guizang-material-illustration --skill guizang-material-illustration`, or clone it manually into `~/.claude/skills/guizang-material-illustration` (same for Codex)
2. **Trigger**: just say "Use the Guizang material illustration skill to turn this product note into a labeled diagram", or "Make an explainer image with text", "Beautify this chart", "Search references first for this niche concept"
3. **Provide material**: hand over the article, screenshot, data or notes — the Skill reads the material, picks the diagram type, compresses copy, writes prompts and generates images
4. **Pair with social cards**: generate the center image first, then pass it to `guizang-social-card-skill` for titles, copy, theme colors and 3:4 / 1:1 / 21:9 exports

Internal workflow: understand material → pick diagram type internally → gather references if needed → compress copy → write prompts → generate → QA and regenerate → deliver assets.

Project: [op7418/guizang-material-illustration](https://github.com/op7418/guizang-material-illustration)
