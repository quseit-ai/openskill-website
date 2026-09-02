# OpenSkill.Top

Agent Skills 聚合导航站 + OpenClaw 公开课文章,使用 MkDocs 构建,支持中英文双语。

## 域名

https://openskill.top

## 站点结构

- **Skills 首页**(`zh/index.md`,自动生成)— 分类导航、搜索、Skill 卡片、视频内嵌播放
- **Skill 详情页**(`zh/skills/<slug>/`,自动生成)— 功能介绍、使用场景、使用方法、视频讲解
- **文章栏目** — 安装配置 / 技能实践 / 技能分享 / 应用案例(原有内容,手动维护)

## 内容维护

### 新增/更新一个 Skill(日常主要操作)

只需在 `skills/` 目录下新增或修改一个 Markdown 文件(文件名即 URL,如 `web-search.md`),字段与写法规范见 **[SKILL_SPEC.md](SKILL_SPEC.md)**。

首页卡片、分类统计、详情页、第三方视频(B 站/抖音/YouTube)内嵌播放器都会在构建时由 `scripts/gen_skills.py` 自动生成,无需手动改任何页面。

### 发布文章

与原来一样:在 `docs/zh/` 对应栏目下新增 `.md`,并在 `mkdocs.yml` 的 `nav` 中登记。

## 本地开发

```bash
# 安装依赖
pip install mkdocs mkdocs-material pyyaml

# 生成 Skills 页面 + 启动开发服务器(改 skills/ 后需重新执行第一行)
python scripts/gen_skills.py
mkdocs serve

# 或一键构建静态站点(内部已包含生成步骤)
./build.sh
```

## 发布上线

```bash
./deploy.sh
```

`deploy.sh` 会自动完成:生成 Skills 页面 → 构建 → 复制到 gh-pages 分支 → 提交 → 确认后推送,推送后 https://openskill.top 自动更新。

## 项目结构

```
openskill.top/
├── mkdocs.yml            # MkDocs 配置(导航、主题)
├── SKILL_SPEC.md         # Skill Markdown 规范 ★ 写内容前先看这个
├── skills/               # Skill 源文件,一个 .md = 一个 Skill ★
├── scripts/
│   └── gen_skills.py     # 生成器:skills/ → 首页 + 详情页
├── docs/
│   ├── zh/               # 中文文章(手动维护)
│   │   ├── index.md      # [自动生成,勿编辑] Skills 导航首页
│   │   ├── skills/       # [自动生成,勿编辑] Skill 详情页
│   │   ├── installation/
│   │   ├── skill-practice/
│   │   ├── skill-sharing/
│   │   └── use-cases/
│   ├── en/               # 英文内容
│   ├── static/           # 图片、视频等静态资源
│   └── stylesheets/extra.css  # 深色科技风主题样式
├── build.sh              # 生成 + 构建
└── deploy.sh             # 生成 + 构建 + 发布到 gh-pages
```
