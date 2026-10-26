param(
    [string]$Destination = "$env:USERPROFILE\.codex\skills\omni-flow"
)

$ErrorActionPreference = "Stop"
$source = (Resolve-Path (Join-Path $PSScriptRoot ".."))
if (-not (Test-Path -LiteralPath $Destination)) {
    throw "Destination skill directory does not exist: $Destination"
}

python (Join-Path $PSScriptRoot "verify_install.py") $source $Destination
if ($LASTEXITCODE -eq 0) {
    Write-Output "Already synchronized: $Destination"
    exit 0
}

Copy-Item -Path (Join-Path $source "*") -Destination $Destination -Recurse -Force
python (Join-Path $PSScriptRoot "verify_install.py") $source $Destination
if ($LASTEXITCODE -ne 0) {
    throw "Installation verification failed after copy"
}
Write-Output "Installed verified omni-flow skill to $Destination"
