# 🛡️ Email DNS Audit Neon

> Auditoría automatizada de autenticación de correo electrónico — **SPF · DKIM · DMARC · DNSSEC · MTA-STS · TLS-RPT · BIMI**
> Genera un **Excel unificado** listo para entregar a Dirección, con hallazgos, severidades y evidencia trazable.

**Autor:** Eduardo Recinos · CISO
**Versión:** 3.0
**Licencia:** MIT
**Repositorio:** [github.com/Drakk90/email-dns-audit](https://github.com/Drakk90/email-dns-audit)
**Compatibilidad:** Ubuntu 20.04+ · Pop!_OS · Kali Linux · Debian 10+ · CachyOS / Arch

---

## 📋 Tabla de contenido

- [¿Qué hace esta herramienta?](#-qué-hace-esta-herramienta)
- [¿Para quién es?](#-para-quién-es)
- [Archivos del proyecto](#-archivos-del-proyecto)
- [🐧 ¿Qué sistema usas? (importante)](#-qué-sistema-usas-importante)
- [⚡ Instalación rápida (recomendada)](#-instalación-rápida-recomendada)
- [🔧 Instalación manual (paso a paso)](#-instalación-manual-paso-a-paso)
  - [Ruta A — Ubuntu / Pop!_OS / Kali / Debian](#ruta-a--ubuntu--popos--kali--debian-bash--apt)
  - [Ruta B — CachyOS / Arch / Manjaro](#ruta-b--cachyos--arch--manjaro-fish--pacman)
- [Preparar la lista de dominios](#-preparar-la-lista-de-dominios)
- [Ejecutar la auditoría](#-ejecutar-la-auditoría)
- [Resultados generados](#-resultados-generados)
- [Uso recurrente](#-uso-recurrente)
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
| `setup.sh` | **Instalador automático** (crea entorno, instala todo, valida) |
| `requirements.txt` | Lista de dependencias de Python |
| `servers.example.txt` | Plantilla de dominios de muestra |
| `servers.txt` | Tu lista real de dominios (la creas tú, no se sube a Git) |
| `.gitignore` | Protege entornos y evidencia de subirse por error |
| `LICENSE` | Licencia MIT |
| `README.md` | Este documento |

---

## 🐧 ¿Qué sistema usas? (importante)

Esta herramienta funciona en **dos familias de Linux** que tienen diferencias clave. Identifica cuál usas antes de empezar:

| Aspecto | 🟠 **Ubuntu / Pop!_OS / Kali / Debian** | 🔵 **CachyOS / Arch / Manjaro** |
|---|---|---|
| **Base** | Debian | Arch |
| **Shell por defecto** | **Bash** | **Fish** |
| **Gestor de paquetes** | `apt` | `pacman` |
| **Activar entorno** | `source venv-email-audit/bin/activate` | `source venv-email-audit/bin/activate.fish` |
| **Instalar Python** | `sudo apt install python3 python3-venv python3-pip` | `sudo pacman -S python python-pip` |
| **Encadenar comandos** | `comando1 && comando2` | `comando1; and comando2` |
| **Problema común de pip** | Puede faltar `python3-venv` | No suele ocurrir |

> 🔍 **¿No sabes cuál shell usas?** Ejecuta `echo $SHELL`. Si responde `/bin/bash` estás en Bash (🟠). Si responde `/usr/bin/fish` estás en Fish (🔵).

> ✅ **Buena noticia:** el instalador automático `setup.sh` **detecta tu sistema y shell**, instala lo correcto y te muestra al final el comando de activación exacto para tu caso. No tienes que memorizar estas diferencias.

---

## ⚡ Instalación rápida (recomendada)

El script `setup.sh` hace **todo** por ti en cualquiera de los dos sistemas: verifica Python, instala lo que falte (`python3-venv` en Ubuntu o `python-pip` en Arch), crea el entorno virtual, instala dependencias, valida y prepara tu `servers.txt`.

```bash
# 1. Descarga el proyecto
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit

# 2. Da permisos de ejecución al instalador
chmod +x setup.sh

# 3. Ejecuta el instalador
./setup.sh
```

Eso es todo. El instalador te mostrará al final los comandos exactos para ejecutar tu primera auditoría según tu shell (Bash o Fish).

> ✅ El instalador es **idempotente**: puedes ejecutarlo varias veces sin problemas. Si el entorno ya existe, te preguntará si deseas recrearlo.

**¿Qué hace el `setup.sh` internamente?**

1. Detecta e instala Python 3.9+ si falta (usando `apt`, `pacman` o `dnf` según tu sistema).
2. **En Ubuntu/Debian/Kali:** instala el paquete exacto `python3.X-venv` para tu versión de Python (resuelve el error "No se encontró pip").
3. Verifica que los archivos del proyecto estén presentes.
4. Crea el entorno virtual **`venv-email-audit`** con pip garantizado.
5. Instala todas las dependencias de `requirements.txt`.
6. Valida que cada librería se importe correctamente.
7. Crea tu `servers.txt` a partir de la plantilla si aún no existe.

Si prefieres entender cada paso o el instalador falla, usa la [instalación manual](#-instalación-manual-paso-a-paso).

---

## 🔧 Instalación manual (paso a paso)

Elige la ruta según tu sistema operativo.

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

> ⚠️ **Importante para Ubuntu/Pop!_OS/Kali:** el paquete `python3-venv` es **obligatorio**. Sin él, el entorno virtual se crea **sin pip** y verás el error `No se encontró pip`. Si tu versión de Python es específica (ej. 3.11), instala también `sudo apt install -y python3.11-venv`.

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

> ✅ Verás `(venv-email-audit)` al inicio de tu prompt:
> ```
> (venv-email-audit) usuario@pop-os:~/email-dns-audit$
> ```

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

#### B.1 — Instalar Python y dependencias del sistema

```bash
python --version
```

Si ves `Python 3.9` o superior, continúa. Si no:

```bash
sudo pacman -S --needed python python-pip
```

> 💡 En Arch, Python viene completo con `venv` y `ensurepip` incluidos, así que no suele haber problemas de pip.

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

> ⚠️ **La extensión `.fish` es obligatoria en CachyOS.** Si usas `activate` sin extensión, verás el error `"case" builtin not inside of switch block`.

> ✅ Verás `(venv-email-audit)` al inicio de tu prompt.

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

Ejemplo de contenido:

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

> 🔒 `servers.txt` está en el `.gitignore`, así que tu lista real **nunca se sube** al repositorio. Solo se comparte `servers.example.txt`.

---

## ▶️ Ejecutar la auditoría

Con el entorno activado y `servers.txt` preparado (igual en ambos sistemas):

```bash
python email_dns_audit_neon.py --domains servers.txt
```

### Opciones disponibles

| Opción | Descripción | Ejemplo |
|---|---|---|
| `--domains`, `-d` | Archivo con la lista de dominios **(requerido)** | `-d servers.txt` |
| `--selectors`, `-s` | Selectores DKIM adicionales | `-s "corp2026 mkt"` |
| `--resolver`, `-r` | Resolver DNS (por defecto `1.1.1.1`) | `-r 8.8.8.8` |
| `--output`, `-o` | Carpeta de salida | `-o ~/auditorias/Q2` |
| `--excel-name` | Nombre del Excel | `--excel-name Audit_2026.xlsx` |
| `--help`, `-h` | Muestra la ayuda | `-h` |

**Ejemplos:**

```bash
# Básica
python email_dns_audit_neon.py --domains servers.txt

# Con selectores DKIM de tu organización
python email_dns_audit_neon.py -d servers.txt -s "corp2026 marketing"

# Resolver de Google y carpeta específica
python email_dns_audit_neon.py -d servers.txt -r 8.8.8.8 -o ~/auditorias/2026Q2
```

---

## 📊 Resultados generados

Al terminar se crea una carpeta `audit_<fecha_hora>/`:

```
audit_20260630_143022/
├── Auditoria_Email_Authentication_<fecha>.xlsx   ← 📄 ENTREGABLE PRINCIPAL
├── audit_spf.csv                                  ← Respaldos CSV
├── audit_dkim.csv
├── audit_dmarc.csv
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

Abre el Excel con doble clic o desde terminal:

```bash
# Ubuntu / Pop!_OS / Kali (GNOME)
xdg-open audit_*/Auditoria_Email_Authentication_*.xlsx

# Con LibreOffice explícito
libreoffice audit_*/Auditoria_Email_Authentication_*.xlsx
```

---

## 🔁 Uso recurrente

Una vez instalado, para futuras auditorías solo necesitas activar el entorno y ejecutar. **El comando de activación depende de tu sistema:**

### 🟠 Ubuntu / Pop!_OS / Kali / Debian (Bash)

```bash
cd ~/email-dns-audit
source venv-email-audit/bin/activate
python email_dns_audit_neon.py --domains servers.txt
deactivate
```

### 🔵 CachyOS / Arch / Manjaro (Fish)

```fish
cd ~/email-dns-audit
source venv-email-audit/bin/activate.fish
python email_dns_audit_neon.py --domains servers.txt
deactivate
```

### 💡 Atajo opcional

**En Bash** (Ubuntu/Pop!_OS/Kali) — edita `~/.bashrc`:

```bash
echo "alias audit-email='cd ~/email-dns-audit && source venv-email-audit/bin/activate && python email_dns_audit_neon.py --domains servers.txt'" >> ~/.bashrc
source ~/.bashrc
```

**En Fish** (CachyOS) — crea una función persistente:

```fish
function audit-email
    cd ~/email-dns-audit
    source venv-email-audit/bin/activate.fish
    python email_dns_audit_neon.py --domains servers.txt
end
funcsave audit-email
```

Luego solo escribes `audit-email` en cualquiera de los dos.

---

## 🔧 Solución de problemas

### ❌ `error: externally-managed-environment` (Ubuntu/Pop!_OS/Kali/Arch)

**Causa:** intentaste instalar con `pip` sin activar el entorno virtual. Es una protección de PEP 668.

**Solución:** activa el entorno **antes** de `pip install`:

```bash
# Bash (Ubuntu/Pop!_OS/Kali)
source venv-email-audit/bin/activate

# Fish (CachyOS)
source venv-email-audit/bin/activate.fish

# Luego
pip install -r requirements.txt
```

---

### ❌ `No se encontró pip en el entorno virtual` (Ubuntu/Pop!_OS/Kali)

**Causa:** falta el paquete `python3-venv`, por lo que el entorno se creó sin pip. Es el error más común en sistemas basados en Debian.

**Solución:**

```bash
# Instala el paquete que falta (usa tu versión de Python si es específica)
sudo apt install -y python3-venv python3-pip

# Borra el entorno incompleto
rm -rf venv-email-audit

# Vuelve a ejecutar el instalador
./setup.sh
```

> El `setup.sh` actualizado ya detecta e instala automáticamente `python3.X-venv` para tu versión exacta de Python.

---

### ❌ `"case" builtin not inside of switch block` (CachyOS/Arch)

**Causa:** usas Fish shell y ejecutaste el script de activación de Bash.

**Solución:** usa la versión `.fish`:

```fish
source venv-email-audit/bin/activate.fish
```

---

### ❌ `ModuleNotFoundError: No module named 'rich'`

**Causa:** el entorno no está activado o faltan dependencias.

**Solución:** activa el entorno (según tu shell) y reinstala:

```bash
# Bash
source venv-email-audit/bin/activate
# Fish
source venv-email-audit/bin/activate.fish

pip install -r requirements.txt
```

---

### ❌ `Permission denied` al ejecutar `./setup.sh`

**Causa:** el script no tiene permisos de ejecución (común tras descargar de GitHub web).

**Solución:**

```bash
chmod +x setup.sh
./setup.sh
```

---

### ❌ `requirements.txt` con `&gt;` o `&lt;`

**Causa:** entidades HTML por copy-paste desde una web renderizada.

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

**¿Funciona igual en Ubuntu/Pop!_OS y en CachyOS/Arch?**
Sí. La única diferencia práctica es el comando de activación del entorno (`activate` en Bash vs `activate.fish` en Fish). El `setup.sh` lo detecta por ti.

**¿Necesito conocimientos de programación?**
No. Con `./setup.sh` y copiar/pegar comandos es suficiente.

**¿Modifica algo en mis dominios o DNS?**
No. La herramienta **solo lee** (consultas DNS y HTTP públicas). Nunca escribe.

**¿Cuánto tarda?**
~10-15 segundos por dominio gracias a consultas asíncronas.

**¿Puedo auditar dominios que no son míos?**
Técnicamente sí (solo datos públicos), pero **audita únicamente dominios propios o autorizados**.

**¿Puedo automatizarlo con cron?**
Sí. Recuerda activar el entorno virtual dentro del script de cron con la ruta absoluta.

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
