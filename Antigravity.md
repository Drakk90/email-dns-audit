# Antigravity — Reglas de Flujo y Disciplina

## Perfil del Proyecto
- **Proyecto:** `email-dns-audit` (Auditoría DNS / Autenticación de Correo: SPF, DMARC, DKIM, MTA-STS, TLS-RPT, DNSSEC, DANE, Certificados, WHOIS).
- **Autor / CISO:** Eduardo Recinos (VCISO).
- **Visibilidad:** Repositorio Privado (`https://github.com/Drakk90/email-dns-audit`).
- **Idiomas:** Bilingüe (Español / Inglés). Respuestas concisas, directas y con rigor de ingeniería.

## Disciplina y Metodología (Gentle-AI + SDD)
1. **Spec-Driven Development (SDD):**
   - No escribir código apresurado ni realizar "vibecoding".
   - Flujo: `Spec / Discovery` → `Proposal & Plan` → `Tasks / Implementation` → `Verification` → `Handoff / Changelog`.
2. **Estructura de Documentación Durable (Zona 1 — Rastreada en Git):**
   - `Antigravity.md`: Reglas de flujo, perfil y contexto de ingeniería.
   - `HANDOFF.md`: Estado actual exacto y próximo paso accionable.
   - `CHANGELOG.md`: Registro formal de cambios por versión (Conventional Commits).
   - `DEVLOG.md`: Razón técnica y arquitectónica de cada decisión de diseño.
3. **Calidad y Commits:**
   - Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`).
   - Validación con Gentleman Guardian Angel (`gga`) en pre-commit.
   - Tests unitarios para validar lógica de parsing DNS y seguridad.
