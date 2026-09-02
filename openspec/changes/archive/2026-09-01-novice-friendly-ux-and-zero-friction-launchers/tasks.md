# Tasks: Novice-Friendly UX and Zero-Friction Launchers

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~220 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR (Novice UX & Launchers) |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Double-Click Batch Launchers | PR 1 | `bash setup.bat` check | `setup.bat`, `run.bat` | `setup.bat`, `run.bat` |
| 2 | Interactive Single-Domain & Auto-Open Report | PR 1 | `bash run.sh` / `pwsh run.ps1` | `run.sh`, `run.ps1` | `run.sh`, `run.ps1` |
| 3 | Bilingual Troubleshooting FAQ in `README.md` | PR 1 | Markdown preview | `README.md` | `README.md` |

## Phase 1: Windows Batch Launchers & Store Alias Diagnostics

- [x] 1.1 Create `setup.bat` to launch `setup.ps1` with `-ExecutionPolicy Bypass`.
- [x] 1.2 Create `run.bat` to launch `run.ps1` with `-ExecutionPolicy Bypass` forwarding all parameters.
- [x] 1.3 In `setup.ps1`, detect if `python.exe` is a non-functioning WindowsApps execution alias and provide explicit python.org installation guidance.

## Phase 2: Interactive Single-Domain & Auto-Open Excel Report

- [x] 2.1 Update `run.sh` to prompt the user: `[1] Auditar servidores desde archivo servers.txt` or `[2] Auditar un solo dominio directamente`.
- [x] 2.2 Update `run.sh` to offer opening the generated Excel file with `xdg-open` (Linux) or `open` (macOS).
- [x] 2.3 Update `run.ps1` to prompt for single domain or `servers.txt` list, and offer opening the Excel file with `Invoke-Item` / `start` (Windows).

## Phase 3: Comprehensive Bilingual Troubleshooting & FAQ Documentation

- [x] 3.1 Overhaul `README.md` English section with Quickstart for double-click batch files and an in-depth "Troubleshooting & FAQ" section.
- [x] 3.2 Overhaul `README.md` Spanish section with Quickstart for double-click batch files and an in-depth "Preguntas Frecuentes y Solución de Problemas" section.

## Phase 4: Automated Verification & Testing

- [x] 4.1 Validate syntax of `setup.bat`, `run.bat`, `setup.ps1`, `run.ps1`, `setup.sh`, and `run.sh`.
- [x] 4.2 Run unit test verifying script keywords and bilingual FAQ completeness.
