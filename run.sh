#!/usr/bin/env bash
# =============================================================================
#  run.sh — Ejecutor interactivo de Email DNS Audit Neon v3.3
#  Autor: Eduardo Recinos (VCISO)
#
#  Uso interactivo (Pregunta idioma y modo):
#    ./run.sh
#
#  Uso directo / Scripting:
#    ./run.sh servers.txt normal 30 es   # Lista en Español
#    ./run.sh servers.txt normal 30 en   # Lista en English
#    ./run.sh google.com normal 30 en    # Dominio individual en English
# =============================================================================

set -uo pipefail

if [[ -t 1 ]]; then
    RED=$'\e[31m'; GRN=$'\e[32m'; YEL=$'\e[33m'; CYA=$'\e[36m'; MAG=$'\e[35m'; BLD=$'\e[1m'; RST=$'\e[0m'
else
    RED=""; GRN=""; YEL=""; CYA=""; MAG=""; BLD=""; RST=""
fi

VENV_NAME="venv-email-audit"
PY_SCRIPT="email_dns_audit_neon.py"
FIRST_ARG="${1:-}"
DKIM_MODE="${2:-normal}"
DEEP_MONTHS="${3:-30}"
LANG_ARG="${4:-}"

# ---------- 0. Selección interactiva de idioma y objetivo ----------
IS_INTERACTIVE=0
if [[ -z "$FIRST_ARG" && -z "$LANG_ARG" ]]; then
    IS_INTERACTIVE=1
fi

if [[ -z "$LANG_ARG" ]]; then
    echo
    echo "${MAG}${BLD}╔══════════════════════════════════════════════════════════════╗${RST}"
    echo "${MAG}${BLD}║${RST}  ${CYA}${BLD}E M A I L   D N S   A U D I T   N E O N   v 3 . 3${RST}           ${MAG}${BLD}║${RST}"
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

# Selección de objetivo (Archivo de lista vs Dominio único)
TARGET_FLAG=""
TARGET_VALUE=""

if [[ "$IS_INTERACTIVE" -eq 1 ]]; then
    if [[ "$LANG_CHOICE" == "en" ]]; then
        echo "${CYA}🎯 Select Audit Target:${RST}"
        echo "   ${BLD}[1]${RST} 📋 Batch audit from domain list file (servers.txt)"
        echo "   ${BLD}[2]${RST} 🎯 Single domain audit (e.g. example.com)"
        echo
        read -r -p "👉 Option [1/2] (Enter = servers.txt): " TARGET_MODE_INPUT
    else
        echo "${CYA}🎯 Seleccione el objetivo de la auditoría:${RST}"
        echo "   ${BLD}[1]${RST} 📋 Auditar lista de dominios desde archivo (servers.txt)"
        echo "   ${BLD}[2]${RST} 🎯 Auditar un solo dominio directamente (ej: miempresa.com)"
        echo
        read -r -p "👉 Opción [1/2] (Enter = servers.txt): " TARGET_MODE_INPUT
    fi
    echo

    if [[ "$TARGET_MODE_INPUT" == "2" ]]; then
        if [[ "$LANG_CHOICE" == "en" ]]; then
            read -r -p "👉 Enter target domain (e.g. google.com): " TARGET_DOMAIN_INPUT
        else
            read -r -p "👉 Ingrese el dominio a auditar (ej: google.com): " TARGET_DOMAIN_INPUT
        fi
        echo
        TARGET_FLAG="--domain"
        TARGET_VALUE="${TARGET_DOMAIN_INPUT:-google.com}"
    else
        TARGET_FLAG="--domains"
        TARGET_VALUE="servers.txt"
    fi
else
    if [[ -f "$FIRST_ARG" ]]; then
        TARGET_FLAG="--domains"
        TARGET_VALUE="$FIRST_ARG"
    elif [[ -n "$FIRST_ARG" ]]; then
        TARGET_FLAG="--domain"
        TARGET_VALUE="$FIRST_ARG"
    else
        TARGET_FLAG="--domains"
        TARGET_VALUE="servers.txt"
    fi
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
    echo "     Ejecuta / Run: ${BLD}./setup.sh${RST}"
    exit 1
fi

# ---------- 2. Verificar objetivo ----------
if [[ "$TARGET_FLAG" == "--domains" && ! -f "$TARGET_VALUE" ]]; then
    if [[ -f "servers.example.txt" ]]; then
        cp servers.example.txt servers.txt
        echo "${GRN}[OK]${RST} servers.txt creado a partir de servers.example.txt"
    else
        echo "${RED}[ERROR]${RST} No se encontró el archivo de dominios / Domain file not found: ${TARGET_VALUE}"
        exit 1
    fi
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
    echo "${CYA}[*]${RST} Running audit (Target: ${TARGET_FLAG} ${TARGET_VALUE})..."
else
    echo "${CYA}[*]${RST} Ejecutando auditoría (Objetivo: ${TARGET_FLAG} ${TARGET_VALUE})..."
fi
echo

"$VENV_PYTHON" "$PY_SCRIPT" \
    "$TARGET_FLAG" "$TARGET_VALUE" \
    --dnssec-resolvers "$DNSSEC_RESOLVERS" \
    --lang "$LANG_CHOICE" \
    "${DKIM_ARGS[@]}"

echo
if [[ "$LANG_CHOICE" == "en" ]]; then
    echo "${BLD}${CYA}Audit finished · Eduardo Recinos (VCISO)${RST}"
else
    echo "${BLD}${CYA}Auditoría finalizada · Eduardo Recinos (VCISO)${RST}"
fi

# ---------- 5. Apertura de reporte Excel ----------
LATEST_EXCEL="$(find . -maxdepth 2 -type f -name "*.xlsx" -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -n 1 | awk '{print $2}')"
if [[ -n "$LATEST_EXCEL" && "$IS_INTERACTIVE" -eq 1 ]]; then
    echo
    if [[ "$LANG_CHOICE" == "en" ]]; then
        read -r -p "📊 Would you like to open the Excel report now? [y/N]: " OPEN_REPORT
    else
        read -r -p "📊 ¿Desea abrir el reporte Excel ahora? [s/N]: " OPEN_REPORT
    fi
    if [[ "$OPEN_REPORT" =~ ^[sSyY]$ ]]; then
        if command -v xdg-open &>/dev/null; then
            xdg-open "$LATEST_EXCEL" 2>/dev/null &
        elif command -v open &>/dev/null; then
            open "$LATEST_EXCEL" 2>/dev/null &
        fi
    fi
fi
