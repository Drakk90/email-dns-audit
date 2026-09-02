# =============================================================================
#  run.ps1 — Windows PowerShell Interactive Runner
#  Email DNS Audit Neon v3.3
#  Author: Eduardo Recinos (VCISO)
#  Repository: https://github.com/Drakk90/email-dns-audit
#
#  Interactive Usage (Prompts for language):
#    .\run.ps1
#
#  Direct CLI Usage:
#    .\run.ps1 -DomainsFile servers.txt -DkimMode normal -DeepMonths 30 -Lang es
#    .\run.ps1 -DomainsFile servers.txt -DkimMode deep -DeepMonths 30 -Lang en
# =============================================================================

[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [string]$DomainsFile = "servers.txt",

    [Parameter(Position=1)]
    [string]$DkimMode = "normal",

    [Parameter(Position=2)]
    [int]$DeepMonths = 30,

    [Parameter(Position=3)]
    [string]$Lang = ""
)

$VENV_NAME = "venv-email-audit"
$PY_SCRIPT = "email_dns_audit_neon.py"
$DNSSEC_RESOLVERS = "1.1.1.1,8.8.8.8,9.9.9.9"

# ---------- 0. Interactive Language Prompt ----------
$LangChoice = $Lang
if ([string]::IsNullOrWhiteSpace($LangChoice)) {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║  E M A I L   D N S   A U D I T   N E O N   v 3 . 3            ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "🌐 Seleccione el idioma del reporte y consola / Select Language:" -ForegroundColor Cyan
    Write-Host "   [1] 🇪🇸 Español (Predeterminado / Default)" -ForegroundColor White
    Write-Host "   [2] 🇬🇧 English" -ForegroundColor White
    Write-Host ""
    
    $userInput = Read-Host "👉 Opción / Option [1/2] (Enter = Español)"
    Write-Host ""
    
    if ($userInput -match "^(2|en|english|inglés|ingles)$") {
        $LangChoice = "en"
    } else {
        $LangChoice = "es"
    }
}

# Resolve Interpreter
$VENV_PY = Join-Path (Get-Location) "$VENV_NAME\Scripts\python.exe"
if (Test-Path $VENV_PY) {
    $PYTHON_EXEC = $VENV_PY
} elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
    $PYTHON_EXEC = "python"
} else {
    Write-Host "[ERROR] Python interpreter not found. Please run .\setup.ps1 first." -ForegroundColor Red
    exit 1
}

if ($LangChoice -eq "en") {
    Write-Host "[*] Email DNS Audit Neon v3.3 — Language: English" -ForegroundColor Cyan
} else {
    Write-Host "[*] Email DNS Audit Neon v3.3 — Idioma: Español" -ForegroundColor Cyan
}

# ---------- 1. Verify Dependencies ----------
$depCheck = & $PYTHON_EXEC -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl; print('OK')" 2>$null
if ($depCheck -notmatch "OK") {
    Write-Host "[!] Faltan dependencias / Missing dependencies." -ForegroundColor Yellow
    Write-Host "    Ejecuta / Run: .\setup.ps1" -ForegroundColor Yellow
    exit 1
}

# ---------- 2. Verify Domains File ----------
if (-not (Test-Path $DomainsFile)) {
    Write-Host "[ERROR] No se encontró el archivo de dominios / Domain file not found: $DomainsFile" -ForegroundColor Red
    Write-Host "        Ejemplo: Copy-Item servers.example.txt servers.txt" -ForegroundColor Yellow
    exit 1
}

# ---------- 3. Build DKIM Arguments ----------
$DkimArgs = @()
switch ($DkimMode.ToLower()) {
    { $_ -in @("deep", "profundo") } {
        $DkimArgs = @("--deep-dkim", "--deep-months", "$DeepMonths")
        if ($LangChoice -eq "en") {
            Write-Host "[OK] DKIM Mode: DEEP (~166 selectors, $DeepMonths rotated months)" -ForegroundColor Green
        } else {
            Write-Host "[OK] Modo DKIM: PROFUNDO (~166 selectores, $DeepMonths meses rotativos)" -ForegroundColor Green
        }
    }
    default {
        if ($LangChoice -eq "en") {
            Write-Host "[OK] DKIM Mode: BALANCED (~55 common selectors)" -ForegroundColor Green
        } else {
            Write-Host "[OK] Modo DKIM: BALANCEADO (~55 selectores comunes)" -ForegroundColor Green
        }
    }
}

# ---------- 4. Run Audit ----------
Write-Host "[*] DNSSEC Resolvers: $DNSSEC_RESOLVERS" -ForegroundColor Cyan
if ($LangChoice -eq "en") {
    Write-Host "[*] Running audit (Excel report will be generated in English)..." -ForegroundColor Cyan
} else {
    Write-Host "[*] Ejecutando auditoría (El reporte Excel se generará en Español)..." -ForegroundColor Cyan
}
Write-Host ""

$cmdArgs = @(
    $PY_SCRIPT,
    "--domains", $DomainsFile,
    "--dnssec-resolvers", $DNSSEC_RESOLVERS,
    "--lang", $LangChoice
) + $DkimArgs

& $PYTHON_EXEC @cmdArgs

Write-Host ""
if ($LangChoice -eq "en") {
    Write-Host "Audit finished · Eduardo Recinos (VCISO)" -ForegroundColor Cyan
} else {
    Write-Host "Auditoría finalizada · Eduardo Recinos (VCISO)" -ForegroundColor Cyan
}
