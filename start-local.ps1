param([int]$Port = 8000)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$projectPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) {
    $projectPython = Join-Path (Split-Path $PSScriptRoot -Parent) 'luntiai-test-env\Scripts\python.exe'
}
if (-not (Test-Path -LiteralPath $projectPython)) {
    throw 'Create .venv with Python 3.11 and install requirements-notebook.txt first. See README.md.'
}
$env:LUNTIAI_DEMO_MODE = 'true'
Write-Host "Open http://127.0.0.1:$Port/app/ after the server starts. Ctrl+C stops it."
& $projectPython -m uvicorn api.main:app --host 127.0.0.1 --port $Port
