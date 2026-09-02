# =============================================================================
#  setup.ps1 — Windows PowerShell Automated Installer
#  Email DNS Audit Neon v3.3
#  Author: Eduardo Recinos (VCISO)
#  Repository: https://github.com/Drakk90/email-dns-audit
# =============================================================================

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

function Write-Info($msg)  { Write-Host "[*] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)    { Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Warn($msg)  { Write-Host "[!] $msg" -ForegroundColor Yellow }
function Write-Err($msg)   { Write-Host "[ERROR] $msg" -ForegroundColor Red }

Clear-Host
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Blue
Write-Host "  EMAIL DNS AUDIT NEON — Windows PowerShell Installer" -ForegroundColor Cyan
Write-Host "  Author: Eduardo Recinos (VCISO)" -ForegroundColor Blue
Write-Host "=====================================================================" -ForegroundColor Blue
Write-Host ""

$VENV_NAME = "venv-email-audit"
$PY_SCRIPT = "email_dns_audit_neon.py"

# ---------- 1. Detect Python 3.10+ ----------
Write-Info "Step 1/6: Checking Python installation..."

$PYTHON_CMD = $null
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    $PYTHON_CMD = "python"
} elseif (Get-Command "py" -ErrorAction SilentlyContinue) {
    $PYTHON_CMD = "py"
}

if (-not $PYTHON_CMD) {
    Write-Err "Python 3 is not installed or not in PATH."
    Write-Err "Please download and install Python 3.10+ from https://www.python.org/downloads/ (check 'Add python.exe to PATH')."
    exit 1
}

$pyVersionRaw = & $PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$pyMajor = [int]($pyVersionRaw.Split('.')[0])
$pyMinor = [int]($pyVersionRaw.Split('.')[1])

if ($pyMajor -lt 3 -or ($pyMajor -eq 3 -and $pyMinor -lt 10)) {
    Write-Err "Python 3.10 or higher is required. Detected version: $pyVersionRaw"
    exit 1
}
Write-Ok "Python $pyVersionRaw detected ($PYTHON_CMD)"

# ---------- 2. Check Project Files ----------
Write-Info "Step 2/6: Verifying project files..."
if (-not (Test-Path "requirements.txt")) {
    Write-Err "'requirements.txt' not found. Please run this script from the project root directory."
    exit 1
}
Write-Ok "requirements.txt found"

if (Test-Path $PY_SCRIPT) {
    Write-Ok "$PY_SCRIPT found"
} else {
    Write-Warn "$PY_SCRIPT not found in current folder."
}

# ---------- 3. Create Virtual Environment ----------
Write-Info "Step 3/6: Initializing virtual environment '$VENV_NAME'..."

if (Test-Path $VENV_NAME) {
    Write-Warn "Virtual environment '$VENV_NAME' already exists."
    $recreate = Read-Host "Do you want to recreate it from scratch? [y/N]"
    if ($recreate -match "^[yY]$") {
        Remove-Item -Recurse -Force $VENV_NAME
        & $PYTHON_CMD -m venv $VENV_NAME
        Write-Ok "Virtual environment recreated"
    } else {
        Write-Info "Using existing virtual environment"
    }
} else {
    & $PYTHON_CMD -m venv $VENV_NAME
    Write-Ok "Virtual environment '$VENV_NAME' created"
}

# ---------- 4. Bootstrap Pip & Install Dependencies ----------
Write-Info "Step 4/6: Installing Python dependencies..."

$VENV_PY = Join-Path (Get-Location) "$VENV_NAME\Scripts\python.exe"

if (-not (Test-Path $VENV_PY)) {
    Write-Err "Virtual environment Python interpreter not found at: $VENV_PY"
    exit 1
}

& $VENV_PY -m pip install --upgrade pip --quiet
& $VENV_PY -m pip install -r requirements.txt --quiet
Write-Ok "Dependencies installed successfully"

# ---------- 5. Validate Imports ----------
Write-Info "Step 5/6: Validating environment imports..."
$importCheck = & $VENV_PY -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl; print('OK')" 2>$null
if ($importCheck -match "OK") {
    Write-Ok "All dependencies imported successfully"
} else {
    Write-Err "Failed to verify module imports. Please run: & '$VENV_PY' -m pip install -r requirements.txt"
    exit 1
}

# ---------- 6. Prepare servers.txt ----------
Write-Info "Step 6/6: Preparing target domains list..."
if (Test-Path "servers.txt") {
    Write-Ok "servers.txt already exists"
} elseif (Test-Path "servers.example.txt") {
    Copy-Item "servers.example.txt" "servers.txt"
    Write-Ok "servers.txt created from servers.example.txt"
    Write-Warn "Please edit servers.txt with your real domains before running the audit:"
    Write-Host "     notepad servers.txt" -ForegroundColor White
} else {
    Write-Warn "servers.example.txt not found. Please create servers.txt manually."
}

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "  INSTALLATION COMPLETED SUCCESSFULLY" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "To execute the audit on Windows:" -ForegroundColor White
Write-Host ""
Write-Host "  # Interactive Runner (Recommended):" -ForegroundColor Cyan
Write-Host "  .\run.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "  # Or Direct Python Execution:" -ForegroundColor Cyan
Write-Host "  .\$VENV_NAME\Scripts\python.exe $PY_SCRIPT --domains servers.txt --lang es" -ForegroundColor Yellow
Write-Host ""
Write-Host "Audit Ready · Eduardo Recinos (VCISO)" -ForegroundColor Cyan
Write-Host ""
