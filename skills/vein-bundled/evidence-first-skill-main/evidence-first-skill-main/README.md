# Evidence First Skill

[English](README.md) | [中文](README.zh-CN.md)

Evidence First is a portable Codex skill for working in a Fable5-like mode: intent first, evidence before claims, conclusion first, and explicit verification before calling work done.

## Keywords

agent skills, Codex skills, npx skills, skills CLI, AI agents, prompt engineering, evidence-based workflow, verification-first delivery, adversarial review, portable agent methodology, Fable5-like workflow

## What It Is For

This skill is for non-trivial work such as research, analysis, debugging, planning, writing, and code delivery. It is useful when:

- Time is tight, but factual accuracy still matters.
- Sources disagree and claims need to be downgraded or verified.
- The output will be used as decision-making material.
- You want to port the same working style to another model or agent.

## What It Enforces

- Check factual premises in the user's request before acting.
- Attach evidence to every factual claim, number, path, command, or config value.
- Put the conclusion in the first sentence, then support it.
- Replace vague language with numbers, comparisons, examples, or explicit uncertainty.
- Never claim tests passed or work is complete unless verification actually ran.
- Always deliver with five fields: conclusion, premise check, verification, adjacent findings, and pending confirmations.

## Install With npx

List the available skills in this repository:

```bash
npx skills add yinguangyao/evidence-first-skill --list
```

Install globally for Codex:

```bash
npx skills add yinguangyao/evidence-first-skill --skill evidence-first --agent codex --global
```

Install non-interactively:

```bash
npx skills add yinguangyao/evidence-first-skill --skill evidence-first --agent codex --global --yes
```

After installation, start a task that matches the skill description, or explicitly ask Codex to use `evidence-first`.

## Manual Install

You can also clone the repository into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
git clone git@github.com:yinguangyao/evidence-first-skill.git ~/.codex/skills/evidence-first
```

## Portable Use

For another model or agent:

1. Paste the full contents of `methodology.md` into the system prompt or first message.
2. Ask the model to expose scout findings and verification in the deliverable.
3. After it produces output, open a fresh context and paste `review.md` plus the output for adversarial review.
4. Treat every unsupported claim as pending confirmation.

## Files

- `SKILL.md`: Codex skill entry point.
- `methodology.md`: Portable rules that can be pasted into another model's system prompt or first message.
- `phases.md`: Templates for splitting long work into clarify, scout, plan, execute, and deliver phases.
- `review.md`: Adversarial review prompt for a fresh context after producing the deliverable.

## Maintenance Contract

The core rules are duplicated in `SKILL.md` and `methodology.md` so Codex gets the rules immediately while the portable version stays easy to copy. If you change any rule, update both files. `methodology.md` is the source of truth.
