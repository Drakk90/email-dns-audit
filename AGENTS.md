# Coding Standards & Architecture Rules — email-dns-audit

## General Principles
- Follow Spec-Driven Development (SDD) and Clean Architecture.
- Commit messages must follow Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`).
- Keep code clean, modular, and maintainable.

## Python & Internationalization
- Maintain Python 3.10+ compatibility.
- Use asynchronous operations (`async`/`await`) for network, HTTP, and DNS calls.
- Centralize bilingual translations (English & Spanish) in `i18n.py`.

## Git & Repository Discipline
- Maintain 2-Zone documentation:
  - Zona 1 (`Antigravity.md`, `HANDOFF.md`, `CHANGELOG.md`, `DEVLOG.md`, `README.md`) tracked in Git.
  - Zona 2 (`MEMORY.md`, `memory/`) kept local and untracked via `.gitignore`.
