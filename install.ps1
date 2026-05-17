# Installs cie-econ-essay and cie-econ-ppt into ~/.claude/skills/
# and installs Python dependencies for cie-econ-ppt.
#
# Usage:   ./install.ps1
# Run from the root of the cloned A-Level-Econ-Marking-Sample repo.

$ErrorActionPreference = "Stop"

$repoRoot = $PSScriptRoot
$skillsDir = Join-Path $env:USERPROFILE ".claude\skills"

Write-Host ""
Write-Host "Installing CIE Economics skills" -ForegroundColor Cyan
Write-Host "  Source: $repoRoot"
Write-Host "  Target: $skillsDir"
Write-Host ""

New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null

foreach ($skill in @("cie-econ-essay", "cie-econ-ppt")) {
    $src = Join-Path $repoRoot $skill
    $dst = Join-Path $skillsDir $skill
    if (-not (Test-Path $src)) {
        Write-Host "[skip] $skill not found in repo at $src" -ForegroundColor Yellow
        continue
    }
    if (Test-Path $dst) {
        Write-Host "[update] $skill (replacing existing install)" -ForegroundColor Yellow
        Remove-Item -Recurse -Force $dst
    } else {
        Write-Host "[install] $skill" -ForegroundColor Green
    }
    Copy-Item -Recurse -Path $src -Destination $dst
}

Write-Host ""
Write-Host "Installing Python dependencies for cie-econ-ppt..." -ForegroundColor Cyan

# Find a real Python (skip the Windows Store shim)
$python = $null
$candidates = @(
    (Get-Command python.exe -ErrorAction SilentlyContinue | Where-Object { $_.Source -notlike "*WindowsApps*" } | Select-Object -First 1 -ExpandProperty Source),
    (Get-Command python3.exe -ErrorAction SilentlyContinue | Where-Object { $_.Source -notlike "*WindowsApps*" } | Select-Object -First 1 -ExpandProperty Source),
    (Get-ChildItem "$env:LOCALAPPDATA\Programs\Python" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName),
    (Get-ChildItem "C:\Program Files\Python*" -Filter "python.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName)
)
foreach ($c in $candidates) { if ($c -and (Test-Path $c)) { $python = $c; break } }

if (-not $python) {
    Write-Host ""
    Write-Host "  No real Python install found." -ForegroundColor Yellow
    Write-Host "  Install Python 3.12 first, then re-run this script:" -ForegroundColor Yellow
    Write-Host "      winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  The cie-econ-essay skill will still work without Python."
    exit 0
}

Write-Host "  Using Python: $python"
& $python -m pip install --quiet --user python-pptx matplotlib pypdf scipy
if ($LASTEXITCODE -ne 0) {
    Write-Host "  pip install failed. cie-econ-ppt may not work until you install:" -ForegroundColor Red
    Write-Host "      $python -m pip install --user python-pptx matplotlib pypdf scipy" -ForegroundColor Gray
    exit 1
}

# Smoke-test the diagram library
Write-Host "  Verifying diagram library..."
$diagrams = Join-Path $skillsDir "cie-econ-ppt\scripts\diagrams.py"
& $python -c "import sys; sys.path.insert(0, r'$($skillsDir)\cie-econ-ppt\scripts'); import diagrams; print('  OK -', len(diagrams.REGISTRY), 'diagrams available')"

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host ""
Write-Host "Restart Claude Code, then try:"
Write-Host "    cie: write a 12-mark sample answer on PED" -ForegroundColor Cyan
Write-Host "    cie ppt: A-Level Topic 2.1 Demand and supply" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: cie-econ-ppt will need to know your Python path. It's at:"
Write-Host "    $python" -ForegroundColor Gray
