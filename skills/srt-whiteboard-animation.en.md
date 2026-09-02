## Introduction

An Agent Skill that turns SRT subtitles into whiteboard hand-drawn videos following the narrative order. It combines zoned mask orchestration with continuous stroke drawing: each element enters the stage along with its subtitle, the pen keeps inking inside the zone, colors are added step by step, and the result is exported as MP4.

Core capabilities:

- Parse SRT subtitles and split scenes into suggested 25–35 second segments, outputting storyboard and illustration strategy first
- Build a semantic drawing order for elements based on subtitle events rather than screen coordinates
- Manage zones, timing, subtitle mapping and no-overlap guard areas via `annotation.json`
- Continuous streaming strokes per zone: ink lines first, then color fills
- Browser preview console to adjust zones, order, timing and subtitle mapping
- Scene-by-scene rendering and multi-scene merging into a complete MP4

Visual style: warm beige paper background (suggested `#F5EBD7`), dark gray sketch lines, with red, orange and blue reserved for small conceptual accents; minimal hand-drawing, clean background and generous white space.

## Use Cases

- Knowledge videos: turn lectures and explainers into hand-drawn unfolding animations
- Story voiceovers: pair narration scripts with whiteboard drawing that advances with the story
- Subtitle visualization: drive the entrance order directly from existing SRT subtitles
- Short video copy: convert copy into eye-catching hand-drawn animation shorts

## Usage

The key of this Skill is "subtitle-driven, step-by-step confirmation" — wait for confirmation after each step to avoid wasting rendering cost on unconfirmed storyboards, line arts or annotations:

1. **Environment setup**: run `python scripts/prepare_env.py` on first use, isolating dependencies in a dedicated virtual environment
2. **Parse subtitles**: `parse_srt.py` parses the SRT and outputs storyboard and illustration suggestions (25–35 seconds per scene)
3. **Generate line art**: after confirming the storyboard, generate line arts in a consistent style
4. **Create annotations**: generate `annotation.json` from subtitles and source images, load it into the browser preview console `preview.html`, then adjust zones, narrative order, timing and subtitle mapping
5. **Render scenes**: `render_stream_whiteboard.py` renders each scene to MP4 with streaming strokes (ink lines first, then color)
6. **Merge**: `merge_scenes.py` merges all scenes into the complete MP4 in subtitle order

Project: [geeklee/srt-whiteboard-animation](https://github.com/geeklee/srt-whiteboard-animation)
