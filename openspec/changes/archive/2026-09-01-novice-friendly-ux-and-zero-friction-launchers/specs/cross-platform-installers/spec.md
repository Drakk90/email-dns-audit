# Delta for Cross-Platform Installers

## MODIFIED Requirements

### Requirement: Native Windows PowerShell & Batch Launchers
The system MUST provide native PowerShell scripts (`setup.ps1` and `run.ps1`) as well as double-clickable batch wrappers (`setup.bat` and `run.bat`) for Windows environments. `setup.bat` MUST invoke `setup.ps1` with `-ExecutionPolicy Bypass`. `run.bat` MUST invoke `run.ps1` with `-ExecutionPolicy Bypass` forwarding all user arguments. `setup.ps1` MUST detect if the `python` command resolves to a zero-byte Windows Store execution alias (`WindowsApps\python.exe`) without a real Python installation and provide download guidance.

#### Scenario: Running batch setup on Windows
- GIVEN a Windows user double-clicking `setup.bat` in File Explorer
- WHEN `setup.bat` executes
- THEN it MUST launch PowerShell with `-ExecutionPolicy Bypass`
- AND complete virtual environment and dependency setup without permission errors.

### Requirement: Interactive Single-Domain and Batch Target Workflows
The interactive runners (`run.sh` and `run.ps1`) MUST offer the user the choice between auditing the pre-configured `servers.txt` list or entering a single domain name directly in the terminal, without requiring file manipulation for one-off evaluations.

#### Scenario: Interactive single-domain audit
- GIVEN an interactive execution of `run.sh` or `run.ps1`
- WHEN the user selects the single-domain option and enters `example.com`
- THEN the system MUST execute the scanner against `example.com` directly using `--domain example.com`.

### Requirement: Post-Audit Report Presentation and Troubleshooting Documentation
The interactive runners MUST identify the generated `.xlsx` report file and offer or initiate opening it with the native OS default spreadsheet handler (`start` on Windows, `open` on macOS, `xdg-open` on Linux). `README.md` MUST provide an exhaustive Troubleshooting FAQ in both English and Spanish covering Python PATH configuration, script execution permissions, zip extract usage, and Excel inspection.

#### Scenario: Reading troubleshooting guides
- GIVEN a user experiencing script execution or PATH issues
- WHEN reading `README.md` (in English or Spanish)
- THEN the document MUST display copy-pasteable resolution steps for PowerShell ExecutionPolicy, Python PATH check, and Unix execute permissions.
