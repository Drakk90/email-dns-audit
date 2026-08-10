# 🛡️ Email DNS Audit Neon

> Auditoría automatizada de autenticación de correo electrónico — **SPF · DKIM · DMARC · DNSSEC · MTA-STS · TLS-RPT · BIMI**
> Genera un **Excel unificado** listo para entregar a Dirección, con hallazgos, severidades y evidencia trazable.

**Autor:** Eduardo Recinos · CISO
**Versión:** 3.0
**Licencia:** MIT
**Repositorio:** [github.com/Drakk90/email-dns-audit](https://github.com/Drakk90/email-dns-audit)
**Compatibilidad:** Kali Linux · Ubuntu 20.04+ · Debian 10+ · CachyOS / Arch

---

## 📋 Tabla de contenido

- [¿Qué hace esta herramienta?](#-qué-hace-esta-herramienta)
- [¿Para quién es?](#-para-quién-es)
- [Archivos del proyecto](#-archivos-del-proyecto)
- [⚡ Instalación rápida (recomendada)](#-instalación-rápida-recomendada)
- [🔧 Instalación manual (paso a paso)](#-instalación-manual-paso-a-paso)
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

## ⚡ Instalación rápida (recomendada)

Si tienes prisa, el script `setup.sh` hace **todo** por ti: verifica Python, crea el entorno virtual, instala las dependencias, valida y prepara tu `servers.txt`.

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
2. Verifica que los archivos del proyecto estén presentes.
3. Crea el entorno virtual **`venv-email-audit`**.
4. Instala todas las dependencias de `requirements.txt`.
5. Valida que cada librería se importe correctamente.
6. Crea tu `servers.txt` a partir de la plantilla si aún no existe.

Si prefieres entender cada paso o el instalador falla, usa la [instalación manual](#-instalación-manual-paso-a-paso).

---

## 🔧 Instalación manual (paso a paso)

Para quienes prefieren control total o están en un sistema donde el instalador automático no funciona.

### 1. Instalar Python

Verifica si lo tienes:

```bash
python3 --version
```

Si ves `Python 3.9` o superior, salta al paso 2. Si no:

**Ubuntu / Debian / Kali Linux:**

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

### 2. Descargar el proyecto

```bash
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit
```

### 3. Crear el entorno virtual

> 🏷️ **Nombre del entorno:** `venv-email-audit` — reconocible entre otros entornos de tu equipo.

```bash
python3 -m venv venv-email-audit
```

### 4. Activar el entorno virtual

**Bash / Zsh (Ubuntu, Kali, Debian):**

```bash
source venv-email-audit/bin/activate
```

**Fish shell (CachyOS y algunas configuraciones):**

```fish
source venv-email-audit/bin/activate.fish
```

> ✅ Verás `(venv-email-audit)` al inicio de tu prompt cuando esté activo.

### 5. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 6. Verificar la instalación

```bash
python -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl; print('✅ Dependencias OK')"
```

---

## 📝 Preparar la lista de dominios

Copia la plantilla y edítala con tus dominios reales:

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

Con el entorno activado y `servers.txt` preparado:

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

---

## 🔁 Uso recurrente

Una vez instalado, para futuras auditorías solo:

```bash
cd ~/email-dns-audit
source venv-email-audit/bin/activate      # o activate.fish en Fish
python email_dns_audit_neon.py --domains servers.txt
deactivate
```

### 💡 Atajo opcional (Bash)

```bash
echo "alias audit-email='cd ~/email-dns-audit && source venv-email-audit/bin/activate && python email_dns_audit_neon.py --domains servers.txt'" >> ~/.bashrc
source ~/.bashrc
```

Luego solo escribes `audit-email`.

---

## 🔧 Solución de problemas

### ❌ `error: externally-managed-environment`

**Causa:** intentaste instalar sin activar el entorno virtual.
**Solución:** activa el entorno antes de `pip install`:

```bash
source venv-email-audit/bin/activate
pip install -r requirements.txt
```

### ❌ `"case" builtin not inside of switch block`

**Causa:** usas Fish shell y ejecutaste el script de activación de Bash.
**Solución:** usa la versión `.fish`:

```fish
source venv-email-audit/bin/activate.fish
```

### ❌ `ModuleNotFoundError: No module named 'rich'`

**Causa:** el entorno no está activado o faltan dependencias.
**Solución:**

```bash
source venv-email-audit/bin/activate
pip install -r requirements.txt
```

### ❌ `Permission denied` al ejecutar `./setup.sh`

**Causa:** el script no tiene permisos de ejecución.
**Solución:**

```bash
chmod +x setup.sh
./setup.sh
```

### ❌ `requirements.txt` con `&gt;` o `&lt;`

**Causa:** entidades HTML por copy-paste desde una web.
**Solución:**

```bash
sed -i 's/&gt;/>/g; s/&lt;/</g; s/&amp;/\&/g' requirements.txt
```

### ⚠️ WHOIS devuelve `N/D` para dominios `.gt`, `.cr`, etc.

**Causa:** algunos ccTLD no exponen datos completos vía WHOIS.
**Solución:** es normal. Verifica esos datos en el panel de tu registrar.

---

## ❓ Preguntas frecuentes

**¿Necesito conocimientos de programación?**
No. Con `./setup.sh` y copiar/pegar comandos es suficiente.

**¿Modifica algo en mis dominios o DNS?**
No. La herramienta **solo lee** (consultas DNS y HTTP públicas). Nunca escribe.

**¿Cuánto tarda?**
~10-15 segundos por dominio gracias a consultas asíncronas.

**¿Puedo auditar dominios que no son míos?**
Técnicamente sí (solo datos públicos), pero **audita únicamente dominios propios o autorizados**.

**¿Puedo automatizarlo con cron?**
Sí. Recuerda activar el entorno virtual dentro del script de cron.

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
