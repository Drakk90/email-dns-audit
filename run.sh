#!/usr/bin/env bash
# =============================================================================
#  run.sh — Ejecutor interactivo de Email DNS Audit Neon v3.3
#  Autor: Eduardo Recinos (VCISO)
#
#  Uso interactivo (Pregunta idioma y genera Excel en ese idioma):
#    ./run.sh
#
#  Uso directo / Scripting:
#    ./run.sh servers.txt normal 30 es   # Español
#    ./run.sh servers.txt normal 30 en   # English
#    ./run.sh servers.txt deep 30 en     # Deep DKIM en English
# =============================================================================

set -uo pipefail

if [[ -t 1 ]]; then
    RED=$'\e[31m'; GRN=$'\e[32m'; YEL=$'\e[33m'; CYA=$'\e[36m'; MAG=$'\e[35m'; BLD=$'\e[1m'; RST=$'\e[0m'
else
    RED=""; GRN=""; YEL=""; CYA=""; MAG=""; BLD=""; RST=""
fi

VENV_NAME="venv-email-audit"
PY_SCRIPT="email_dns_audit_neon.py"
DOMAINS_FILE="${1:-servers.txt}"
DKIM_MODE="${2:-normal}"
DEEP_MONTHS="${3:-30}"
LANG_ARG="${4:-}"

# ---------- 0. Selección interactiva de idioma ----------
if [[ -z "$LANG_ARG" ]]; then
    echo
    echo "${MAG}${BLD}╔══════════════════════════════════════════════════════════════╗${RST}"
    echo "${MAG}${BLD}║${RST}  ${CYA}${BLD}E M A I L   D N S   A U D I T   N E O N   v 3 . 3${RST}            ${MAG}${BLD}║${RST}"
    echo "${MAG}${BLD}╚══════════════════════════════════════════════════════════════╝${RST}"
    echo
    echo "${CYA}🌐 Seleccione el idioma del reporte y consola / Select Language:${RST}"
    echo "   ${BLD}[1]${RST} 🇪🇸 Español (Predeterminado / Default)"
    echo "   ${BLD}[2]${RST} 🇬🇧 English"
    echo
    if [[ -t 0 ]]; then
        read -r -p "👉 Opción / Option [1/2] (Enter = Español): " USER_LANG_INPUT
    elif [ -c /dev/tty ]; then
        read -r -p "👉 Opción / Option [1/2] (Enter = Español): " USER_LANG_INPUT < /dev/tty 2>/dev/null || read -r USER_LANG_INPUT 2>/dev/null || USER_LANG_INPUT=""
    else
        read -r USER_LANG_INPUT 2>/dev/null || USER_LANG_INPUT=""
    fi
    echo

    case "${USER_LANG_INPUT,,}" in
        2|en|english|inglés|ingles)
            LANG_CHOICE="en"
            ;;
        *)
            LANG_CHOICE="es"
            ;;
    esac
else
    LANG_CHOICE="${LANG_ARG:-es}"
fi

# Resolvers validadores para DNSSEC
DNSSEC_RESOLVERS="1.1.1.1,8.8.8.8,9.9.9.9"

# Python dentro del entorno virtual si existe, o fallback a python3 del sistema
if [[ -x "./${VENV_NAME}/bin/python" ]]; then
    VENV_PYTHON="./${VENV_NAME}/bin/python"
else
    VENV_PYTHON="python3"
fi

if [[ "$LANG_CHOICE" == "en" ]]; then
    echo "${CYA}[*]${RST} Email DNS Audit Neon v3.3 — Language: ${BLD}English${RST}"
else
    echo "${CYA}[*]${RST} Email DNS Audit Neon v3.3 — Idioma: ${BLD}Español${RST}"
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
if [[ "$LANG_CHOICE" == "en" ]]; then
    echo "${CYA}[*]${RST} Running audit (Excel report will be generated in English)..."
else
    echo "${CYA}[*]${RST} Ejecutando auditoría (El reporte Excel se generará en Español)..."
fi
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
