# Proposal: Novice-Friendly UX and Zero-Friction Launchers

## Intent

Eliminate all operational friction for non-technical users across Windows, macOS, and Linux by providing double-clickable Windows launchers, interactive single-domain audit workflows, automated report opening, and a comprehensive bilingual Troubleshooting FAQ in the documentation.

## Scope

### In Scope
- **Windows Double-Click Launchers**:
  - Add `setup.bat` and `run.bat` that automatically invoke PowerShell with `-ExecutionPolicy Bypass`, allowing Windows users to double-click without terminal errors.
- **Enhanced Interactive Runner Workflows (`run.sh` & `run.ps1`)**:
  - Prompt user to choose between auditing `servers.txt` or entering a single target domain directly (e.g. `example.com`), eliminating file-editing requirements for single scans.
  - Automatically detect generated Excel path and offer to open it immediately (`start` on Windows, `open` on macOS, `xdg-open` on Linux).
- **Windows Store Python Alias Diagnostic (`setup.ps1`)**:
  - Detect 0-byte Windows Store Python stubs and provide clear installation instructions.
- **Bilingual Troubleshooting & FAQ in `README.md`**:
  - Add an exhaustive, copy-pasteable FAQ section in English and Spanish addressing PATH setup, script policies, zip downloads, and Excel viewing.

### Out of Scope
- Building native GUI desktop apps or altering security audit algorithms.

## Capabilities

### Modified Capabilities
- `cross-platform-installers`: Adds `setup.bat`, `run.bat`, interactive single-domain options in `run.sh` / `run.ps1`, auto-report opening, and bilingual Troubleshooting FAQ in `README.md`.

## Approach

1. Create `setup.bat` and `run.bat` wrapping PowerShell execution with `-ExecutionPolicy Bypass`.
2. Update `run.sh` and `run.ps1` to include target selection (file vs single domain) and post-audit report opening prompt.
3. Enhance `setup.ps1` to detect Windows Store execution aliases.
4. Overhaul `README.md` with beginner tips and a dedicated Troubleshooting & FAQ section in both languages.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `setup.bat` | New | Windows double-clickable setup wrapper |
| `run.bat` | New | Windows double-clickable runner wrapper |
| `run.sh` | Modified | Add single domain prompt and auto-open report |
| `run.ps1` | Modified | Add single domain prompt and auto-open report |
| `setup.ps1` | Modified | Add WindowsApps Python alias detection |
| `README.md` | Modified | Add beginner guidance & Troubleshooting FAQ |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| OS lack of default GUI application for Excel | Low | Fallback gracefully with file path display if `open`/`start`/`xdg-open` fails |

## Rollback Plan

Delete `.bat` files and revert script updates via git.

## Dependencies

- None (built-in OS shell utilities).

## Success Criteria

- [ ] Windows users can execute setup and run via double-click on `.bat` files.
- [ ] Users can audit a single domain interactively without editing `servers.txt`.
- [ ] `README.md` includes comprehensive beginner Troubleshooting FAQs in English and Spanish.
