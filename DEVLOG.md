# DEVLOG — Decisiones de Diseño y Arquitectura

## Registro de Decisiones de Arquitectura (ADR)

### ADR-001: Estrategia de Documentación en 2 Zonas (Git vs Local)
- **Fecha:** 2026-09-01
- **Contexto:** El proyecto se desarrolla en múltiples máquinas (Linux / macOS MacBook). Se requiere que el contexto de ingeniería viaje con el repositorio sin exponer rutas locales absolutas ni depender de cachés de una sola máquina.
- **Decisión:**
  - **Zona 1 (Git Tracked):** `Antigravity.md`, `HANDOFF.md`, `CHANGELOG.md`, `DEVLOG.md` viajan con `git clone / git pull`.
  - **Zona 2 (Local Memory):** `MEMORY.md` y `memory/` quedan ignorados en `.gitignore` para conveniencia local sin contaminar el repositorio remoto.
- **Consecuencias:** Cualquier agente o desarrollador que clone el repositorio en otra máquina puede retomar inmediatamente leyendo `Antigravity.md` → `HANDOFF.md` → `DEVLOG.md`.

### ADR-002: Internacionalización (i18n) Bilingüe (EN/ES)
- **Fecha:** 2026-09-01
- **Contexto:** La herramienta genera reportes técnicos y ejecutivos que se entregan tanto a equipos de habla hispana como angloparlantes (CISO / SOC / Infraestructura).
- **Decisión:** Centralizar todas las etiquetas, severidades, estados, glosarios y nombres de hojas de cálculo de Excel en un catálogo de traducción estructurado `i18n` seleccionable por flag `--lang [es|en]`.

---

## ADR-003: Integración de Motor Dual RDAP / WHOIS para Inventario de Activos
- **Fecha:** 2026-09-01
- **Estado:** Aceptado
- **Contexto:** Las consultas WHOIS tradicionales por puerto 43 TCP sufren bloqueos de firewall y timeouts constantes en redes corporativas, dejando vacíos o como `N/D` los campos de Registrar, Expiración y Marca en la hoja de inventario.
- **Decisión:** Implementar consultas asíncronas a RDAP (Registration Data Access Protocol) sobre HTTPS estándar (puerto 443) con `httpx`, extrayendo eventos de expiración, entidades registradoras y entidad registrante (Brand), con fallback asíncrono a WHOIS y guardado de evidencias forenses en `rdap.json`.
- **Consecuencias:** Tiempos de respuesta reducidos de 30s a <10s por lote, 100% de confiabilidad frente a firewalls, y población completa de la hoja `Inventario_Dominios` / `Domain_Inventory`.
