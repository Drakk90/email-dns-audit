#!/usr/bin/env bash
# =============================================================================
#  setup.sh — Instalador automatico de Email DNS Audit Neon
#  Autor: Eduardo Recinos
#  Compatibilidad: Kali Linux, Ubuntu 20.04+, Debian 10+, CachyOS/Arch
#
#  Este script:
#    1. Verifica que Python 3.9+ este instalado (y lo instala si falta)
#    2. Crea el entorno virtual "venv-email-audit"
#    3. Instala las dependencias de requirements.txt
#    4. Valida la instalacion
#    5. Prepara servers.txt a partir de servers.example.txt
#
#  Uso:
#    chmod +x setup.sh
#    ./setup.sh
# =============================================================================

set -uo pipefail

# ---------- Colores para la salida ----------
if [[ -t 1 ]]; then
    RED=$'\e[31m'; GRN=$'\e[32m'; YEL=$'\e[33m'
    BLU=$'\e[34m'; CYA=$'\e[36m'; BLD=$'\e[1m'; RST=$'\e[0m'
else
    RED=""; GRN=""; YEL=""; BLU=""; CYA=""; BLD=""; RST=""
fi

VENV_NAME="venv-email-audit"
PY_SCRIPT="email_dns_audit_neon.py"

# ---------- Funciones auxiliares ----------
info()  { echo "${CYA}[*]${RST} $*"; }
ok()    { echo "${GRN}[OK]${RST} $*"; }
warn()  { echo "${YEL}[!]${RST} $*"; }
error() { echo "${RED}[ERROR]${RST} $*"; }
hr()    { printf '%*s\n' 70 '' | tr ' ' '-'; }

banner() {
    echo
    echo "${BLD}${BLU}=====================================================================${RST}"
    echo "${BLD}${CYA}  EMAIL DNS AUDIT NEON — Instalador Automatico${RST}"
    echo "${BLD}${BLU}  Autor: Eduardo Recinos${RST}"
    echo "${BLD}${BLU}=====================================================================${RST}"
    echo
}

# ---------- Detectar gestor de paquetes ----------
detect_pkg_manager() {
    if command -v apt &>/dev/null; then
        echo "apt"
    elif command -v pacman &>/dev/null; then
        echo "pacman"
    elif command -v dnf &>/dev/null; then
        echo "dnf"
    else
        echo "unknown"
    fi
}

# ---------- Detectar shell del usuario ----------
detect_shell() {
    local sh
    sh="$(basename "${SHELL:-}")"
    echo "$sh"
}

# =============================================================================
#  INICIO
# =============================================================================
banner

# ---------- Paso 1: Verificar Python ----------
info "Paso 1/5: Verificando Python 3..."

PYTHON_BIN=""
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
fi

if [[ -z "$PYTHON_BIN" ]]; then
    warn "Python 3 no esta instalado. Intentando instalar..."
    PKG="$(detect_pkg_manager)"
    case "$PKG" in
        apt)
            sudo apt update && sudo apt install -y python3 python3-pip python3-venv
            ;;
        pacman)
            sudo pacman -S --needed --noconfirm python python-pip
            ;;
        dnf)
            sudo dnf install -y python3 python3-pip
            ;;
        *)
            error "No se pudo detectar el gestor de paquetes. Instala Python 3.9+ manualmente."
            exit 1
            ;;
    esac
    PYTHON_BIN="python3"
fi

# Verificar version minima (3.9)
PY_VERSION="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
PY_MAJOR="$(echo "$PY_VERSION" | cut -d. -f1)"
PY_MINOR="$(echo "$PY_VERSION" | cut -d. -f2)"

if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 9 ]]; }; then
    error "Se requiere Python 3.9 o superior. Version detectada: $PY_VERSION"
    error "Actualiza tu sistema con: sudo apt upgrade"
    exit 1
fi

ok "Python $PY_VERSION detectado ($PYTHON_BIN)"

# Verificar que el modulo venv este disponible
if ! "$PYTHON_BIN" -m venv --help &>/dev/null; then
    warn "El modulo venv no esta disponible. Instalando..."
    PKG="$(detect_pkg_manager)"
    case "$PKG" in
        apt) sudo apt install -y python3-venv ;;
        *)   warn "Instala el paquete venv manualmente para tu distribucion." ;;
    esac
fi

hr

