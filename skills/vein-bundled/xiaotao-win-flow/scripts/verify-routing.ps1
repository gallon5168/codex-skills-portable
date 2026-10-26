# verify-routing.ps1 -- static reference-consistency lint for the xiaotao-win-flow skill.
# Purpose: promote Iron Rule 1 ("confirm a path exists before using it") from a runtime
#          fallback to a static check. Scans every .md in the skill, extracts referenced
#          internal file paths (references/... playbooks/... scripts/*.ps1 templates/*.*
#          and bare `xxx.md` mentions), and verifies each exists on disk.
# Usage:   powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify-routing.ps1
# Exit:    0 = all path-bearing refs resolved; 1 = broken path-bearing ref(s); 2 = self error.
# Note:    ASCII-only on purpose -- PowerShell 5.1 reads .ps1 as the system ANSI codepage,
#          so non-ASCII comments in a BOM-less UTF-8 file get mis-decoded and break parsing.
#          Bare filenames (no path separator) only warn; refs with / or \ that miss are errors.

$ErrorActionPreference = 'Stop'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = [System.IO.Path]::GetFullPath((Join-Path $here '..'))

if (-not (Test-Path (Join-Path $root 'SKILL.md'))) {
    Write-Output "ERROR: cannot locate skill root (SKILL.md missing). Tried: $root"
    exit 2
}

Write-Output "=== xiaotao-win-flow routing/reference consistency check ==="
Write-Output "=== skill root: $root ==="

# Scope: routing-AUTHORITATIVE files only -- the top-level skill docs, the references/
# top level, the playbooks, and each sub-skill's SKILL entry. Deliberately NOT the vendored
# third-party doc mirrors (frida-docs/, anti-debug-db/, ida-re/x64dbg internal docs): those
# are full of example script names (agent.js, dump_region.py) that are prose, not routing links,
# and they maintain their own internal consistency. This lint guards the routing surface.
$mdFiles = New-Object System.Collections.Generic.List[object]
Get-ChildItem -Path $root -Filter *.md -File |
    Where-Object { $_.Name -notmatch '[^\x00-\x7F]' } | ForEach-Object { $mdFiles.Add($_) }
Get-ChildItem -Path (Join-Path $root 'references') -Filter *.md -File -ErrorAction SilentlyContinue |
    ForEach-Object { $mdFiles.Add($_) }
Get-ChildItem -Path (Join-Path $root 'references\playbooks') -Filter *.md -File -ErrorAction SilentlyContinue |
    ForEach-Object { $mdFiles.Add($_) }
foreach ($entry in @('references\ida-re\SKILL.md', 'references\frida-win\SKILL.md',
                     'references\x64dbg\AGENTS.md')) {
    $p = Join-Path $root $entry
    if (Test-Path -LiteralPath $p) { $mdFiles.Add((Get-Item -LiteralPath $p)) }
}

# Token that looks like an internal file path: a known top-level/sub-skill dir prefix + separator,
# or a bare filename with a known extension. The leading lookbehind stops the alternation from
# anchoring on an INNER keyword dir mid-path (which truncated `frida-win/references/x` to
# `references/x` and produced false failures).
$pattern = '(?<![\w./\\-])((?:references|playbooks|scripts|templates|tools|frida-win|ida-re|x64dbg)[/\\][\w./\\-]+|[\w-]+\.(?:md|ps1|py|js))'

$strong = New-Object System.Collections.Generic.List[object]
$weak   = New-Object System.Collections.Generic.List[object]
$seen   = @{}

foreach ($f in $mdFiles) {
    $text = Get-Content -Raw -LiteralPath $f.FullName
    $rxMatches = [regex]::Matches($text, $pattern)   # NOT $matches -- that shadows the -match auto-var
    foreach ($m in $rxMatches) {
        $ref = $m.Groups[1].Value.TrimEnd('.', ',', ')', ':', ';').Replace('\', '/')
        if ([string]::IsNullOrWhiteSpace($ref)) { continue }
        if ($ref -match '^https?:' -or $ref -match '[\*\?]') { continue }
        if ($ref -match '[^\x00-\x7F]') { continue }   # skip mis-decoded / garbled tokens

        $hasSep = $ref.Contains('/')
        $key = $f.FullName + '|' + $ref
        if ($seen.ContainsKey($key)) { continue }
        $seen[$key] = $true

        $candidates = @(
            (Join-Path $root $ref),
            (Join-Path (Join-Path $root 'references') $ref),
            (Join-Path $f.Directory.FullName $ref)
        )
        # Walk ancestor dirs up to the skill root: a vendored sub-skill doc may reference
        # a path relative to its OWN skill root (e.g. `scripts/dump_region.py` inside ida-re/).
        $anc = $f.Directory
        while ($anc -and $anc.FullName.Length -ge $root.Length) {
            $candidates += (Join-Path $anc.FullName $ref)
            if ($anc.FullName -eq $root) { break }
            $anc = $anc.Parent
        }
        $resolved = $false
        foreach ($c in $candidates) {
            if (Test-Path -LiteralPath $c) { $resolved = $true; break }
        }
        if ((-not $resolved) -and (-not $hasSep)) {
            $leaf = Split-Path $ref -Leaf
            $hit = Get-ChildItem -Path $root -Recurse -Filter $leaf -File -ErrorAction SilentlyContinue |
                   Where-Object { $_.FullName -notmatch '\\\.git\\' } | Select-Object -First 1
            if ($hit) { $resolved = $true }
        }

        if (-not $resolved) {
            $rel = $f.FullName.Substring($root.Length).TrimStart('\')
            $rec = [pscustomobject]@{ InFile = $rel; Ref = $ref }
            # Hard-FAIL only when the ref names a specific FILE via a known extension.
            # A path-like token with no extension that resolves as neither file nor dir is
            # almost always prose (e.g. "x64dbg/IDA plugin", "toolA/toolB black-box") -> WARN.
            $namesFile = $ref -match '\.(md|ps1|py|js|txt|json|yaml|yml|exe|dll)$'
            if ($hasSep -and $namesFile) { $strong.Add($rec) } else { $weak.Add($rec) }
        }
    }
}

Write-Output ""
Write-Output "--- scanned $($mdFiles.Count) .md files, $($seen.Count) unique refs ---"

if ($weak.Count -gt 0) {
    Write-Output ""
    Write-Output "[WARN] bare filenames not found (may be prose, not a reference -- verify manually):"
    $weak | Sort-Object InFile, Ref | Format-Table -AutoSize | Out-String | Write-Output
}

if ($strong.Count -gt 0) {
    Write-Output ""
    Write-Output "[FAIL] path-bearing internal references not found (broken links, fix these):"
    $strong | Sort-Object InFile, Ref | Format-Table -AutoSize | Out-String | Write-Output
    Write-Output "$($strong.Count) broken reference(s)."
    exit 1
}

Write-Output ""
Write-Output "[OK] all path-bearing internal references resolve on disk."
exit 0
