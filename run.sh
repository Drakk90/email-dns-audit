#!/usr/bin/env bash
# =============================================================================
#  run.sh — Ejecutor rapido de Email DNS Audit Neon
#  Autor: Eduardo Recinos
#
#  A DIFERENCIA de setup.sh, este script NO instala nada. Solo:
#    1. Verifica que el entorno virtual exista y tenga las dependencias.
#    2. Ejecuta la auditoria usando el Python del entorno directamente.
#
#  Si faltan dependencias, te avisa para que corras setup.sh UNA sola vez.
#
#  Uso:
#    chmod +x run.sh
#    ./run.sh                        # usa servers.txt por defecto
#    ./run.sh mis_dominios.txt       # usa otro archivo de dominios
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

# ---------- 4. Ejecutar la auditoria ----------
echo "${GRN}[OK]${RST} Entorno y dependencias listos. Ejecutando auditoria..."
echo
"$VENV_PYTHON" "$PY_SCRIPT" --domains "$DOMAINS_FILE"
