# Tasks: Cross-Platform Installers for Windows PowerShell and macOS

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~250 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR (Cross-platform installers & docs) |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Windows PowerShell `setup.ps1` & `run.ps1` | PR 1 | `pwsh -Command "..."` | `pwsh -File setup.ps1` | `setup.ps1`, `run.ps1` |
| 2 | macOS / Homebrew Detection in `setup.sh` | PR 1 | `bash setup.sh --dry-run` | `setup.sh` | `setup.sh` |
| 3 | Bilingual Documentation in `README.md` | PR 1 | Markdown preview | `README.md` | `README.md` |

## Phase 1: Native Windows PowerShell Scripts

- [x] 1.1 Create `setup.ps1` supporting Python 3.10+ verification, virtual environment creation (`venv-email-audit`), pip bootstrap/repair, `requirements.txt` installation, and `servers.txt` creation.
- [x] 1.2 Create `run.ps1` featuring interactive bilingual selection prompt (`[1] Español`, `[2] English`), DKIM discovery mode parameters, DNSSEC resolvers, and execution of `email_dns_audit_neon.py`.

## Phase 2: macOS and Homebrew Compatibility

- [x] 2.1 Update `setup.sh` with `uname -s == Darwin` detection and `brew` package manager support.

## Phase 3: Multi-Platform Bilingual Documentation

- [x] 3.1 Update English section of `README.md` with dedicated installation and execution steps for Linux, macOS, and Windows PowerShell.
- [x] 3.2 Update Spanish section of `README.md` with dedicated installation and execution steps for Linux, macOS, and Windows PowerShell.

## Phase 4: Verification and Quality Assurance

- [x] 4.1 Validate syntax and execution logic of `setup.ps1` and `run.ps1` with `pwsh` (PowerShell Core).
- [x] 4.2 Verify `setup.sh` and `run.sh` execution on Linux/macOS bash.
- [x] 4.3 Validate `README.md` links and commands.
