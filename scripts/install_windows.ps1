
$ErrorActionPreference = "Stop"

Write-Host "====================================="
Write-Host " Brain Registration - Windows Setup"
Write-Host "====================================="

# Install Python 3.12 if it is not available
try {
    py -3.12 --version
    Write-Host "Python 3.12 is already installed."
}
catch {
    Write-Host "Installing Python 3.12..."
    winget install --id Python.Python.3.12 -e --source winget
}

# Install Git if it is not available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Git..."
    winget install --id Git.Git -e --source winget
}

Write-Host ""
Write-Host "Installation check complete."
Write-Host "Close and reopen PowerShell if commands are not recognized."
Write-Host "Next run: .\scripts\setup_environment.ps1"
