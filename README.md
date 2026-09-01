# 🛡️ Email DNS Audit Neon (v3.3)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gentle-AI Ready](https://img.shields.io/badge/Ecosystem-Gentle--AI-purple.svg)](https://github.com/Gentleman-Programming/gentle-ai)

> **Bilingual Automated Email Authentication & DNS Security Auditor**  
> *Auditoría automatizada y bilingüe de autenticación de correo electrónico y seguridad DNS.*  
> **SPF · DKIM · DMARC · DNSSEC · MTA-STS · TLS-RPT · BIMI**

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
| **WHOIS** | Registrar identity, creation/expiration dates, domain status, WHOIS DNSSEC flag |
| **NS & SOA** | Authoritative Name Servers, SOA serial, detected DNS hosting provider (Cloudflare, Route53, etc.) |
| **DNSSEC** | DNSKEY publication, DS in parent zone, AD bit validation across **multi-resolvers** (Cloudflare, Google, Quad9) |
| **SPF (RFC 7208)** | Full record text, `all` mechanism enforcement (`-all`, `~all`, `+all`, `?all`), 10-lookup limit, void lookups, sender consolidation |
| **DKIM (RFC 6376)** | Common (~55) and deep rotated (~166) selectors, cryptographic key size (bits), algorithm, `t=y` test flag |
| **DMARC (RFC 7489)** | Policy status (`p=none`, `quarantine`, `reject`), subdomain policy (`sp`), alignment (`aspf`, `adkim`), `rua`/`ruf` mailboxes, percentage (`pct`) |
| **MX & Email Gateway** | Mail exchange routing and provider detection (Google Workspace, M365, Mimecast, Proofpoint, etc.) |
| **MTA-STS (RFC 8461)** | Policy publication, `max_age`, TLS enforcement mode, HTTPS `/.well-known/mta-sts.txt` policy fetch |
| **TLS-RPT (RFC 8460)** | TLS reporting TXT records (`_smtp._tls`), `rua` report destination |
| **BIMI** | Brand Indicators for Message Identification TXT record, SVG logo URI, VMC (Verified Mark Certificate) X.509 parsing |

---

## ⚡ Quickstart & Installation

### 1. Prerequisites (Linux)
- Python 3.10+ & `pip`
- Git

### 2. Setup (Run Once)
```bash
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit

# Run the installer to create the virtual environment and install dependencies
chmod +x setup.sh run.sh
./setup.sh
```

### 3. Prepare Target Domains
Create your `servers.txt` file (one domain per line):
```bash
cp servers.example.txt servers.txt
nano servers.txt
```

### 4. Run the Audit
```bash
# Standard Balanced Run (Spanish Default)
./run.sh

# Standard Balanced Run in English
./run.sh servers.txt normal 30 en

# Deep DKIM Discovery in English (30 months date-rotated selectors)
./run.sh servers.txt deep 30 en
```

---

## 💻 CLI Usage & Arguments

You can also run the Python engine directly using the virtual environment:

```bash
./venv-email-audit/bin/python email_dns_audit_neon.py --domains servers.txt --lang en
```

### Parameters Reference

| Flag | Short | Default | Description |
|---|---|---|---|
| `--domains` | `-d` | *Required* | File path containing domain list (one per line). |
| `--lang` | `-l` | `es` | Language for terminal output and Excel report (`es` or `en`). |
| `--deep-dkim` | | `False` | Enables exhaustive DKIM selector discovery (adds ~110 date-rotated and vendor selectors). |
| `--deep-months` | | `30` | Months to look back when generating date-based selectors (e.g. `20240101`, `202401`). |
| `--selectors` | `-s` | `""` | Extra custom DKIM selectors separated by space or comma. |
| `--resolver` | `-r` | `1.1.1.1` | Primary DNS resolver IP for queries. |
| `--dnssec-resolvers` | | `1.1.1.1,8.8.8.8,9.9.9.9` | Comma-separated resolver IPs used to validate the DNSSEC AD bit. |
| `--output` | `-o` | `./audit_YYYYMMDD_HHMMSS` | Target directory for outputs and evidence logs. |
| `--excel-name` | | `Auditoria_Email_...xlsx` | Custom name for the generated Excel workbook. |

