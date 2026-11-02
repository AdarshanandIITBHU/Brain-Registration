
$ErrorActionPreference = "Stop"

# Always run from the repository root
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "Checking Python 3.12..."

py -3.12 --version

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    py -3.12 -m venv .venv
}

Write-Host "Activating virtual environment..."
& ".\.venv\Scripts\Activate.ps1"

Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

Write-Host "Installing project dependencies..."
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Environment setup complete!"
Write-Host "Activate later using: .\.venv\Scripts\Activate.ps1"
