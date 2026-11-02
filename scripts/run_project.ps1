
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$Python = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $Python)) {
    Write-Host "Virtual environment not found."
    Write-Host "Run .\scripts\setup_environment.ps1 first."
    exit 1
}

if (-not (Test-Path "assets\brain_tumor_ar.glb")) {
    Write-Host "Brain model not found in assets folder."
    exit 1
}

Write-Host "Starting Brain Registration viewer..."

$ViewerCommand = "Set-Location '$ProjectRoot'; & '$Python' 'src\view_brain.py'"

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command", $ViewerCommand
)

Start-Sleep -Seconds 3

Write-Host "Starting AprilTag pose tracking..."
Write-Host "Press Q in the camera window to stop tracking."

& $Python "src\pose_estimation.py"
