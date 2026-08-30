---
title: Self-Evolving AI Agents on Claude: Warp's Practice at Scale
date: 2026-08-28
version: 1.0
tags: [Claude, Agent Skills, Self-Evolving, AI Agent, Warp, Code Review, Workflow]
---

# Self-Evolving AI Agents on Claude: Warp's Practice at Scale

As AI agents go mainstream, most general-purpose agents share common pain points: unstable output, no ability to iterate on themselves, and poor fit for specialized development scenarios. Even when the initial prompt gets 80% of the task right, the user experience still suffers from messy, inconsistent output. Warp ran headfirst into this problem and reworked its product strategy around it, polishing the experience for nearly a million developers worldwide.

Founded in 2020, Warp focuses on AI-native terminals and agent development environments, built on the Claude platform. Its tech stack spans Rust, Golang, GitHub Actions, and Oz, its in-house agent orchestration platform. The company has raised $73 million in total funding, serves 800K monthly active developers, and is used by 56% of the Fortune 500. The platform has hosted over 10 million Claude Code sessions, runs more than 400K sessions per week, and its agents have exchanged over 40 million messages. That said, Warp's internal code review agent once had a messy-output problem — engineers complained it produced useless comments of low quality.

The team's first fix was reactive: manually rewriting prompts based on issues exposed during code review. This improved output usability, but it didn't scale. Tuning context config files such as AGENTS.md helped somewhat, yet still treated the symptom rather than the cause.

Eventually the team identified the core issue: no matter what job an agent performs, once a session ends, feedback about the agent is usually lost — leaving the agent's iteration loop missing its most critical input. Their solution: build a framework based on Agent Skills to create self-improving agents, so that feedback keeps accumulating and output quality keeps getting polished over time.

---

## Company Overview: Warp's AI Development Capability Has Reached Scale

Public records show that Warp, founded in 2020, is a professional AI terminal and intelligent development environment provider serving developers worldwide, with mature commercialization and technical delivery capabilities. To date, the company has raised $73 million, serves 800K monthly active developers, and counts 56% of the Fortune 500 among its users.

Within the Claude ecosystem, the Warp platform has run over 10 million Claude Code sessions, adds more than 400K effective sessions per week, and its agents have exchanged over 40 million messages — making it one of the most widely deployed, most broadly applied developer tools in the Claude ecosystem. Its technical approach carries substantial reference value for the industry.

According to the team, Warp's own code review agent previously exhibited problems common across the industry: verbose output, unprofessional review suggestions, and poor alignment with business standards, hurting team productivity. Early optimization attempts — manually editing prompts and tuning context config files — delivered only temporary improvements, with no scalable, sustainable iteration mechanism, so agent capability never kept improving.

After further technical iteration, Warp settled on its core optimization direction: abandoning traditional prompt-stacking in favor of a self-improving agent system built on Claude's file-based Agent Skills architecture — one that continuously accumulates knowledge, reviews itself automatically, and collaborates with humans.

---

## Core Architecture: A Two-Layer Skill Loop for Autonomous Agent Evolution

The self-improving agent framework is built on a two-layer skill architecture. By separating business execution from retrospective optimization, combined with a human final-review mechanism, it closes the full loop of "business execution — feedback collection — autonomous optimization — capability update," solving the capability-stagnation problem of traditional agents.

### 1. Inner Layer — Base Skills: Standardized Business Execution

Base skills are the agent's core business execution modules. They encapsulate domain knowledge, workflows, industry standards, and business rules as standalone files, replacing lengthy prompt configurations. Day-to-day automated work such as code review, issue triage, and requirement analysis all runs on these modules — no redundant context reloading needed, which improves both stability and efficiency.

### 2. Outer Layer — Iteration Skills: Automated Retrospection and Optimization

Iteration skills are the framework's core innovation. They do not participate in business execution; instead, they run autonomously on a schedule. Their job is to harvest and organize human feedback — misjudgments, non-compliant output, missed business rules, and other optimization signals.

