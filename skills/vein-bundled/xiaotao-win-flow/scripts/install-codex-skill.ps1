[CmdletBinding(SupportsShouldProcess=$true)]
param(
    [string]$Destination = (Join-Path $env:USERPROFILE '.codex\skills\xiaotao-win-flow')
)

$ErrorActionPreference = 'Stop'
$source = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$skill = Join-Path $source 'SKILL.md'
if (-not (Test-Path -LiteralPath $skill)) {
    throw "Source skill root is invalid: $source"
}

$destFull = [System.IO.Path]::GetFullPath($Destination)
if ($destFull.TrimEnd('\') -eq $source.TrimEnd('\')) {
    Write-Output "Already at destination: $destFull"
    exit 0
}

$parent = Split-Path -Parent $destFull
if ($PSCmdlet.ShouldProcess($destFull, 'copy Codex skill')) {
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    # Copy/update only; this script never removes destination files.
    # Copy the source contents into the destination. Using the directory itself
    # would create a nested <dest>\xiaotao-win-flow when <dest> already exists.
    New-Item -ItemType Directory -Force -Path $destFull | Out-Null
    Copy-Item -Path (Join-Path $source '*') -Destination $destFull -Recurse -Force
    Write-Output "Installed: $destFull"
    Write-Output "Invoke explicitly with: `$xiaotao-win-flow"
}