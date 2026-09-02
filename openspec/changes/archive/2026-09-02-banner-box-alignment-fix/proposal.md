# Proposal: Fix Terminal Banner Box Alignment

## Intent

In terminal sessions (as seen when running `./run.sh` or launching audits), the double-border ASCII box (`╔═══╗`) around the application title and subtitle has misaligned right vertical borders (`║`). In the CLI launcher (`run.sh` and `run.ps1`), the header has an extra space causing the right border to overhang by 1 character. In the Rich console banner (`email_dns_audit_neon.py`), static arbitrary space paddings (`"            "` and `"                  "`) cause the right vertical borders to fall short by 10 to 12 characters, breaking visual box integrity in both Spanish and English.

## Scope

### In Scope
- Correct spacing in `run.sh` and `run.ps1` so the interactive title box line is exactly 64 characters wide, aligning with `╔` and `╚`.
- Replace static spacing in `banner()` in `email_dns_audit_neon.py` with dynamically computed padding based on the visual string length of the title and localized `app_subtitle`.
- Ensure character-exact alignment across terminal widths in both Spanish (`es`) and English (`en`).

### Out of Scope
- Redesigning terminal color palettes or Rich theme definitions.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
None (UI cosmetic formatting fix).

## Approach

1. **Launcher Alignment (`run.sh` & `run.ps1`)**:
   - Change the middle header line from 12 trailing spaces to 11 trailing spaces:
     `║  E M A I L   D N S   A U D I T   N E O N   v 3 . 3           ║`
     matching the 64-character width of the top and bottom borders.
2. **Dynamic Banner Padding (`email_dns_audit_neon.py`)**:
   - Compute `title_pad = " " * 24` so `  E M A I L  D N S  A U D I T  v 3 . 3` fills exactly 62 characters between borders.
   - Compute `sub_pad = " " * max(0, 60 - len(sub_text))` so any localized subtitle fills exactly 60 characters after the 2-space indentation.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `email_dns_audit_neon.py` | Modified | Fix character padding in `banner()` |
| `run.sh` | Modified | Fix 1-character overhang in interactive launcher banner |
| `run.ps1` | Modified | Fix 1-character overhang in PowerShell launcher banner |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Unicode wide characters breaking character count | Low | Terminal box chars (`╔`, `║`, `╚`, `═`) are single-width; subtitle strings are standard ASCII/Latin-1 |

## Rollback Plan

Revert modified files via `git checkout -- email_dns_audit_neon.py run.sh run.ps1`.

## Dependencies

- None.

## Success Criteria

- [ ] Interactive banner in `run.sh` and `run.ps1` has perfectly aligned right vertical borders (`║`).
- [ ] Console banner in `email_dns_audit_neon.py` has perfectly aligned right vertical borders for both Spanish and English subtitles.
