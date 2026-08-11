# 🛡️ Email DNS Audit Neon

> Auditoría automatizada de autenticación de correo electrónico — **SPF · DKIM · DMARC · DNSSEC · MTA-STS · TLS-RPT · BIMI**
> Genera un **Excel unificado** listo para entregar a Dirección, con hallazgos, severidades y evidencia trazable.

**Autor:** Eduardo Recinos · CISO
**Versión:** 3.2
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
- [Preparar la lista de dominios](#-preparar-la-lista-de-dominios)
- [▶️ Ejecutar la auditoría](#️-ejecutar-la-auditoría)
- [🔎 Modo DKIM profundo (--deep-dkim)](#-modo-dkim-profundo---deep-dkim)
- [🔐 Validación DNSSEC multi-resolver](#-validación-dnssec-multi-resolver)
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
| **DNSSEC** | DNSKEY, DS, bit AD validado contra **múltiples resolvers** |
| **SPF** | Registro, mecanismo `all`, DNS lookups, void lookups, proveedores |
| **DKIM** | ~55 selectores comunes (o ~166 en modo profundo), algoritmo, tamaño de llave |
| **DMARC** | Política `p`/`sp`, `pct`, alineación, `rua`/`ruf`, `fo` |
| **MX** | Proveedor de correo detectado |
| **MTA-STS** | Política publicada, `max_age`, accesibilidad HTTPS |
| **TLS-RPT** | Registro de reportes de fallas TLS |
| **BIMI** | Registro, SVG, certificado VMC (descarga y parseo X.509) |

**Salida principal:** un archivo Excel (`.xlsx`) con múltiples hojas pre-formateadas, formato condicional (verde/amarillo/rojo) y listas desplegables. Además genera CSVs de respaldo y una carpeta de evidencias con marca temporal.

> ⚡ **Rendimiento:** cada dominio tarda **menos de 30 segundos** en modo balanceado gracias a las consultas asíncronas. Dominios como `google.com` o `tesla.com` se auditan por completo en ese rango.

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

> ✅ **Buena noticia:** tanto `setup.sh` como `run.sh` **detectan tu sistema y shell** automáticamente.

---

## 🔄 Flujo de uso: instalar una vez, ejecutar siempre

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

> ⚠️ **No vuelvas a correr `setup.sh` cada vez.** Las dependencias quedan guardadas **permanentemente** dentro del entorno `venv-email-audit`. Para el uso diario usa `run.sh`.

---

## ⚡ Instalación rápida (recomendada)

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

> ✅ El instalador es **idempotente**: puedes ejecutarlo varias veces sin romper nada.

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

### Ruta A — Ubuntu / Pop!_OS / Kali / Debian (Bash + apt)

```bash
# A.1 — Python y dependencias del sistema
python3 --version
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# A.2 — Descargar el proyecto
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit

# A.3 — Crear el entorno virtual
python3 -m venv venv-email-audit

# A.4 — Activar el entorno (Bash)
source venv-email-audit/bin/activate

# A.5 — Instalar dependencias
pip install -r requirements.txt

# A.6 — Verificar
python -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl; print('✅ Dependencias OK')"
```

> ⚠️ **Importante:** `python3-venv` es **obligatorio**. Si tu Python es específico (ej. 3.11), instala también `sudo apt install -y python3.11-venv`.

### Ruta B — CachyOS / Arch / Manjaro (Fish + pacman)

```bash
# B.1 — Instalar Python
python --version
sudo pacman -S --needed python python-pip

# B.2 — Descargar el proyecto
git clone https://github.com/Drakk90/email-dns-audit.git
cd email-dns-audit

# B.3 — Crear el entorno virtual
python -m venv venv-email-audit

# B.4 — Activar el entorno (Fish)  ⚠️ nota la extension .fish
source venv-email-audit/bin/activate.fish

# B.5 — Instalar dependencias
pip install -r requirements.txt

# B.6 — Verificar
python -c "import rich, dns.resolver, cryptography, httpx, whois, aiodns, openpyxl; print('✅ Dependencias OK')"
```

---

## 📝 Preparar la lista de dominios

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

### 🚀 Opción 1 — Con `run.sh` (recomendada)

El `run.sh` verifica que todo esté listo y ejecuta la auditoría **sin que tengas que activar el entorno manualmente**. Funciona igual en Bash y en Fish.

```bash
# servers.txt · modo DKIM balanceado (default)
./run.sh

# archivo indicado · balanceado
./run.sh servers.txt

# archivo indicado · modo DKIM PROFUNDO
./run.sh servers.txt deep

# DKIM profundo con 48 meses de selectores rotativos
./run.sh servers.txt deep 48
```

| Argumento | Posición | Valores | Default |
|---|---|---|---|
| Archivo de dominios | `$1` | ruta a un `.txt` | `servers.txt` |
| Modo DKIM | `$2` | `normal` \| `deep` | `normal` |
| Meses rotativos (solo deep) | `$3` | número | `30` |

### 🔧 Opción 2 — Activando el entorno manualmente (aconsejable)

> 💡 **Recomendación:** para auditorías puntuales o de diagnóstico, es **aconsejable ejecutar de forma manual** con el entorno activado. Te da control total sobre las opciones (resolver, selectores, salida) y permite ver el detalle de cada control en pantalla. Cada dominio tarda **menos de 30 segundos**, así que auditar unos pocos dominios es cuestión de segundos.

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
| `--deep-dkim` | Activa búsqueda DKIM profunda (~166 selectores) | `--deep-dkim` |
| `--deep-months` | Meses rotativos para modo profundo | `--deep-months 48` |
| `--resolver`, `-r` | Resolver DNS general (por defecto `1.1.1.1`) | `-r 8.8.8.8` |
| `--dnssec-resolvers` | Resolvers validadores DNSSEC (coma) | `--dnssec-resolvers 1.1.1.1,8.8.8.8` |
| `--output`, `-o` | Carpeta de salida | `-o ~/auditorias/Q2` |
| `--excel-name` | Nombre del Excel | `--excel-name Audit_2026.xlsx` |
| `--help`, `-h` | Muestra la ayuda | `-h` |

---

## 🔎 Modo DKIM profundo (`--deep-dkim`)

DKIM tiene una limitación de diseño: **no es enumerable**. Cada dominio usa un *selector* arbitrario y no existe forma de listar todos los selectores vía DNS. Por eso la herramienta prueba una lista de selectores conocidos.

| Modo | Selectores probados | Velocidad | Cuándo usarlo |
|---|---|---|---|
| **Balanceado** (default) | ~55 comunes | Rápido | Auditoría rutinaria |
| **Profundo** (`--deep-dkim`) | ~166 (incluye rotativos por fecha) | Más lento | Dominios grandes con selectores custom o rotativos |

El modo profundo añade selectores rotativos por fecha (patrón `YYYYMMDD`) usados por **Google, Amazon SES, SparkPost, Postmark** y muchos otros, además de decenas de proveedores adicionales (Marketo, Pardot, Brevo, Campaign Monitor, etc.).

```bash
# Manual
python email_dns_audit_neon.py --domains servers.txt --deep-dkim

# Con run.sh
./run.sh servers.txt deep
```

> 💡 **Si un dominio muestra "DKIM: No detectado"** no significa que carezca de DKIM: probablemente usa un selector fuera de la lista. Reintenta con `--deep-dkim`, o lee el header `DKIM-Signature: s=...` de un correo real y pásalo con `--selectors`.

---

## 🔐 Validación DNSSEC multi-resolver

El bit **AD** (Authenticated Data) que confirma la validación DNSSEC **depende del resolver** que responde. Para evitar falsos negativos por un resolver o red específicos, la herramienta prueba **internamente** contra varios resolvers validadores en una sola pasada:

- **Cloudflare** (1.1.1.1)
- **Google** (8.8.8.8)
- **Quad9** (9.9.9.9)

Si **cualquiera** confirma el bit AD, el dominio se marca como **Secure**. Todo ocurre en una sola ejecución, generando **una sola carpeta de salida** (sin duplicidad).

```bash
# Personalizar los resolvers validadores
python email_dns_audit_neon.py --domains servers.txt --dnssec-resolvers "1.1.1.1,8.8.8.8"
```

> ℹ️ **Dato importante:** algunos gigantes tecnológicos (Google, Amazon, Microsoft) **NO firman sus dominios principales con DNSSEC** por decisión deliberada (riesgo de amplificación DDoS y consideraciones operativas a su escala). Por eso `google.com` puede aparecer como "DNSSEC: No implementado" — y es correcto. Tu perfil de riesgo probablemente sí justifica implementarlo.

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
        ├── dnssec_validation.txt                  ← volcado de los 3 resolvers
        └── ... (cada consulta con timestamp ISO 8601)
```

### Hojas del Excel unificado

| Hoja | Contenido |
|---|---|
| **Portada** | Metadata, marco normativo, convenciones, modo DKIM usado |
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

**Solución:**

```bash
source venv-email-audit/bin/activate    # o activate.fish en Fish
pip list | grep -Ei "rich|dnspython|cryptography|httpx|whois|aiodns|openpyxl"
deactivate
```

- **Si aparecen las 7 librerías:** el entorno está bien. Usa `./run.sh` de aquí en adelante.
- **Si NO aparecen:** corre `./setup.sh` **una última vez**. Quedará permanente.

### ❌ "DKIM: No detectado" en un dominio que sí tiene DKIM

**Causa:** el dominio usa un selector fuera de la lista balanceada.

**Solución:** reintenta con el modo profundo o pasa el selector real:

```bash
./run.sh servers.txt deep
# o, si conoces el selector real (del header DKIM-Signature):
python email_dns_audit_neon.py --domains servers.txt --selectors "20240115 nombreselector"
```

### ❌ `error: externally-managed-environment`

**Causa:** intentaste instalar con `pip` sin activar el entorno virtual (PEP 668).

**Solución:**

```bash
source venv-email-audit/bin/activate     # Bash
source venv-email-audit/bin/activate.fish # Fish
pip install -r requirements.txt
```

### ❌ `No se encontró pip en el entorno virtual` (Ubuntu/Pop!_OS/Kali)

```bash
sudo apt install -y python3-venv python3-pip
rm -rf venv-email-audit
./setup.sh
```

### ❌ `"case" builtin not inside of switch block` (CachyOS/Arch)

**Causa:** usas Fish y ejecutaste el script de activación de Bash.

```fish
source venv-email-audit/bin/activate.fish
```

### ❌ `Permission denied` al ejecutar `./setup.sh` o `./run.sh`

```bash
chmod +x setup.sh run.sh
```

### ❌ `requirements.txt` con `&gt;` o `&lt;`

```bash
sed -i 's/&gt;/>/g; s/&lt;/</g; s/&amp;/\&/g' requirements.txt
```

### ⚠️ WHOIS devuelve `N/D` para dominios `.gt`, `.cr`, etc.

**Causa:** algunos ccTLD no exponen datos completos vía WHOIS. Es normal; verifícalos en el panel de tu registrar.

---

## ❓ Preguntas frecuentes

**¿Cuándo uso `setup.sh` y cuándo `run.sh`?**
`setup.sh` una sola vez para instalar. `run.sh` cada vez que auditas.

**¿Conviene ejecutar manualmente o con `run.sh`?**
Para auditorías rutinarias, `run.sh` es lo más simple. Para diagnóstico puntual o para usar opciones avanzadas (resolver, selectores, deep-dkim), es **aconsejable la ejecución manual** con el entorno activado. Cada dominio tarda menos de 30 segundos.

**¿El `run.sh` funciona en Fish y en Bash?**
Sí. Usa el Python del entorno directamente, así que no depende de tu shell.

**¿Por qué google.com sale sin DNSSEC/BIMI si es líder en seguridad?**
Es correcto. Google no firma sus dominios principales con DNSSEC por decisión deliberada (riesgo de amplificación DDoS a su escala), y no publica BIMI en `google.com` porque no envía correo comercial masivo desde el dominio raíz. La ausencia de un control puede ser una decisión de gestión de riesgo, no un error.

**¿Cuánto tarda?**
Menos de 30 segundos por dominio en modo balanceado. El modo `--deep-dkim` es más lento por probar ~166 selectores.

**¿Modifica algo en mis dominios o DNS?**
No. La herramienta **solo lee** (consultas DNS y HTTP públicas). Nunca escribe.

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
