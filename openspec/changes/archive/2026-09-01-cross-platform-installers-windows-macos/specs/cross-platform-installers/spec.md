# Cross-Platform Installers Specification

## Purpose
Provide native, automated setup scripts, interactive runners, and comprehensive documentation for Linux, macOS, and Windows PowerShell environments.

## Requirements

### Requirement: Native Windows PowerShell Installation and Execution
The system MUST provide native PowerShell scripts (`setup.ps1` and `run.ps1`) for Windows environments. `setup.ps1` MUST verify Python 3.10+, create the `venv-email-audit` virtual environment, upgrade pip, install `requirements.txt`, and prepare `servers.txt`. `run.ps1` MUST provide an interactive language selection prompt (Spanish / English), support DKIM discovery modes (normal / deep), and execute the scanner using the virtual environment interpreter.

#### Scenario: Running setup on Windows PowerShell
- GIVEN a Windows system with Python 3.10+ installed
- WHEN the user executes `.\setup.ps1` in PowerShell
- THEN the script MUST create `venv-email-audit`, install dependencies from `requirements.txt`, and copy `servers.example.txt` to `servers.txt`.

#### Scenario: Interactive execution on Windows PowerShell
- GIVEN an installed environment on Windows
- WHEN the user runs `.\run.ps1` without arguments
- THEN the script MUST present an interactive prompt to choose between `[1] Español` and `[2] English`
- AND execute `email_dns_audit_neon.py` with `--lang` set to the selected language.

### Requirement: macOS and Homebrew Compatibility in Unix Scripts
The `setup.sh` script MUST detect macOS (`uname -s == Darwin`) and Homebrew package manager (`brew`), avoiding Linux-specific package commands (`apt`, `pacman`, `dnf`) on macOS systems.

#### Scenario: Running setup on macOS
- GIVEN a macOS system with Homebrew or system Python
- WHEN the user runs `./setup.sh`
- THEN the script MUST detect `brew` or macOS environment and proceed with virtual environment creation without invoking `apt` or `pacman`.

### Requirement: Comprehensive Multi-Platform Bilingual Documentation
The `README.md` document MUST provide clear, separate installation and execution guides for Linux, macOS, and Windows (PowerShell) in both English and Spanish documentation sections.

#### Scenario: Reading installation instructions in English
- GIVEN a user viewing the English documentation section in `README.md`
- WHEN looking for setup instructions
- THEN the document MUST display dedicated subsections for Linux, macOS, and Windows (PowerShell).

#### Scenario: Reading installation instructions in Spanish
- GIVEN a user viewing the Spanish documentation section in `README.md`
- WHEN looking for setup instructions
- THEN the document MUST display dedicated subsections for Linux, macOS, and Windows (PowerShell).
