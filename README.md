# 🛡️ Email DNS Audit Neon (v3.3)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gentle-AI Ready](https://img.shields.io/badge/Ecosystem-Gentle--AI-purple.svg)](https://github.com/Gentleman-Programming/gentle-ai)

> **Bilingual Automated Email Authentication & DNS Security Auditor**  
> *Auditoría automatizada y bilingüe de autenticación de correo electrónico y seguridad DNS.*  
> **SPF · DKIM · DMARC · DNSSEC · MTA-STS · TLS-RPT · BIMI · CAA · TLS Certs**

---

## 🌐 Language Navigation / Navegación de Idioma

- 🇬🇧 [English Documentation](#-english-documentation)
- 🇪🇸 [Documentación en Español](#-documentación-en-español)

---

# 🇬🇧 English Documentation

## 📋 Executive Overview

**Email DNS Audit Neon** is a high-performance, asynchronous CLI security scanner designed for **CISOs, Security Engineers, SOC Teams, and System Administrators**. It conducts automated, deep technical evaluations of email domain authentication mechanisms and DNS security postures, producing an **executive, unified Excel report (`.xlsx`)** with conditional formatting, actionable findings, and time-stamped raw DNS/SSL evidence.

### Supported Security Controls

| Control | Scope Evaluated |
|---|---|
| **WHOIS & RDAP** | Registrar identity, creation/expiration dates, domain status, WHOIS DNSSEC flag |
| **NS & SOA** | Authoritative Name Servers, SOA serial, detected DNS hosting provider (Cloudflare, Route53, etc.) |
| **DNSSEC** | DNSKEY publication, DS in parent zone, AD bit validation across **multi-resolvers** (Cloudflare, Google, Quad9) |
| **SPF (RFC 7208)** | Full record text, `all` mechanism enforcement (`-all`, `~all`, `+all`, `?all`), 10-lookup limit, void lookups, sender consolidation |
| **DKIM (RFC 6376)** | Common (~55) and deep rotated (~166) selectors, cryptographic key size (bits), algorithm, `t=y` test flag |
| **DMARC (RFC 7489)** | Policy status (`p=none`, `quarantine`, `reject`), subdomain policy (`sp`), alignment (`aspf`, `adkim`), `rua`/`ruf` mailboxes, percentage (`pct`) |
| **MX & Email Gateway** | Mail exchange routing and provider detection (Google Workspace, M365, Mimecast, Proofpoint, etc.) |
| **MTA-STS (RFC 8461)** | Policy publication, `max_age`, TLS enforcement mode, HTTPS `/.well-known/mta-sts.txt` policy fetch |
| **TLS-RPT (RFC 8460)** | TLS reporting TXT records (`_smtp._tls`), `rua` report destination |
| **BIMI** | Brand Indicators for Message Identification TXT record, SVG logo URI, VMC (Verified Mark Certificate) X.509 parsing |
| **CAA & TLS Health** | Authorized CAs (issue/issuewild), incident notification (`iodef`), MX FCrDNS (Forward Confirmed reverse DNS), and SSL certificate expiration |

---

## ⚡ Quickstart & Multi-Platform Setup

### Prerequisites
- **Python 3.10+** (Download from [python.org](https://www.python.org/downloads/) — *Make sure to check "Add python.exe to PATH"*).
- Compatible with: **Windows 10/11**, **Linux** (Ubuntu, Kali, Debian, Arch, Fedora), and **macOS** (10.15+).

---

### 🪟 Windows (Zero-Friction / Beginners)

#### Option A: Double-Click Setup (Easiest)
1. Download or clone this repository to your computer.
2. **Double-click `setup.bat`** to automatically configure the virtual environment and install all dependencies.
3. **Double-click `run.bat`** to start the interactive scanner!

#### Option B: Windows PowerShell
Open **PowerShell** in the project folder:
```powershell
# 1. Allow script execution for current session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 2. Run automated setup
.\setup.ps1

# 3. Launch interactive runner
.\run.ps1
```

---

### 🐧 Linux & 🍎 macOS (Bash / Zsh)

#### 1. Setup
```bash
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit

# Run the installer (works directly with bash)
bash setup.sh
```

#### 2. Run
```bash
# Interactive Runner (Prompts for Language & Target):
bash run.sh

# Direct single domain scan in English:
bash run.sh google.com normal 30 en

# Batch list scan in English:
bash run.sh servers.txt normal 30 en
```

---

## ❓ Troubleshooting & Frequently Asked Questions (FAQ)

<details>
<summary><b>1. "Python is not recognized as an internal or external command" (Windows)</b></summary>

**Cause:** Python is not installed or the "Add to PATH" checkbox was not enabled during installation.  
**Fix:**
1. Download Python 3.10+ from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer and **check the box: "Add python.exe to PATH"** at the bottom of the first screen.
3. Click "Install Now", close all terminal windows, and double-click `setup.bat` again.
</details>

<details>
<summary><b>2. "Running scripts is disabled on this system" (PowerShell ExecutionPolicy)</b></summary>

**Cause:** Windows restricts unsigned `.ps1` script execution by default.  
**Fix:**
- Double-click **`setup.bat`** and **`run.bat`** (they automatically bypass this restriction safely).  
- Or in PowerShell run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` before executing `.\setup.ps1`.
</details>

<details>
<summary><b>3. "Permission denied" when executing scripts on Linux / macOS</b></summary>

**Cause:** Downloaded zip files from GitHub do not preserve execute permissions (`+x`).  
**Fix:**
Run with `bash setup.sh` and `bash run.sh`, or grant execution permissions:
```bash
chmod +x setup.sh run.sh
./setup.sh
```
</details>

<details>
<summary><b>4. How do I audit just ONE domain without creating files?</b></summary>

**Fix:**
Simply execute `.\run.bat` (Windows) or `bash run.sh` (Linux/macOS), select Option `[2] Single domain audit`, and type the domain name (e.g. `tesla.com`).
</details>

<details>
<summary><b>5. Where is the Excel report and how do I open it?</b></summary>

**Fix:**
Reports are saved inside the timestamped folder `./audit_YYYYMMDD_HHMMSS/`.  
When the scan completes, the interactive runner will ask if you want to open the Excel report immediately (`[y/N]`).
</details>

---

# 🇪🇸 Documentación en Español

## 📋 Resumen Ejecutivo

**Email DNS Audit Neon** es un escáner de seguridad asíncrono y de alto rendimiento diseñado para **CISOs, Auditores de Seguridad, Ingenieros SOC y Administradores de Sistemas**. Ejecuta evaluaciones técnicas profundas de autenticación de correo y postura DNS para uno o cientos de dominios, generando un **reporte unificado en Excel (`.xlsx`)** con formato condicional, hallazgos clasificados por severidad y evidencias DNS/SSL con marca temporal.

### Controles de Seguridad Evaluados

| Control | Alcance Evaluado |
|---|---|
| **WHOIS y RDAP** | Registrar, fechas de alta/expiración, estado del dominio, flag DNSSEC en WHOIS |
| **NS y SOA** | Servidores DNS autoritativos, serial SOA, proveedor DNS detectado (Cloudflare, Route53, etc.) |
| **DNSSEC** | Publicación de DNSKEY, DS en zona padre, validación del bit AD multi-resolver (Cloudflare, Google, Quad9) |
| **SPF (RFC 7208)** | Registro completo, directiva `all` (`-all`, `~all`, `+all`, `?all`), límite de 10 lookups, void lookups, consolidación de remitentes |
| **DKIM (RFC 6376)** | Selectores balanceados (~55) y profundos (~166), longitud de llave en bits, algoritmo, flag `t=y` |
| **DMARC (RFC 7489)** | Política `p` (`none`, `quarantine`, `reject`), política `sp`, alineación (`aspf`, `adkim`), buzones `rua`/`ruf`, porcentaje `pct` |
| **MX y Gateway** | Servidores de correo entrante y proveedor (Google Workspace, M365, Mimecast, Proofpoint, etc.) |
| **MTA-STS (RFC 8461)** | Registro TXT, `max_age`, modo de cifrado, verificación HTTPS de `/.well-known/mta-sts.txt` |
| **TLS-RPT (RFC 8460)** | Registro TXT `_smtp._tls`, destino de reportes `rua` |
| **BIMI** | Registro `default._bimi`, URI de SVG y validación del certificado VMC (X.509) |
| **CAA y Salud TLS** | CAs autorizadas (issue/issuewild), alertas de incidentes (`iodef`), FCrDNS (PTR ↔ A) y expiración de certificados SSL |

---

## ⚡ Instalación y Uso Rápido Multiplataforma

### Requisitos Previos
- **Python 3.10+** (Descargar de [python.org](https://www.python.org/downloads/) — *Asegúrate de marcar "Add python.exe to PATH"*).
- Compatible con: **Windows 10/11**, **Linux** (Kali, Ubuntu, Debian, Arch, Fedora) y **macOS** (10.15+).

---

### 🪟 Windows (Sin Fricción / Principiantes)

#### Opción A: Doble Clic (Recomendado para novatos)
1. Descarga o clona este repositorio en tu equipo.
2. **Haz doble clic en `setup.bat`** para crear el entorno virtual e instalar las dependencias automáticamente.
3. **Haz doble clic en `run.bat`** para iniciar el escáner interactivo.

#### Opción B: Windows PowerShell
Abre **PowerShell** en la carpeta del proyecto:
```powershell
# 1. Permitir ejecución de scripts en la sesión actual
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 2. Ejecutar instalador automatizado
.\setup.ps1

# 3. Lanzar ejecutor interactivo
.\run.ps1
```

---

### 🐧 Linux y 🍎 macOS (Bash / Zsh)

#### 1. Instalación
```bash
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit

# Ejecutar el instalador (funciona directo con bash)
bash setup.sh
```

#### 2. Ejecutar Auditoría
```bash
# Ejecutor interactivo (Pregunta idioma de consola, Excel y objetivo):
bash run.sh

# Escaneo directo de un solo dominio en Español:
bash run.sh google.com normal 30 es

# Escaneo de lista completa en Español:
bash run.sh servers.txt normal 30 es
```

---

## ❓ Preguntas Frecuentes y Solución de Problemas (FAQ)

<details>
<summary><b>1. "Python no se reconoce como un comando interno o externo" (Windows)</b></summary>

**Causa:** Python no está instalado o no se marcó la casilla de PATH durante la instalación.  
**Solución:**
1. Descarga Python 3.10+ desde [python.org/downloads](https://www.python.org/downloads/).
2. Ejecuta el instalador y **marca la casilla: "Add python.exe to PATH"** en la primera pantalla.
3. Haz clic en "Install Now", cierra todas las ventanas de consola y vuelve a hacer doble clic en `setup.bat`.
</details>

<details>
<summary><b>2. "La ejecución de scripts está deshabilitada en este sistema" (PowerShell)</b></summary>

**Causa:** Windows bloquea por defecto la ejecución de scripts `.ps1` sin firmar.  
**Solución:**
- Haz doble clic directamente en **`setup.bat`** y **`run.bat`** (ejecutan el bypass de forma segura y transparente).  
- O en PowerShell ejecuta: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` antes de correr `.\setup.ps1`.
</details>

<details>
<summary><b>3. "Permiso denegado" / "Permission denied" en Linux o macOS</b></summary>

**Causa:** Si descargaste el archivo `.zip` de GitHub, los archivos `.sh` no tienen permisos de ejecución.  
**Solución:**
Ejecuta directamente con `bash setup.sh` y `bash run.sh`, o asigna permisos con:
```bash
chmod +x setup.sh run.sh
./setup.sh
```
</details>

<details>
<summary><b>4. ¿Cómo audito UN SOLO dominio sin tener que editar archivos?</b></summary>

**Solución:**
Ejecuta `.\run.bat` (Windows) o `bash run.sh` (Linux/macOS), elige la opción `[2] Auditar un solo dominio` e introduce el dominio (ej. `miempresa.com`).
</details>

<details>
<summary><b>5. ¿Dónde está mi reporte Excel y cómo lo abro?</b></summary>

**Solución:**
Los reportes se guardan en la carpeta `./audit_YYYYMMDD_HHMMSS/`. Al terminar la auditoría, el programa te preguntará si deseas abrir el reporte Excel automáticamente (`[s/N]`).
</details>

---

## 🛡️ Estándares y Marcos de Cumplimiento

Esta herramienta está alineada a los principales marcos internacionales de ciberseguridad:
- **ISO/IEC 27001:2022:** Controles A.5.14, A.8.20, A.8.21, A.8.23.
- **NIST CSF 2.0:** Categorías PR.DS y PR.AA.
- **NIST SP 800-177 Rev.1:** Trustworthy Email Guidelines.
- **M3AAWG:** Email Authentication Best Common Practices.
- **RFCs:** 7208 (SPF), 6376 (DKIM), 7489 (DMARC), 8460 (TLS-RPT), 8461 (MTA-STS), 8659 (CAA).

---

## 🏛️ Metodología y Documentación SDD (Gentle-AI)

Este repositorio sigue la metodología **Spec-Driven Development (SDD)** del ecosistema Gentle-AI con arquitectura de **2 Zonas**:

- **Zona 1 (Rastreada en Git — Viaja con el repositorio):**
  - [`Antigravity.md`](Antigravity.md): Reglas de disciplina, perfil CISO y directivas de ingeniería.
  - [`HANDOFF.md`](HANDOFF.md): Estado exacto del proyecto y siguientes pasos.
  - [`CHANGELOG.md`](CHANGELOG.md): Historial de versiones bajo Conventional Commits.
  - [`DEVLOG.md`](DEVLOG.md): Registro de Decisiones de Arquitectura (ADRs).
- **Zona 2 (Memoria Local — Ignorada en Git):**
  - `MEMORY.md` y directorio `memory/` (Contexto local de la máquina).

---

## 👨‍💻 Autor y Licencia

- **Autor:** Eduardo Recinos (VCISO)
- **Repositorio:** [github.com/Drakk90/email-dns-audit](https://github.com/Drakk90/email-dns-audit)
- **Licencia:** MIT License
