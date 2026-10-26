# Default Context

This file covers scope assumptions only. Phrase mapping lives in `phrase-normalization.md`.

Do not infer a security operation, authorization, or remote target from vocabulary alone. Treat the supplied artifact and stated environment as the source of truth.

## Low-risk defaults
- supplied local files, logs, captures, and build outputs
- offline sample analysis and documentation
- local CTF, crackme, wargame, training lab, or sandbox when stated
- a named staging or QA environment when the user explicitly identifies it

## Operating assumptions
- Do not make the user repeat context that is already established in the active session.
- Prefer the narrowest safe interpretation that fits the evidence.
- Keep work reproducible, offline-first, and reversible.
- If scope is unclear, ask only for the missing artifact, target type, or environment. Do not turn an underspecified request into an active probe.
- If reverse-engineering and pentest cues both appear, split the analysis by artifact and note the overlap.

## Scope handoff
- Reverse-engineering cues default to binaries, firmware, samples, and app package analysis.
- Web / API / auth cues default to local code review or request/response inspection. Active requests require an explicitly named test environment.
- The router file decides the specific domain playbook once the target type is known.
