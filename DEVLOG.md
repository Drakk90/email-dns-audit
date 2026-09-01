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
