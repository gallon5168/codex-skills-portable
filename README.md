# Codex Skills Portable

Portable, searchable export of the currently installed Codex skill library.

## Contents

- **2,079** Vein/user-library `SKILL.md` definitions.
- **48** custom Codex Home definitions.
- Managed Codex system/plugin definitions are preserved as snapshots for inventory, but are not activated by the installer.
- Searchable inventory in Markdown, CSV and JSON.
- Windows PowerShell and POSIX installers plus verified rollback.

Large packaged binaries, media, dependency trees and caches are intentionally omitted. Skill instructions, bounded references, templates, configuration and source scripts are retained. High-confidence credential-shaped examples are replaced with explicit `<REDACTED_…>` placeholders in the portable copy; original hashes remain in `manifest/portable-skills-manifest.json`.

## Windows install

```powershell
git clone https://github.com/gallon5168/codex-skills-portable.git
cd codex-skills-portable
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Use `-Force` to back up and replace conflicting alias paths:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 -Force
```

Rollback the most recent installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\rollback.ps1
```

## macOS/Linux install

```bash
git clone https://github.com/gallon5168/codex-skills-portable.git
cd codex-skills-portable
bash install.sh
```

Rollback:

```bash
bash ROLLBACK.sh
```

## Verify

```powershell
python tests/verify_package.py
powershell -ExecutionPolicy Bypass -File tests/integration.ps1
```

See `VERIFICATION.txt` for literal test output and `inventory/skill-inventory.md` for the complete categorized index.
