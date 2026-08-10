#!/usr/bin/env bash
# =============================================================================
#  setup.sh — Instalador automatico de Email DNS Audit Neon
#  Autor: Eduardo Recinos
#  Repositorio: https://github.com/Drakk90/email-dns-audit
#  Compatibilidad: Kali Linux, Ubuntu 20.04+, Debian 10+, CachyOS/Arch, Fedora
#
#  Este script es AUTONOMO: detecta y resuelve automaticamente los problemas
#  comunes de pip/venv/ensurepip sin fallar, tanto si ya estan instalados
#  como si faltan.
#
#    1. Verifica Python 3.9+ (lo instala si falta)
#    2. Asegura venv + ensurepip (instalando el paquete exacto de tu version
#       de Python en Debian/Ubuntu/Kali: python3.X-venv)
#    3. Crea el entorno virtual "venv-email-audit" con pip garantizado
#    4. Repara pip dentro del venv si por alguna razon falta
#    5. Instala las dependencias de requirements.txt
#    6. Valida la instalacion
#    7. Prepara servers.txt a partir de servers.example.txt
#
#  Uso:
#    chmod +x setup.sh
#    ./setup.sh
# =============================================================================

set -uo pipefail

# ---------- Colores ----------
if [[ -t 1 ]]; then
    RED=$'\e[31m'; GRN=$'\e[32m'; YEL=$'\e[33m'
    BLU=$'\e[34m'; CYA=$'\e[36m'; BLD=$'\e[1m'; RST=$'\e[0m'
else
    RED=""; GRN=""; YEL=""; BLU=""; CYA=""; BLD=""; RST=""
fi

VENV_NAME="venv-email-audit"
PY_SCRIPT="email_dns_audit_neon.py"

# ---------- Auxiliares ----------
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

detect_pkg_manager() {
    if command -v apt &>/dev/null; then echo "apt"
    elif command -v pacman &>/dev/null; then echo "pacman"
    elif command -v dnf &>/dev/null; then echo "dnf"
    else echo "unknown"; fi
}

detect_shell() { basename "${SHELL:-bash}"; }

# ---------- Verificar si sudo esta disponible ----------
have_sudo() {
    if command -v sudo &>/dev/null; then return 0; fi
    return 1
}

run_priv() {
    # Ejecuta un comando con privilegios si es posible; si ya es root, directo.
    if [[ "$(id -u)" -eq 0 ]]; then
        "$@"
    elif have_sudo; then
        sudo "$@"
    else
        warn "No hay 'sudo' ni eres root. Ejecuta manualmente: $*"
        return 1
    fi
}

# =============================================================================
#  Instala venv/pip segun distro, detectando la version EXACTA de Python
#  en sistemas Debian/Ubuntu/Kali (python3.X-venv).
# =============================================================================
ensure_venv_packages() {
    local pkg
    pkg="$(detect_pkg_manager)"
    case "$pkg" in
        apt)
            # Detectar version exacta para instalar python3.X-venv correcto
            local pyver
            pyver="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)"
            info "Instalando paquetes de venv/pip para Python ${pyver} (apt)..."
            run_priv apt update -y || true
            # Intentar el paquete versionado primero (mas confiable en Debian/Kali)
            if ! run_priv apt install -y "python${pyver}-venv" 2>/dev/null; then
                warn "python${pyver}-venv no disponible; probando python3-venv generico..."
                run_priv apt install -y python3-venv || true
            fi
            run_priv apt install -y python3-pip || true
            ;;
        pacman)
            info "Instalando python/pip (pacman)..."
            run_priv pacman -S --needed --noconfirm python python-pip || true
            ;;
        dnf)
            info "Instalando python3/pip (dnf)..."
            run_priv dnf install -y python3-venv python3-pip || true
            ;;
        *)
            warn "Gestor de paquetes no detectado. Instala python3-venv y python3-pip manualmente."
            ;;
    esac
}

# =============================================================================
#  INICIO
# =============================================================================
banner

# ---------- Paso 1: Python ----------
info "Paso 1/7: Verificando Python 3..."

PYTHON_BIN=""
if command -v python3 &>/dev/null; then PYTHON_BIN="python3"
elif command -v python &>/dev/null; then PYTHON_BIN="python"; fi

if [[ -z "$PYTHON_BIN" ]]; then
    warn "Python 3 no esta instalado. Intentando instalar..."
    pkg="$(detect_pkg_manager)"
    case "$pkg" in
        apt)    run_priv apt update -y && run_priv apt install -y python3 python3-pip python3-venv ;;
        pacman) run_priv pacman -S --needed --noconfirm python python-pip ;;
        dnf)    run_priv dnf install -y python3 python3-pip ;;
        *)      error "No se pudo instalar Python automaticamente. Instalalo manualmente."; exit 1 ;;
    esac
    PYTHON_BIN="python3"
fi

if ! command -v "$PYTHON_BIN" &>/dev/null; then
    error "Python sigue sin estar disponible tras el intento de instalacion."
    exit 1
fi

PY_VERSION="$("$PYTHON_BIN" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
PY_MAJOR="$(echo "$PY_VERSION" | cut -d. -f1)"
PY_MINOR="$(echo "$PY_VERSION" | cut -d. -f2)"

if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 9 ]]; }; then
    error "Se requiere Python 3.9 o superior. Version detectada: $PY_VERSION"
    error "Actualiza tu sistema (ej: sudo apt upgrade) e intenta de nuevo."
    exit 1
fi
ok "Python $PY_VERSION detectado ($PYTHON_BIN)"

hr

