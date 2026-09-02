# Proposal: Cross-Platform Installers for Windows PowerShell and macOS

## Intent

Deliver first-class native installation, execution, and documentation support for Windows (PowerShell) and macOS (Homebrew/Zsh), eliminating OS barriers while preserving the standalone, zero-paid-API design.

## Scope

### In Scope
- **Native Windows PowerShell Suite**:
  - `setup.ps1`: Automated installer validating Python 3.10+, initializing `venv-email-audit`, upgrading pip, installing `requirements.txt`, and seeding `servers.txt`.
  - `run.ps1`: Interactive runner supporting language selection (ES/EN), DKIM discovery modes, and direct command-line arguments in PowerShell.
- **macOS Compatibility in Unix Scripts**:
  - Update `setup.sh` to detect macOS (`darwin`) and Homebrew (`brew`), ensuring smooth virtual environment setup on macOS without Linux package manager errors.
- **Bilingual Documentation Overhaul**:
  - Update `README.md` (both English and Spanish sections) with distinct installation and execution instructions for Linux, macOS, and Windows.

### Out of Scope
- Creating compiled binary executables (.exe / .app) or introducing GUI installers.

## Capabilities

### Modified Capabilities
- `cross-platform-installers`: Adds native PowerShell installation (`setup.ps1`), execution (`run.ps1`), macOS Homebrew detection in `setup.sh`, and multi-platform quickstart guides in `README.md`.

## Approach

1. Implement `setup.ps1` with robust error handling, execution policy awareness, and pip bootstrapping.
2. Implement `run.ps1` with interactive prompts matching `run.sh` behavior.
3. Update `setup.sh` to detect `uname -s == Darwin` and utilize `brew` if Python/venv is missing.
4. Update `README.md` to document Linux, macOS, and Windows commands clearly.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `setup.ps1` | New | Native PowerShell installer for Windows |
| `run.ps1` | New | Native PowerShell runner for Windows |
| `setup.sh` | Modified | Add macOS and Homebrew platform detection |
| `README.md` | Modified | Add Windows (PowerShell) & macOS setup guides |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| PowerShell execution policy restrictions (`Restricted`) | Medium | Document `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in README |

## Rollback Plan

Delete new `.ps1` files and revert `setup.sh` and `README.md` via git.

## Dependencies

- None (built-in PowerShell 5.1+ / 7+ and Bash).

## Success Criteria

- [ ] `setup.ps1` and `run.ps1` execute on Windows PowerShell.
- [ ] `setup.sh` handles macOS environment detection without package manager errors.
- [ ] `README.md` contains clear multi-platform quickstart instructions.