The module automatically compares the agent's historical output against human corrections, distills business rules, produces minimal, fine-grained skill update proposals, and submits update PRs automatically — turning human feedback into technical optimization with no manual plumbing.

### 3. Human Final Review: Keeping AI Evolution Under Control

To mitigate compliance risks and logic gaps from autonomous iteration, the framework keeps humans in the loop for final review. Every automated skill-modification proposal must pass a standardized human review process; only after approval and merge does the optimization take effect and propagate to the agent's business modules. This preserves the efficiency of AI-driven iteration while keeping humans in control, preventing capability drift.

---

## Field Case: GitHub Issue Triage Proves the Iteration Loop

Warp validated the framework publicly using its GitHub Issue triage scenario. Its issue classification agent automatically estimates ticket difficulty, applies labels, and suggests fix directions. But the first version of its base skill had a rule gap: it couldn't recognize the "ready to spec" label, so some business tickets were triaged inaccurately.

To fix it, maintainers submitted precise feedback directly in existing ticket comments — clarifying when the label applies and how to judge it. No extra forms were required; the optimization signal was captured through the existing workflow.

The outer iteration skill then triggered automatically, harvesting the valid feedback via companion scripts and distilling a standardized business rule: genuine business tickets should be labeled "ready to spec" even when no concrete UI/UX plan has been spelled out. Based on that rule, the module automatically modified the base skill file and opened an update PR. Once humans approved and merged it, the agent upgraded immediately, closing the classification gap for good.

According to Warp, a single piece of precise human feedback becomes permanent agent capability. As scenario-specific feedback keeps accumulating, agent capability keeps iterating and accuracy keeps rising. The model is now fully deployed across Warp's open-source repositories, covering requirement writing, code review, and issue handling.

---

## Six Ground Rules for Building Self-Improving Agents

Drawing on its experience at scale, the Warp team published six development guidelines for self-improving agents, offering a standardized reference for similar projects:

1. **Prefer principle-based guidance**: avoid rigid piles of fine-grained rules; lead with directional, first-principles guidance that leaves room for reasoning and improves generalization across scenarios.
2. **Document the "why" behind rules**: annotate business rules with their rationale inside skill files, so the agent understands execution logic rather than mechanically copying instructions — essential for complex, changing business scenarios.
3. **Low-friction feedback collection**: embed feedback entry points into existing workflows (PRs, tickets, comments) so no extra user action is needed, keeping optimization signals flowing continuously.
4. **Prioritize feedback quality**: precise, scenario-specific feedback from domain experts is worth far more than volumes of shallow feedback — it's the core effective signal for agent iteration.
5. **Keep skill architecture lightweight**: use progressive disclosure — split skill files, resource scripts, and reference documents, loading context on demand to avoid bloat and improve runtime efficiency.
6. **Reuse the iteration core**: retrospective outer skills are generic — build once, reuse across code review, issue handling, requirement management, and more, dramatically cutting development cost.

---

## Industry Impact: A New Paradigm for Iterating AI Agents at Scale

Industry analysts note that traditional AI agent development is human-adapts-to-AI: staff repeatedly debug prompts, patch output bugs, and tune parameters — costly, slow, and incapable of continuous evolution.

The solution jointly delivered by Warp and Anthropic flips that model, letting AI adapt proactively to the business. Corrections, business standards, and hands-on know-how from daily work all automatically settle into the agent's fixed capabilities, transforming AI from a one-off automation tool into a digital asset that grows and adapts to the business over the long term.

Built on Claude's mature skills architecture, the approach is low-friction, reusable, scalable, and controllable. It addresses the core enterprise pain points of deploying agents — hard to land, slow to iterate, poor to adapt — and offers a fresh technical paradigm for AI automation, enterprise agent deployment, and industry AI adoption. It may well define the mainstream direction of next-generation agent technology.
