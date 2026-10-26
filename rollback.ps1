[CmdletBinding()]
param([string]$HomePath = $HOME)
$ErrorActionPreference = 'Stop'
$StatePath = Join-Path $HomePath '.codex-skills-portable-state.json'
if (-not (Test-Path -LiteralPath $StatePath)) { throw "Rollback state not found: $StatePath" }
$state = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($link in @($state.createdLinks)) {
  if (Test-Path -LiteralPath $link) { Remove-Item -LiteralPath $link -Force }
}
if (Test-Path -LiteralPath $state.installRoot) {
  $resolved=[IO.Path]::GetFullPath([string]$state.installRoot)
  if (-not $resolved.EndsWith('.portable-export')) { throw "Unexpected install root in rollback state: $resolved" }
  [IO.Directory]::Delete(('\\?\'+$resolved), $true)
}
foreach ($item in @($state.moved)) {
  if (Test-Path -LiteralPath $item.backup) {
    $parent = Split-Path -Parent $item.original
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    Move-Item -LiteralPath $item.backup -Destination $item.original
  }
}
Remove-Item -LiteralPath $StatePath -Force
"ROLLBACK PASS restored=$(@($state.moved).Count) removedLinks=$(@($state.createdLinks).Count) installRootRemoved=$(-not (Test-Path -LiteralPath $state.installRoot))"
