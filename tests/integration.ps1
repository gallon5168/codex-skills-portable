$ErrorActionPreference='Stop'
$Repo=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$TempRoot=[IO.Path]::GetFullPath([IO.Path]::GetTempPath())
$Tmp=[IO.Path]::GetFullPath((Join-Path $TempRoot ('csp-portable-test-'+$PID)))
if(-not $Tmp.StartsWith($TempRoot) -or (Split-Path -Leaf $Tmp) -notmatch '^csp-portable-test-[0-9]+$'){throw "Unexpected test path: $Tmp"}
New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
$aliasesForTest=Get-Content -LiteralPath (Join-Path $Repo 'manifest\aliases.json') -Raw -Encoding UTF8|ConvertFrom-Json
$alias=($aliasesForTest|Where-Object {$_.alias.Length -lt 40}|Select-Object -First 1).alias
$conflict=Join-Path $Tmp ('.agents\skills\'+$alias)
New-Item -ItemType Directory -Force -Path $conflict | Out-Null
'before-install' | Set-Content -LiteralPath (Join-Path $conflict 'sentinel.txt') -Encoding UTF8
$install=& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Repo 'install.ps1') -HomePath $Tmp -CodexHome (Join-Path $Tmp '.codex') -Force
if($LASTEXITCODE -ne 0){throw "installer failed: $install"}
$during=(Get-Item -LiteralPath $conflict -Force).Attributes -band [IO.FileAttributes]::ReparsePoint
if(-not $during){throw 'expected junction after install'}
$rollback=& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $Repo 'rollback.ps1') -HomePath $Tmp
if($LASTEXITCODE -ne 0){throw "rollback failed: $rollback"}
$sentinel=(Get-Content -LiteralPath (Join-Path $conflict 'sentinel.txt') -Raw -Encoding UTF8).Trim()
$installRoot=Join-Path $Tmp '.codex\skills\.portable-export'
if($sentinel -ne 'before-install' -or (Test-Path -LiteralPath $installRoot)){throw 'rollback state mismatch'}
$installNormalized=([string]$install).Replace($Tmp,'${TEST_HOME}')
$rollbackNormalized=([string]$rollback).Replace($Tmp,'${TEST_HOME}')
$result="$installNormalized`n$rollbackNormalized`nROLLBACK VERIFY PASS sentinel=$sentinel installRootExists=$(Test-Path -LiteralPath $installRoot)"
Remove-Item -LiteralPath $Tmp -Recurse -Force
$result
