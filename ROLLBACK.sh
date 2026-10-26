#!/usr/bin/env bash
set -euo pipefail
HOME_PATH="${HOME_PATH:-$HOME}"
if command -v pwsh >/dev/null 2>&1 && [[ -f "$(dirname "$0")/rollback.ps1" ]]; then
  exec pwsh -NoProfile -File "$(dirname "$0")/rollback.ps1" -HomePath "$HOME_PATH"
fi
STATE="$HOME_PATH/.codex-skills-portable-state.tsv"
[[ -f "$STATE" ]] || { echo "Rollback state not found: $STATE" >&2; exit 1; }
install_root="$(awk -F '\t' '$1=="INSTALL_ROOT"{print $2}' "$STATE")"
while IFS=$'\t' read -r kind a b; do
  case "$kind" in
    LINK) [[ -L "$a" || -e "$a" ]] && rm -rf -- "$a" ;;
  esac
done < "$STATE"
[[ -n "$install_root" && ( -e "$install_root" || -L "$install_root" ) ]] && rm -rf -- "$install_root"
while IFS=$'\t' read -r kind original backup; do
  if [[ "$kind" == "MOVED" && -e "$backup" ]]; then mkdir -p "$(dirname "$original")"; mv "$backup" "$original"; fi
done < "$STATE"
rm -f -- "$STATE"
echo "ROLLBACK PASS installRootRemoved=true"