# ---------- Paso 2: Verificar archivos del proyecto ----------
info "Paso 2/5: Verificando archivos del proyecto..."

if [[ ! -f "requirements.txt" ]]; then
    error "No se encontro 'requirements.txt' en el directorio actual."
    error "Ejecuta este script desde la carpeta del proyecto."
    exit 1
fi
ok "requirements.txt encontrado"

if [[ ! -f "$PY_SCRIPT" ]]; then
    warn "No se encontro '$PY_SCRIPT'. Asegurate de colocarlo en esta carpeta."
else
    ok "$PY_SCRIPT encontrado"
fi

hr

# ---------- Paso 3: Crear entorno virtual ----------
info "Paso 3/5: Creando entorno virtual '${VENV_NAME}'..."

if [[ -d "$VENV_NAME" ]]; then
    warn "El entorno '${VENV_NAME}' ya existe."
    read -rp "${YEL}¿Deseas recrearlo desde cero? [s/N]: ${RST}" resp
    if [[ "$resp" =~ ^[sS]$ ]]; then
        rm -rf "$VENV_NAME"
        "$PYTHON_BIN" -m venv "$VENV_NAME"
        ok "Entorno recreado"
    else
        info "Usando el entorno existente"
    fi
else
    "$PYTHON_BIN" -m venv "$VENV_NAME"
    ok "Entorno '${VENV_NAME}' creado"
fi

hr

# ---------- Paso 4: Instalar dependencias ----------
info "Paso 4/5: Instalando dependencias..."

# Usar el pip del entorno virtual directamente (no requiere activar)
VENV_PIP="./${VENV_NAME}/bin/pip"
VENV_PYTHON="./${VENV_NAME}/bin/python"

if [[ ! -x "$VENV_PIP" ]]; then
    error "No se encontro pip en el entorno virtual. Algo fallo al crearlo."
    exit 1
fi

"$VENV_PIP" install --upgrade pip --quiet
"$VENV_PIP" install -r requirements.txt

ok "Dependencias instaladas"

hr

# ---------- Paso 5: Validar instalacion ----------
info "Paso 5/5: Validando instalacion..."

if "$VENV_PYTHON" -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl" 2>/dev/null; then
    ok "Todas las dependencias se importan correctamente"
else
    error "Alguna dependencia no se instalo correctamente."
    error "Revisa los mensajes anteriores o reinstala con:"
    error "  ${VENV_PIP} install -r requirements.txt"
    exit 1
fi

hr

# ---------- Preparar servers.txt ----------
info "Preparando lista de dominios..."

if [[ -f "servers.txt" ]]; then
    ok "servers.txt ya existe (no se sobrescribe)"
elif [[ -f "servers.example.txt" ]]; then
    cp servers.example.txt servers.txt
    ok "servers.txt creado a partir de servers.example.txt"
    warn "Edita servers.txt con tus dominios reales antes de auditar:"
    echo "     ${BLD}nano servers.txt${RST}"
else
    warn "No se encontro servers.example.txt. Crea servers.txt manualmente."
fi

# =============================================================================
#  RESUMEN FINAL
# =============================================================================
echo
echo "${BLD}${GRN}=====================================================================${RST}"
echo "${BLD}${GRN}  INSTALACION COMPLETADA${RST}"
echo "${BLD}${GRN}=====================================================================${RST}"
echo

USER_SHELL="$(detect_shell)"
echo "${BLD}Para ejecutar la auditoria:${RST}"
echo
echo "  ${CYA}# 1. Activar el entorno virtual${RST}"
if [[ "$USER_SHELL" == "fish" ]]; then
    echo "  source ${VENV_NAME}/bin/activate.fish"
else
    echo "  source ${VENV_NAME}/bin/activate"
fi
echo
echo "  ${CYA}# 2. Editar tus dominios (si aun no lo has hecho)${RST}"
echo "  nano servers.txt"
echo
echo "  ${CYA}# 3. Ejecutar la auditoria${RST}"
echo "  python ${PY_SCRIPT} --domains servers.txt"
echo
echo "  ${CYA}# 4. Al terminar, desactivar el entorno${RST}"
echo "  deactivate"
echo
echo "${BLD}Entorno virtual:${RST} ${VENV_NAME}"
echo "${BLD}Shell detectado:${RST} ${USER_SHELL}"
echo
echo "${BLD}${CYA}Auditoria lista · Eduardo Recinos${RST}"
echo
