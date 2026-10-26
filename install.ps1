[CmdletBinding()]
param(
  [string]$HomePath = $HOME,
  [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }),
  [switch]$Force
)
$ErrorActionPreference = 'Stop'
$Repo = $PSScriptRoot
$InstallRoot = Join-Path $CodexHome 'skills\.portable-export'
$AgentRoot = Join-Path $HomePath '.agents\skills'
$CodexSkillsRoot = Join-Path $CodexHome 'skills'
$BackupRoot = Join-Path $HomePath ('.codex-skills-portable-backups\' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$StatePath = Join-Path $HomePath '.codex-skills-portable-state.json'

New-Item -ItemType Directory -Force -Path $AgentRoot,$CodexSkillsRoot,$BackupRoot | Out-Null
$state = [ordered]@{ schema=1; installRoot=$InstallRoot; backupRoot=$BackupRoot; createdLinks=@(); moved=@(); skipped=@() }

function Move-ForBackup([string]$Path, [string]$Label) {
  if (-not (Test-Path -LiteralPath $Path)) { return $true }
  if (-not $Force) { $state.skipped += $Path; return $false }
  $safe = ($Label -replace '[^A-Za-z0-9._-]','_')
  $dest = Join-Path $BackupRoot $safe
  Move-Item -LiteralPath $Path -Destination $dest
  $state.moved += [ordered]@{ original=$Path; backup=$dest }
  return $true
}

if (Test-Path -LiteralPath $InstallRoot) {
  if (-not (Move-ForBackup $InstallRoot 'portable-export')) {
    throw "Install root already exists. Re-run with -Force: $InstallRoot"
  }
}
New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null
$package=(Get-Content -LiteralPath (Join-Path $Repo 'manifest\portable-skills-manifest.json') -Raw -Encoding UTF8|ConvertFrom-Json)
foreach($file in $package.files){
  $repoPath=[string]$file.repo_path
  if($repoPath.StartsWith('skills/vein-bundled/')){
    $relative=$repoPath.Substring('skills/vein-bundled/'.Length)
    $destination=Join-Path (Join-Path $InstallRoot 'vein-bundled') ($relative -replace '/', '\')
  } elseif($repoPath.StartsWith('skills/codex-home/')) {
    $relative=$repoPath.Substring('skills/codex-home/'.Length)
    $destination=Join-Path (Join-Path $InstallRoot 'codex-home') ($relative -replace '/', '\')
  } else { continue }
  $source=Join-Path $Repo ($repoPath -replace '/', '\')
  $sourceLong='\\?\'+[IO.Path]::GetFullPath($source)
  $destinationLong='\\?\'+[IO.Path]::GetFullPath($destination)
  [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($destinationLong)) | Out-Null
  [IO.File]::Copy($sourceLong,$destinationLong,$true)
}

$aliases = Get-Content -LiteralPath (Join-Path $Repo 'manifest\aliases.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($alias in $aliases) {
  $target = Join-Path (Join-Path $InstallRoot 'vein-bundled') ($alias.target -replace '/', '\')
  $targetForLink='\\?\'+[IO.Path]::GetFullPath($target)
  foreach ($root in @($AgentRoot,$CodexSkillsRoot)) {
    $link = Join-Path $root $alias.alias
    if (-not (Move-ForBackup $link ('alias-' + $alias.alias + '-' + ([guid]::NewGuid().ToString('N'))))) { continue }
    New-Item -ItemType Junction -Path $link -Target $targetForLink | Out-Null
    $state.createdLinks += $link
  }
}

$customRoots = Get-Content -LiteralPath (Join-Path $Repo 'manifest\custom-roots.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($name in $customRoots) {
  $target = Join-Path (Join-Path $InstallRoot 'codex-home') $name
  $targetForLink='\\?\'+[IO.Path]::GetFullPath($target)
  $link = Join-Path $CodexSkillsRoot $name
  if (-not (Move-ForBackup $link ('custom-' + $name))) { continue }
  New-Item -ItemType Junction -Path $link -Target $targetForLink | Out-Null
  $state.createdLinks += $link
}

$state | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $StatePath -Encoding UTF8
$definitionCount=@($package.files|Where-Object {$_.repo_path -match '/SKILL\.md$'}).Count
"INSTALL PASS definitions=$definitionCount aliases=$($state.createdLinks.Count) skipped=$($state.skipped.Count) state=$StatePath"
