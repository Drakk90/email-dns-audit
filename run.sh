#!/usr/bin/env bash
# =============================================================================
#  run.sh — Ejecutor rapido de Email DNS Audit Neon
#  Autor: Eduardo Recinos
#
#  A DIFERENCIA de setup.sh, este script NO instala nada. Solo:
#    1. Verifica que el entorno virtual exista y tenga las dependencias.
#    2. Ejecuta la auditoria en UNA sola pasada -> UNA sola carpeta de salida.
#
#  DNSSEC:
#    La validacion del bit AD se prueba INTERNAMENTE contra varios resolvers
#    validadores (Cloudflare 1.1.1.1, Google 8.8.8.8, Quad9 9.9.9.9). Si
#    cualquiera confirma la validacion, el dominio se marca como Secure.
#
#  DKIM:
#    Por defecto usa la lista balanceada de ~55 selectores comunes (rapido).
#    Con el modo "deep" agrega ~110 selectores adicionales, incluyendo
#    rotativos por fecha (Google, Amazon SES, SparkPost, Postmark, etc.).
#    Mas lento pero mayor deteccion en dominios grandes.
#
#  Uso:
#    chmod +x run.sh
#    ./run.sh                          # servers.txt · modo DKIM balanceado
#    ./run.sh servers.txt              # archivo indicado · balanceado
#    ./run.sh servers.txt deep         # archivo indicado · DKIM PROFUNDO
#    ./run.sh servers.txt deep 48      # DKIM profundo con 48 meses rotativos
#
#  Argumentos:
#    $1 = archivo de dominios (default: servers.txt)
#    $2 = modo DKIM:  normal (default) | deep
#    $3 = meses rotativos para modo deep (default: 30)
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

# Resolvers validadores para el bit AD de DNSSEC (probados internamente por el
# script Python en una sola pasada). Si cualquiera valida, el dominio es Secure.
DNSSEC_RESOLVERS="1.1.1.1,8.8.8.8,9.9.9.9"

# Python DENTRO del entorno (no requiere activar el venv en la shell)
VENV_PYTHON="./${VENV_NAME}/bin/python"

echo "${CYA}[*]${RST} Email DNS Audit Neon — Ejecutor rapido"

# ---------- 1. Verificar que el entorno exista ----------
if [[ ! -x "$VENV_PYTHON" ]]; then
    echo "${RED}[ERROR]${RST} No existe el entorno '${VENV_NAME}'."
    echo "        Ejecuta el instalador UNA vez:  ${BLD}./setup.sh${RST}"
    exit 1
fi

# ---------- 2. Verificar dependencias (sin instalar) ----------
if ! "$VENV_PYTHON" -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl" 2>/dev/null; then
    echo "${YEL}[!]${RST} Faltan dependencias en el entorno."
    echo "     Corre el instalador UNA sola vez:  ${BLD}./setup.sh${RST}"
    echo "     O instala directamente dentro del entorno:"
    echo "        ${BLD}${VENV_PYTHON} -m pip install -r requirements.txt${RST}"
    exit 1
fi

# ---------- 3. Verificar archivo de dominios ----------
if [[ ! -f "$DOMAINS_FILE" ]]; then
    echo "${RED}[ERROR]${RST} No se encontro el archivo de dominios: ${DOMAINS_FILE}"
    echo "        Crea tu lista:  ${BLD}cp servers.example.txt servers.txt && nano servers.txt${RST}"
    exit 1
fi

# ---------- 4. Construir argumentos DKIM segun el modo ----------
DKIM_ARGS=()
case "$DKIM_MODE" in
    deep|DEEP|profundo)
        DKIM_ARGS=(--deep-dkim --deep-months "$DEEP_MONTHS")
        echo "${GRN}[OK]${RST} Modo DKIM: ${BLD}PROFUNDO${RST} (~166 selectores, ${DEEP_MONTHS} meses rotativos)"
        echo "     ${YEL}Nota:${RST} este modo es mas lento pero detecta selectores custom/rotativos."
        ;;
    normal|NORMAL|"")
        echo "${GRN}[OK]${RST} Modo DKIM: ${BLD}BALANCEADO${RST} (~55 selectores comunes)"
        echo "     Para deteccion profunda usa:  ${BLD}./run.sh ${DOMAINS_FILE} deep${RST}"
        ;;
    *)
        echo "${YEL}[!]${RST} Modo DKIM '${DKIM_MODE}' no reconocido; usando BALANCEADO por defecto."
        echo "     Opciones validas: normal | deep"
        ;;
esac

# ---------- 5. Ejecutar la auditoria (una sola pasada, una sola carpeta) ----------
echo "${CYA}[*]${RST} DNSSEC se validara contra: ${DNSSEC_RESOLVERS}"
echo "${CYA}[*]${RST} Ejecutando auditoria (salida unica)..."
echo
"$VENV_PYTHON" "$PY_SCRIPT" \
    --domains "$DOMAINS_FILE" \
    --dnssec-resolvers "$DNSSEC_RESOLVERS" \
    "${DKIM_ARGS[@]}"

echo
echo "${BLD}${CYA}Auditoria finalizada · Eduardo Recinos${RST}"