---

## 📊 Generated Artifacts & Deliverables

Each audit run produces a dedicated output directory containing:
1. **Unified Excel Report (`.xlsx`):** Pre-formatted workbook with Cover, Inventory, SPF Details, DKIM Details, DMARC Details, DNSSEC & DANE, MTA-STS & TLS, Authorized Senders, and Findings Sheet.
2. **Evidence Logs (`evidencias/<domain>/`):** Raw output of all DNS queries (`dig_txt.txt`, `dig_dnskey.txt`, `dig_ds.txt`, `whois.txt`, `mtasts_policy.txt`).

---

# 🇪🇸 Documentación en Español

## 📋 Resumen Ejecutivo

**Email DNS Audit Neon** es un escáner de seguridad asíncrono y de alto rendimiento diseñado para **CISOs, Auditores de Seguridad, Ingenieros SOC y Administradores de Sistemas**. Ejecuta evaluaciones técnicas profundas de autenticación de correo y postura DNS para uno o cientos de dominios, generando un **reporte unificado en Excel (`.xlsx`)** con formato condicional, hallazgos clasificados por severidad y evidencias DNS/SSL con marca temporal.

### Controles de Seguridad Evaluados

| Control | Alcance Evaluado |
|---|---|
| **WHOIS** | Registrar, fechas de alta/expiración, estado del dominio, flag DNSSEC en WHOIS |
| **NS y SOA** | Servidores DNS autoritativos, serial SOA, proveedor DNS detectado (Cloudflare, Route53, etc.) |
| **DNSSEC** | Publicación de DNSKEY, DS en zona padre, validación del bit AD multi-resolver (Cloudflare, Google, Quad9) |
| **SPF (RFC 7208)** | Registro completo, directiva `all` (`-all`, `~all`, `+all`, `?all`), límite de 10 lookups, void lookups, consolidación de remitentes |
| **DKIM (RFC 6376)** | Selectores balanceados (~55) y profundos (~166), longitud de llave en bits, algoritmo, flag `t=y` |
| **DMARC (RFC 7489)** | Política `p` (`none`, `quarantine`, `reject`), política `sp`, alineación (`aspf`, `adkim`), buzones `rua`/`ruf`, porcentaje `pct` |
| **MX y Gateway** | Servidores de correo entrante y proveedor (Google Workspace, M365, Mimecast, Proofpoint, etc.) |
| **MTA-STS (RFC 8461)** | Registro TXT, `max_age`, modo de cifrado, verificación HTTPS de `/.well-known/mta-sts.txt` |
| **TLS-RPT (RFC 8460)** | Registro TXT `_smtp._tls`, destino de reportes `rua` |
| **BIMI** | Registro `default._bimi`, URI de SVG y validación del certificado VMC (X.509) |

---

## ⚡ Instalación y Uso Rápido

### 1. Requisitos (Linux)
- Python 3.10+ y `pip`
- Git

### 2. Instalación (Se ejecuta UNA sola vez)
```bash
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit

chmod +x setup.sh run.sh
./setup.sh
```

### 3. Configurar Dominios a Auditar
```bash
cp servers.example.txt servers.txt
nano servers.txt
```

### 4. Ejecutar Auditoría
```bash
# Modo Balanceado por defecto (Español)
./run.sh

# Modo Balanceado en Inglés
./run.sh servers.txt normal 30 en

# Modo DKIM Profundo en Español (30 meses de rotación)
./run.sh servers.txt deep 30 es
```

---

## 🛡️ Estándares y Marcos de Cumplimiento

Esta herramienta está alineada a los principales marcos internacionales de ciberseguridad:
- **ISO/IEC 27001:2022:** Controles A.5.14, A.8.20, A.8.21, A.8.23.
- **NIST CSF 2.0:** Categorías PR.DS y PR.AA.
- **NIST SP 800-177 Rev.1:** Trustworthy Email Guidelines.
- **M3AAWG:** Email Authentication Best Common Practices.
- **RFCs:** 7208 (SPF), 6376 (DKIM), 7489 (DMARC), 8460 (TLS-RPT), 8461 (MTA-STS).

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
