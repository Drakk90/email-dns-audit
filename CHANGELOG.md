# Changelog — email-dns-audit

Todos los cambios notables en este proyecto se documentan en este archivo siguiendo [Conventional Commits](https://www.conventionalcommits.org/).

## [3.3.0] - 2026-09-01
### Added
- Integración de motor RDAP (RFC 7480-7484 / RFC 9082-9083) sobre HTTPS (puerto 443) con fallback a WHOIS socket.
- Extracción automática de Registrar, Fecha de Expiración, Creación, y Entidad Registrante (Brand/Entity).
- Inferencia inteligente de Marca y asignación de Propietario Interno (`Seguridad / TI` / `Security / IT`) en inventario.
- Selector interactivo de idioma en `run.sh` al iniciar la ejecución.
- Soporte de internacionalización (i18n) completo: flag `--lang [es|en]` para CLI, tablas Rich y reporte Excel.
- Documentación bilingüe integral en `README.md` (English / Español).
- Estructura de versionado y trazabilidad SDD (Zona 1: `Antigravity.md`, `HANDOFF.md`, `CHANGELOG.md`, `DEVLOG.md`).
- Zona 2 de memoria local (`MEMORY.md`, `memory/`).

## [3.2.0] - 2026-06-30
### Added
- DKIM: lista balanceada (~50 selectores comunes) por defecto.
- Nuevo flag `--deep-dkim`: búsqueda exhaustiva con selectores rotativos por fecha (Google, Microsoft, Amazon SES, SparkPost, etc.).
- DKIM: mensaje diferenciado "Sin DKIM" vs "No detectado (selector no común)".
- DNSSEC: multi-resolver interno con salida unificada.
