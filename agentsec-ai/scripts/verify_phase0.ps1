<#
Phase 0 verification script.
Run this from the repository root in PowerShell.
#>

Write-Host "Phase 0 verification: setting up venv and running tests"

if (-Not (Test-Path -Path .venv)) {
    python -m venv .venv
}

Write-Host "Activating venv"
. .\.venv\Scripts\Activate.ps1

Write-Host "Installing requirements"
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Running pytest"
python -m pytest -q

Write-Host "Phase 0 verification complete"
