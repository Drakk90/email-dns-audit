#!/usr/bin/env bash
# =============================================================================
#  run.sh — Ejecutor rápido de Email DNS Audit Neon v3.3
#  Autor: Eduardo Recinos (VCISO)
#
#  Uso / Usage:
#    chmod +x run.sh
#    ./run.sh                          # servers.txt · normal · 30 · es
#    ./run.sh servers.txt normal 30 en # servers.txt en Inglés
#    ./run.sh servers.txt deep 30 es   # servers.txt · modo DKIM profundo · Español
#
#  Argumentos / Arguments:
#    $1 = archivo de dominios / domains file (default: servers.txt)
#    $2 = modo DKIM / dkim mode: normal (default) | deep
#    $3 = meses rotativos / deep months (default: 30)
#    $4 = idioma / language: es (default) | en
# =============================================================================

set -uo pipefail

if [[ -t 1 ]]; then
    RED=$'\e[31m'; GRN=$'\e[32m'; YEL=$'\e[33m'; CYA=$'\e[36m'; BLD=$'\e[1m'; RST=$'\e[0m'
else
    RED=""; GRN=""; YEL=""; CYA=""; BLD=""; RST=""
fi

VENV_NAME="venv-email-audit"
PY_SCRIPT="email_dns_audit_neon.py"
DOMAINS_FILE="${1:-servers.txt}"
DKIM_MODE="${2:-normal}"
DEEP_MONTHS="${3:-30}"
LANG_CHOICE="${4:-es}"

# Resolvers validadores para DNSSEC
DNSSEC_RESOLVERS="1.1.1.1,8.8.8.8,9.9.9.9"

# Python dentro del entorno virtual si existe, o fallback a python3 del sistema
if [[ -x "./${VENV_NAME}/bin/python" ]]; then
    VENV_PYTHON="./${VENV_NAME}/bin/python"
else
    VENV_PYTHON="python3"
fi

if [[ "$LANG_CHOICE" == "en" ]]; then
    echo "${CYA}[*]${RST} Email DNS Audit Neon v3.3 — Fast Runner (Language: English)"
else
    echo "${CYA}[*]${RST} Email DNS Audit Neon v3.3 — Ejecutor Rápido (Idioma: Español)"
fi

# ---------- 1. Verificar dependencias ----------
if ! "$VENV_PYTHON" -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl" 2>/dev/null; then
    echo "${YEL}[!]${RST} Faltan dependencias / Missing dependencies."
    echo "     Ejecuta / Run: ${BLD}pip install -r requirements.txt${RST}"
    exit 1
fi

# ---------- 2. Verificar archivo de dominios ----------
if [[ ! -f "$DOMAINS_FILE" ]]; then
    echo "${RED}[ERROR]${RST} No se encontró el archivo de dominios / Domain file not found: ${DOMAINS_FILE}"
    echo "        Ejemplo:  ${BLD}cp servers.example.txt servers.txt && nano servers.txt${RST}"
    exit 1
fi

# ---------- 3. Construir argumentos DKIM ----------
DKIM_ARGS=()
case "$DKIM_MODE" in
    deep|DEEP|profundo)
        DKIM_ARGS=(--deep-dkim --deep-months "$DEEP_MONTHS")
        if [[ "$LANG_CHOICE" == "en" ]]; then
            echo "${GRN}[OK]${RST} DKIM Mode: ${BLD}DEEP${RST} (~166 selectors, ${DEEP_MONTHS} rotated months)"
        else
            echo "${GRN}[OK]${RST} Modo DKIM: ${BLD}PROFUNDO${RST} (~166 selectores, ${DEEP_MONTHS} meses rotativos)"
        fi
        ;;
    normal|NORMAL|"")
        if [[ "$LANG_CHOICE" == "en" ]]; then
            echo "${GRN}[OK]${RST} DKIM Mode: ${BLD}BALANCED${RST} (~55 common selectors)"
        else
            echo "${GRN}[OK]${RST} Modo DKIM: ${BLD}BALANCEADO${RST} (~55 selectores comunes)"
        fi
        ;;
    *)
        echo "${YEL}[!]${RST} Modo DKIM '${DKIM_MODE}' desconocido; usando BALANCEADO."
        ;;
esac

# ---------- 4. Ejecutar la auditoría ----------
echo "${CYA}[*]${RST} DNSSEC resolvers: ${DNSSEC_RESOLVERS}"
echo "${CYA}[*]${RST} Ejecutando auditoría / Executing audit..."
echo

"$VENV_PYTHON" "$PY_SCRIPT" \
    --domains "$DOMAINS_FILE" \
    --dnssec-resolvers "$DNSSEC_RESOLVERS" \
    --lang "$LANG_CHOICE" \
    "${DKIM_ARGS[@]}"

echo
if [[ "$LANG_CHOICE" == "en" ]]; then
    echo "${BLD}${CYA}Audit finished · Eduardo Recinos (VCISO)${RST}"
else
    echo "${BLD}${CYA}Auditoría finalizada · Eduardo Recinos (VCISO)${RST}"
fi
