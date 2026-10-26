# ida-reverse-engineering

A [Codex](https://openai.com) skill that drives IDA Pro through the [IDA Pro MCP](https://github.com/mrexodia/ida-pro-mcp) like a senior reverse engineer: instead of narrating raw decompiler output, it transforms the database — renaming functions and variables, recovering structs, fixing types, and adding comments.

## What's inside

- **SKILL.md** — the skill itself: iterative cleanup loop, anti-hallucination rules, triage / deobfuscation / library-resolution pre-pass, a definition-of-done, and game-binary reversing (Unity/IL2CPP, Unreal, RTTI, anti-cheat/DRM)
- **references/** — methodology, tool reference, game RE notes, and a reading list
- **scripts/** — bundled IDAPython helpers: triage, struct recovery, stack-string recovery, crypto constant scanning, string/xref mapping, function fingerprinting and capability tagging, region dumps, progress/report export

## Install

Copy this repository into your Codex skills directory:

```
git clone https://github.com/Newmcpe/ida-reverse-engineering-skill "$HOME/.codex/skills/ida-reverse-engineering"
```

The skill triggers automatically when you reverse a binary with IDA Pro over MCP — e.g. "reverse engineer this binary", "clean up this IDB", or "make this pseudocode readable".

## Requirements

- IDA Pro with an MCP server ([mrexodia/ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) or idalib-mcp) connected to Codex

## License

[WTFPL](LICENSE)
