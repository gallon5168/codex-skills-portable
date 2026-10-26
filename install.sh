#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_PATH="${HOME_PATH:-$HOME}"
CODEX_HOME="${CODEX_HOME:-$HOME_PATH/.codex}"
INSTALL_ROOT="$CODEX_HOME/skills/.portable-export"
AGENT_ROOT="$HOME_PATH/.agents/skills"
CODEX_SKILLS_ROOT="$CODEX_HOME/skills"
STATE="$HOME_PATH/.codex-skills-portable-state.tsv"
BACKUP="$HOME_PATH/.codex-skills-portable-backups/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$AGENT_ROOT" "$CODEX_SKILLS_ROOT" "$BACKUP"
: > "$STATE"
printf 'INSTALL_ROOT\t%s\nBACKUP_ROOT\t%s\n' "$INSTALL_ROOT" "$BACKUP" >> "$STATE"
if [[ -e "$INSTALL_ROOT" || -L "$INSTALL_ROOT" ]]; then mv "$INSTALL_ROOT" "$BACKUP/portable-export"; printf 'MOVED\t%s\t%s\n' "$INSTALL_ROOT" "$BACKUP/portable-export" >> "$STATE"; fi
mkdir -p "$INSTALL_ROOT"
cp -a "$ROOT/skills/vein-bundled" "$INSTALL_ROOT/vein-bundled"
cp -a "$ROOT/skills/codex-home" "$INSTALL_ROOT/codex-home"
python3 - "$ROOT" "$INSTALL_ROOT" "$AGENT_ROOT" "$CODEX_SKILLS_ROOT" "$STATE" "$BACKUP" <<'PY'
import json, os, pathlib, shutil, sys
root, install, agent, codex, state, backup = map(pathlib.Path, sys.argv[1:])
aliases=json.loads((root/'manifest/aliases.json').read_text(encoding='utf-8'))
custom=json.loads((root/'manifest/custom-roots.json').read_text(encoding='utf-8'))
with state.open('a', encoding='utf-8') as out:
    for a in aliases:
        target=install/'vein-bundled'/a['target']
        for base in (agent,codex):
            link=base/a['alias']
            if link.exists() or link.is_symlink():
                out.write(f'SKIPPED\t{link}\n'); continue
            link.symlink_to(target, target_is_directory=True); out.write(f'LINK\t{link}\n')
    for name in custom:
        target=install/'codex-home'/name; link=codex/name
        if link.exists() or link.is_symlink(): out.write(f'SKIPPED\t{link}\n'); continue
        link.symlink_to(target, target_is_directory=True); out.write(f'LINK\t{link}\n')
PY
count="$(find "$INSTALL_ROOT" -name SKILL.md -type f | wc -l | tr -d ' ')"
echo "INSTALL PASS definitions=$count state=$STATE"
