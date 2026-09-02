# Archive Report: Cross-Platform Installers for Windows PowerShell and macOS

## Change Information
- **Change ID**: `cross-platform-installers-windows-macos`
- **Archive Date**: 2026-09-01
- **Status**: Completed & Archived
- **Target Repository**: `/home/erecinos/Downloads/email-dns-audit/`

## Synced Capabilities (Source of Truth)
The following capability specification has been promoted to `openspec/specs/`:
1. `openspec/specs/cross-platform-installers/spec.md` (Native Windows PowerShell, macOS Homebrew, and Multi-Platform Bilingual Documentation)

## Summary of Shipped Artifacts
- **Native Windows PowerShell Suite (`setup.ps1` & `run.ps1`)**:
  - `setup.ps1`: Python 3.10+ verification, virtual environment initialization (`venv-email-audit`), pip upgrade, `requirements.txt` installation, and `servers.txt` creation.
  - `run.ps1`: Interactive bilingual language selection prompt (`[1] Español`, `[2] English`), DKIM discovery modes, DNSSEC resolvers, and direct CLI support.
- **macOS / Homebrew Integration (`setup.sh`)**:
  - Added OS and Homebrew detection to bypass Linux package managers on macOS systems.
- **Bilingual Multi-Platform Documentation (`README.md`)**:
  - Added dedicated installation and execution instructions for Linux, macOS, and Windows PowerShell in English and Spanish.

## Verification Evidence
- **Automated Tests**: 3/3 passing validation tests covering file existence, keyword syntax, and bilingual README consistency.
- **Syntax Validation**: Bash syntax check passed with code 0 on `setup.sh` and `run.sh`.
- **Mechanical Readback**: `diff -r` verified with exit code 0.