# ---------- Paso 2: Asegurar venv + ensurepip (idempotente) ----------
info "Paso 2/7: Verificando venv y ensurepip..."

venv_ok()      { "$PYTHON_BIN" -m venv --help &>/dev/null; }
ensurepip_ok() { "$PYTHON_BIN" -m ensurepip --version &>/dev/null; }

if venv_ok && ensurepip_ok; then
    ok "venv y ensurepip ya estan disponibles (no se requiere instalacion)"
else
    if ! venv_ok; then warn "Modulo 'venv' no disponible."; fi
    if ! ensurepip_ok; then warn "Modulo 'ensurepip' no disponible (causa el error 'No se encontro pip')."; fi

    ensure_venv_packages

    # Re-verificar tras instalar
    if venv_ok && ensurepip_ok; then
        ok "venv y ensurepip quedaron disponibles"
    elif venv_ok && ! ensurepip_ok; then
        warn "venv OK pero ensurepip sigue ausente; se compensara con --upgrade-deps al crear el venv."
    else
        warn "No se pudo confirmar venv/ensurepip; se intentara crear el venv de todas formas."
    fi
fi

hr

# ---------- Paso 3: Archivos del proyecto ----------
info "Paso 3/7: Verificando archivos del proyecto..."

if [[ ! -f "requirements.txt" ]]; then
    error "No se encontro 'requirements.txt' en el directorio actual."
    error "Ejecuta este script desde la carpeta del proyecto (donde estan los archivos)."
    exit 1
fi
ok "requirements.txt encontrado"

if [[ ! -f "$PY_SCRIPT" ]]; then
    warn "No se encontro '$PY_SCRIPT'. Coloca tu script en esta carpeta antes de auditar."
else
    ok "$PY_SCRIPT encontrado"
fi

hr

# ---------- Paso 4: Crear entorno virtual ----------
info "Paso 4/7: Creando entorno virtual '${VENV_NAME}'..."

create_venv() {
    # Preferir --upgrade-deps (instala/actualiza pip dentro del venv).
    # Si la version de Python no lo soporta, caer al metodo estandar.
    if "$PYTHON_BIN" -m venv --upgrade-deps "$VENV_NAME" 2>/dev/null; then
        return 0
    fi
    warn "'--upgrade-deps' no soportado en esta version; usando metodo estandar..."
    "$PYTHON_BIN" -m venv "$VENV_NAME"
}

if [[ -d "$VENV_NAME" ]]; then
    warn "El entorno '${VENV_NAME}' ya existe."
    read -rp "${YEL}¿Deseas recrearlo desde cero? [s/N]: ${RST}" resp
    if [[ "$resp" =~ ^[sS]$ ]]; then
        rm -rf "$VENV_NAME"
        create_venv && ok "Entorno recreado" || { error "Fallo al recrear el entorno."; exit 1; }
    else
        info "Usando el entorno existente"
    fi
else
    create_venv && ok "Entorno '${VENV_NAME}' creado" || { error "Fallo al crear el entorno."; exit 1; }
fi

hr

# ---------- Paso 5: Garantizar pip DENTRO del venv ----------
info "Paso 5/7: Verificando pip dentro del entorno..."

VENV_PIP="./${VENV_NAME}/bin/pip"
VENV_PYTHON="./${VENV_NAME}/bin/python"

# Intento 1: si pip ya existe, perfecto (caso normal)
if [[ -x "$VENV_PIP" ]]; then
    ok "pip ya esta presente en el entorno"
else
    # Intento 2: reparar con ensurepip del propio venv
    warn "pip no encontrado en el entorno; reparando con ensurepip..."
    if "$VENV_PYTHON" -m ensurepip --upgrade &>/dev/null; then
        ok "pip instalado en el entorno via ensurepip"
    else
        # Intento 3: instalar paquetes del sistema y recrear el venv
        warn "ensurepip del venv fallo; instalando paquetes del sistema y recreando..."
        ensure_venv_packages
        rm -rf "$VENV_NAME"
        create_venv
        if [[ ! -x "$VENV_PIP" ]]; then
            "$VENV_PYTHON" -m ensurepip --upgrade &>/dev/null || true
        fi
    fi
fi

# Verificacion definitiva
if [[ ! -x "$VENV_PIP" ]] && ! "$VENV_PYTHON" -m pip --version &>/dev/null; then
    error "No fue posible habilitar pip dentro del entorno virtual."
    error "Solucion manual (Debian/Ubuntu/Kali):"
    error "  sudo apt install -y python${PY_VERSION}-venv python3-pip"
    error "  rm -rf ${VENV_NAME}"
    error "  ./setup.sh"
    exit 1
fi
ok "pip operativo en el entorno virtual"

hr

# ---------- Paso 6: Instalar dependencias ----------
info "Paso 6/7: Instalando dependencias..."

# Usar 'python -m pip' garantiza que funcione aunque el wrapper 'pip' no exista
"$VENV_PYTHON" -m pip install --upgrade pip --quiet
"$VENV_PYTHON" -m pip install -r requirements.txt

ok "Dependencias instaladas"

hr

# ---------- Paso 7: Validar ----------
info "Paso 7/7: Validando instalacion..."

if "$VENV_PYTHON" -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl" 2>/dev/null; then
    ok "Todas las dependencias se importan correctamente"
else
    error "Alguna dependencia no se instalo correctamente."
    error "Reinstala con: ${VENV_PYTHON} -m pip install -r requirements.txt"
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
echo "${BLD}Python:${RST} ${PY_VERSION}"
echo
echo "${BLD}${CYA}Auditoria lista · Eduardo Recinos${RST}"
echo
