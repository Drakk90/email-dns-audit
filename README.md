# 🛡️ Email DNS Audit Neon

> Auditoría automatizada de autenticación de correo electrónico — **SPF · DKIM · DMARC · DNSSEC · MTA-STS · TLS-RPT · BIMI**
> Genera un **Excel unificado** listo para entregar a Dirección, con hallazgos, severidades y evidencia trazable.

**Autor:** Eduardo Recinos · CISO
**Versión:** 3.1
**Licencia:** MIT
**Repositorio:** [github.com/Drakk90/email-dns-audit](https://github.com/Drakk90/email-dns-audit)
**Compatibilidad:** Ubuntu 20.04+ · Pop!_OS · Kali Linux · Debian 10+ · CachyOS / Arch

---

## 📋 Tabla de contenido

- [¿Qué hace esta herramienta?](#-qué-hace-esta-herramienta)
- [¿Para quién es?](#-para-quién-es)
- [Archivos del proyecto](#-archivos-del-proyecto)
- [🐧 ¿Qué sistema usas? (importante)](#-qué-sistema-usas-importante)
- [🔄 Flujo de uso: instalar una vez, ejecutar siempre](#-flujo-de-uso-instalar-una-vez-ejecutar-siempre)
- [⚡ Instalación rápida (recomendada)](#-instalación-rápida-recomendada)
- [🔧 Instalación manual (paso a paso)](#-instalación-manual-paso-a-paso)
  - [Ruta A — Ubuntu / Pop!_OS / Kali / Debian](#ruta-a--ubuntu--popos--kali--debian-bash--apt)
  - [Ruta B — CachyOS / Arch / Manjaro](#ruta-b--cachyos--arch--manjaro-fish--pacman)
- [Preparar la lista de dominios](#-preparar-la-lista-de-dominios)
- [▶️ Ejecutar la auditoría](#️-ejecutar-la-auditoría)
- [Resultados generados](#-resultados-generados)
- [Solución de problemas](#-solución-de-problemas)
- [Preguntas frecuentes](#-preguntas-frecuentes)
- [Consideraciones de seguridad](#-consideraciones-de-seguridad)
- [Licencia](#-licencia)

---

## 🎯 ¿Qué hace esta herramienta?

`email_dns_audit_neon.py` realiza una auditoría completa de la postura de seguridad del correo electrónico para uno o varios dominios. Para cada dominio evalúa:

| Control | Qué verifica |
|---|---|
| **WHOIS** | Registrar, fechas de creación/expiración, estado del dominio |
| **NS / SOA** | Nameservers y proveedor DNS detectado |
| **DNSSEC** | DNSKEY, DS, bit AD, diagnóstico de cadena de confianza |
| **SPF** | Registro, mecanismo `all`, DNS lookups, void lookups, proveedores |
| **DKIM** | 28 selectores comunes, algoritmo, tamaño de llave, modo prueba |
| **DMARC** | Política `p`/`sp`, `pct`, alineación, `rua`/`ruf`, `fo` |
| **MX** | Proveedor de correo detectado |
| **MTA-STS** | Política publicada, `max_age`, accesibilidad HTTPS |
| **TLS-RPT** | Registro de reportes de fallas TLS |
| **BIMI** | Registro, SVG, certificado VMC (descarga y parseo X.509) |

**Salida principal:** un archivo Excel (`.xlsx`) con múltiples hojas pre-formateadas, formato condicional (verde/amarillo/rojo) y listas desplegables. Además genera CSVs de respaldo y una carpeta de evidencias con marca temporal.

---

## 👥 ¿Para quién es?

Esta herramienta está diseñada para **CISOs, auditores de seguridad, administradores de sistemas y equipos de cumplimiento** que necesitan evaluar de forma rápida y repetible la configuración de autenticación de correo de sus dominios, alineado a:

- **ISO/IEC 27001:2022** (A.5.14, A.8.20, A.8.21, A.8.23)
- **NIST CSF 2.0** (PR.DS, PR.AA)
- **NIST SP 800-177 Rev.1**
- **M3AAWG Email Authentication BCP**
- **RFCs** 7208 (SPF), 6376 (DKIM), 7489 (DMARC), 8460 (TLS-RPT), 8461 (MTA-STS)

> 💡 **No necesitas ser programador.** Con el instalador automático tendrás la herramienta funcionando en menos de 5 minutos.

---

## 📁 Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `email_dns_audit_neon.py` | Script principal de auditoría |
| `setup.sh` | **Instalador** — se corre **UNA vez** (crea entorno, instala dependencias) |
| `run.sh` | **Ejecutor rápido** — se corre **cada vez** que auditas (no reinstala nada) |
| `requirements.txt` | Lista de dependencias de Python |
| `servers.example.txt` | Plantilla de dominios de muestra |
| `servers.txt` | Tu lista real de dominios (la creas tú, no se sube a Git) |
| `.gitignore` | Protege entornos y evidencia de subirse por error |
| `LICENSE` | Licencia MIT |
| `README.md` | Este documento |

---

## 🐧 ¿Qué sistema usas? (importante)

Esta herramienta funciona en **dos familias de Linux** con diferencias clave. Identifica cuál usas antes de empezar:

| Aspecto | 🟠 **Ubuntu / Pop!_OS / Kali / Debian** | 🔵 **CachyOS / Arch / Manjaro** |
|---|---|---|
| **Base** | Debian | Arch |
| **Shell por defecto** | **Bash** | **Fish** |
| **Gestor de paquetes** | `apt` | `pacman` |
| **Activar entorno** | `source venv-email-audit/bin/activate` | `source venv-email-audit/bin/activate.fish` |
| **Instalar Python** | `sudo apt install python3 python3-venv python3-pip` | `sudo pacman -S python python-pip` |
| **Problema común de pip** | Puede faltar `python3-venv` | No suele ocurrir |

> 🔍 **¿No sabes qué shell usas?** Ejecuta `echo $SHELL`. Si responde `/bin/bash` estás en Bash (🟠). Si responde `/usr/bin/fish` estás en Fish (🔵).

> ✅ **Buena noticia:** tanto `setup.sh` como `run.sh` **detectan tu sistema y shell** automáticamente. El `run.sh` incluso ejecuta la auditoría **sin que tengas que activar el entorno manualmente**.

---

## 🔄 Flujo de uso: instalar una vez, ejecutar siempre

Este es el concepto más importante para no repetir trabajo:

```
┌─────────────────────────────────────────────────────────────┐
│  PRIMERA VEZ (instalación)                                   │
│  ─────────────────────────                                   │
│  ./setup.sh          ← Instala Python, crea el entorno,      │
│                        instala dependencias. SOLO UNA VEZ.   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  CADA VEZ QUE AUDITAS                                         │
│  ───────────────────                                         │
│  ./run.sh            ← Solo ejecuta la auditoría.            │
│                        NO reinstala nada. Rapido.            │
└─────────────────────────────────────────────────────────────┘
```

> ⚠️ **No vuelvas a correr `setup.sh` cada vez.** Las dependencias quedan guardadas **permanentemente** dentro del entorno `venv-email-audit` tras la primera instalación. Para el uso diario usa `run.sh`.

---

## ⚡ Instalación rápida (recomendada)

El script `setup.sh` hace **todo** por ti en cualquier sistema: verifica Python, instala lo que falte, crea el entorno virtual, instala dependencias, valida y prepara tu `servers.txt`.

```bash
# 1. Descarga el proyecto
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit

# 2. Da permisos de ejecución a los scripts
chmod +x setup.sh run.sh

# 3. Ejecuta el instalador UNA sola vez
./setup.sh
```

Al terminar, para auditar solo necesitas:

```bash
./run.sh
```

> ✅ El instalador es **idempotente**: puedes ejecutarlo varias veces sin romper nada. Si el entorno ya existe, te preguntará si deseas recrearlo.

**¿Qué hace el `setup.sh` internamente?**

1. Detecta e instala Python 3.9+ si falta (usando `apt`, `pacman` o `dnf`).
2. **En Ubuntu/Debian/Kali:** instala el paquete exacto `python3.X-venv` para tu versión de Python (resuelve el error "No se encontró pip").
3. Crea el entorno virtual **`venv-email-audit`** con pip garantizado.
4. Instala todas las dependencias de `requirements.txt`.
5. Valida que cada librería se importe correctamente.
6. Crea tu `servers.txt` a partir de la plantilla si aún no existe.

---

## 🔧 Instalación manual (paso a paso)

Elige la ruta según tu sistema operativo. Solo necesitas esto **una vez**; después usa `run.sh`.

---

### Ruta A — Ubuntu / Pop!_OS / Kali / Debian (Bash + apt)

#### A.1 — Instalar Python y dependencias del sistema

```bash
python3 --version
```

Si ves `Python 3.9` o superior, continúa. Si no, o si falta `venv`:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

> ⚠️ **Importante para Ubuntu/Pop!_OS/Kali:** `python3-venv` es **obligatorio**. Sin él, el entorno se crea **sin pip** y verás el error `No se encontró pip`. Si tu Python es específico (ej. 3.11), instala también `sudo apt install -y python3.11-venv`.

#### A.2 — Descargar el proyecto

```bash
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit
```

#### A.3 — Crear el entorno virtual

```bash
python3 -m venv venv-email-audit
```

#### A.4 — Activar el entorno (Bash)

```bash
source venv-email-audit/bin/activate
```

> ✅ Verás `(venv-email-audit)` al inicio del prompt.

#### A.5 — Instalar dependencias

```bash
pip install -r requirements.txt
```

#### A.6 — Verificar

```bash
python -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl; print('✅ Dependencias OK')"
```

---

### Ruta B — CachyOS / Arch / Manjaro (Fish + pacman)

#### B.1 — Instalar Python

```bash
python --version
```

Si es menor a 3.9:

```bash
sudo pacman -S --needed python python-pip
```

> 💡 En Arch, Python viene completo con `venv` y `ensurepip`, así que no hay problemas de pip.

#### B.2 — Descargar el proyecto

```bash
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit
```

#### B.3 — Crear el entorno virtual

```bash
python -m venv venv-email-audit
```

#### B.4 — Activar el entorno (Fish)

```fish
source venv-email-audit/bin/activate.fish
```

> ⚠️ **La extensión `.fish` es obligatoria en CachyOS.** Con `activate` sin extensión verás `"case" builtin not inside of switch block`.

#### B.5 — Instalar dependencias

```fish
pip install -r requirements.txt
```

#### B.6 — Verificar

```fish
python -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl; print('✅ Dependencias OK')"
```

---

## 📝 Preparar la lista de dominios

Copia la plantilla y edítala con tus dominios reales (igual en ambos sistemas):

```bash
cp servers.example.txt servers.txt
nano servers.txt
```

Ejemplo:

```text
# Líneas que empiezan con # son comentarios
midominio.com
otrodominio.org
sucursal.midominio.com
```

**Reglas:**

- Un dominio por línea.
- Sin `http://`, sin `https://`, sin `/` final.
- Las líneas con `#` son comentarios; las vacías se ignoran.

> 🔒 `servers.txt` está en el `.gitignore`, así que tu lista real **nunca se sube** al repositorio.

---

## ▶️ Ejecutar la auditoría

Hay **dos formas**. La recomendada para uso diario es el `run.sh`.

### 🚀 Opción 1 — Con `run.sh` (recomendada, la más simple)

El `run.sh` verifica que todo esté listo y ejecuta la auditoría **sin que tengas que activar el entorno manualmente**. Funciona igual en Bash y en Fish.

```bash
# Con servers.txt por defecto
./run.sh

# Con otro archivo de dominios
./run.sh mis_dominios.txt
```

**¿Qué hace el `run.sh`?**

1. Verifica que el entorno `venv-email-audit` exista.
2. Verifica que las 7 dependencias estén instaladas (sin reinstalar).
3. Verifica que exista tu `servers.txt`.
4. Ejecuta la auditoría usando el Python del entorno directamente.

> Si falta algo, el `run.sh` te avisa exactamente qué hacer (por ejemplo, correr `setup.sh` una vez). **No reinstala nada por su cuenta**, así que es rápido.

### 🔧 Opción 2 — Activando el entorno manualmente

Si prefieres el método clásico:

**🟠 Ubuntu / Pop!_OS / Kali / Debian (Bash):**

```bash
source venv-email-audit/bin/activate
python email_dns_audit_neon.py --domains servers.txt
deactivate
```

**🔵 CachyOS / Arch / Manjaro (Fish):**

```fish
source venv-email-audit/bin/activate.fish
python email_dns_audit_neon.py --domains servers.txt
deactivate
```

### Opciones del script

| Opción | Descripción | Ejemplo |
|---|---|---|
| `--domains`, `-d` | Archivo con la lista de dominios **(requerido)** | `-d servers.txt` |
| `--selectors`, `-s` | Selectores DKIM adicionales | `-s "corp2026 mkt"` |
| `--resolver`, `-r` | Resolver DNS (por defecto `1.1.1.1`) | `-r 8.8.8.8` |
| `--output`, `-o` | Carpeta de salida | `-o ~/auditorias/Q2` |
| `--excel-name` | Nombre del Excel | `--excel-name Audit_2026.xlsx` |
| `--help`, `-h` | Muestra la ayuda | `-h` |

> 💡 El `run.sh` pasa el archivo de dominios automáticamente. Para usar opciones avanzadas (resolver, selectores, etc.), usa la Opción 2 con el entorno activado.

---

## 📊 Resultados generados

Al terminar se crea una carpeta `audit_<fecha_hora>/`:

```
audit_20260630_143022/
├── Auditoria_Email_Authentication_<fecha>.xlsx   ← 📄 ENTREGABLE PRINCIPAL
├── audit_spf.csv                                  ← Respaldos CSV
├── audit_dkim.csv
├── ... (un CSV por control)
└── evidencias/                                    ← Evidencia trazable
    └── midominio.com/
        ├── whois.txt
        ├── dig_dmarc.txt
        └── ... (cada consulta con timestamp ISO 8601)
```

### Hojas del Excel unificado

| Hoja | Contenido |
|---|---|
| **Portada** | Metadata, marco normativo, convenciones |
| **Inventario_Dominios** | Registrar, expiración, DNS, DNSSEC |
| **SPF / DKIM / DMARC / DNSSEC** | Una hoja por control con estado y severidad |
| **Complementos** | MTA-STS, TLS-RPT, BIMI |
| **Remitentes_Autorizados** | Proveedores cruzados con SPF/DKIM/DMARC |
| **Hallazgos** | Lista priorizada con severidad y recomendación |
| **Resumen_Consolidado** | Vista global con % de cumplimiento por dominio |

> 🎨 Formato condicional automático: verde (Cumple), amarillo (Parcial), rojo (No cumple), y colores por severidad.

### Ver los resultados de forma gráfica

```bash
xdg-open audit_*/Auditoria_Email_Authentication_*.xlsx
# o
libreoffice audit_*/Auditoria_Email_Authentication_*.xlsx
```

---

## 🔧 Solución de problemas

### ❌ "Cada vez que audito tengo que correr `setup.sh` de nuevo"

**Causa:** la primera instalación falló al instalar dependencias (típico del problema `python3-venv` en Ubuntu), por lo que el entorno quedó vacío.

**Solución:** confirma qué hay en el entorno:

```bash
source venv-email-audit/bin/activate    # o activate.fish en Fish
pip list | grep -Ei "rich|dnspython|cryptography|httpx|whois|aiodns|openpyxl"
deactivate
```

- **Si aparecen las 7 librerías:** el entorno está bien. Usa `./run.sh` de aquí en adelante, **no** `setup.sh`.
- **Si NO aparecen:** corre `./setup.sh` **una última vez** con la versión corregida. Quedará permanente.

---

### ❌ `error: externally-managed-environment`

**Causa:** intentaste instalar con `pip` sin activar el entorno virtual (protección PEP 668).

**Solución:** activa el entorno antes de `pip install`:

```bash
# Bash
source venv-email-audit/bin/activate
# Fish
source venv-email-audit/bin/activate.fish

pip install -r requirements.txt
```

---

### ❌ `No se encontró pip en el entorno virtual` (Ubuntu/Pop!_OS/Kali)

**Causa:** falta `python3-venv`, por lo que el entorno se creó sin pip.

**Solución:**

```bash
sudo apt install -y python3-venv python3-pip
rm -rf venv-email-audit
./setup.sh
```

---

### ❌ `"case" builtin not inside of switch block` (CachyOS/Arch)

**Causa:** usas Fish y ejecutaste el script de activación de Bash.

**Solución:**

```fish
source venv-email-audit/bin/activate.fish
```

---

### ❌ `Permission denied` al ejecutar `./setup.sh` o `./run.sh`

**Causa:** falta permiso de ejecución (común tras descargar de GitHub web).

**Solución:**

```bash
chmod +x setup.sh run.sh
```

---

### ❌ `requirements.txt` con `&gt;` o `&lt;`

**Causa:** entidades HTML por copy-paste desde una web.

**Solución:**

```bash
sed -i 's/&gt;/>/g; s/&lt;/</g; s/&amp;/\&/g' requirements.txt
```

---

### ⚠️ WHOIS devuelve `N/D` para dominios `.gt`, `.cr`, etc.

**Causa:** algunos ccTLD no exponen datos completos vía WHOIS.

**Solución:** es normal. Verifica esos datos en el panel de tu registrar.

---

## ❓ Preguntas frecuentes

**¿Cuándo uso `setup.sh` y cuándo `run.sh`?**
`setup.sh` una sola vez para instalar. `run.sh` cada vez que auditas. Nunca necesitas repetir `setup.sh`.

**¿El `run.sh` funciona en Fish y en Bash?**
Sí. Usa el Python del entorno directamente, así que no depende de tu shell ni requiere activar el venv.

**¿Necesito conocimientos de programación?**
No. Con `./setup.sh` una vez y `./run.sh` para auditar es suficiente.

**¿Modifica algo en mis dominios o DNS?**
No. La herramienta **solo lee** (consultas DNS y HTTP públicas). Nunca escribe.

**¿Cuánto tarda?**
~10-15 segundos por dominio gracias a consultas asíncronas.

**¿Puedo auditar dominios que no son míos?**
Técnicamente sí (solo datos públicos), pero **audita únicamente dominios propios o autorizados**.

---

## 🔒 Consideraciones de seguridad

- ✅ Realiza **solo consultas de lectura** (DNS, WHOIS, HTTP público). No modifica configuraciones.
- ⚠️ **Audita únicamente dominios propios o autorizados.**
- 🔐 Los archivos de **evidencia** contienen información de tu infraestructura. Trátalos como confidenciales.
- 🗂️ El Excel es un **documento de auditoría**. Almacénalo según tu política de retención (ISO 27001 A.5.33).
- 🚫 El `.gitignore` evita que entornos, evidencia y tu `servers.txt` real se suban por error a Git.

---

## 📄 Licencia

Este proyecto se distribuye bajo la **Licencia MIT**. Consulta el archivo [`LICENSE`](LICENSE) para más detalles.

Úsalo de forma **ética y responsable**. El autor no se hace responsable del uso indebido.

---

<div align="center">

**Desarrollado por Eduardo Recinos**
*Compartido para la comunidad de CISOs y profesionales de seguridad*

⭐ Si te fue útil, considera dejar una estrella en el repositorio.

</div>
