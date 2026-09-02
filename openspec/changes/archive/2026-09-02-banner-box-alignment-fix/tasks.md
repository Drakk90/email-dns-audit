# Tasks: Fix Terminal Banner Box Alignment

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~20 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | single-pr |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: stacked-to-main
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Align ASCII box borders in launchers and Python banner | PR 1 | `./venv-email-audit/bin/python -m unittest test_verification.py` | Terminal runner | `email_dns_audit_neon.py`, `run.sh`, `run.ps1` |

## Phase 1: Launchers Alignment

- [x] 1.1 Correct trailing space in `run.sh` from 12 to 11 spaces to achieve exact 64-character width.
- [x] 1.2 Correct trailing space in `run.ps1` from 12 to 11 spaces for PowerShell parity.

## Phase 2: Python Console Banner Dynamic Padding

- [x] 2.1 Calculate `title_pad = " " * 24` in `banner()` in `email_dns_audit_neon.py` for exact 62 inner width.
- [x] 2.2 Calculate `sub_pad = " " * max(0, 60 - len(sub_text))` for dynamic subtitle alignment in both Spanish and English.

## Phase 3: Verification & Automated Tests

- [x] 3.1 Add `test_banner_box_character_alignment` to `test_verification.py`.
- [x] 3.2 Run test suite and verify visual rendering in both languages.
