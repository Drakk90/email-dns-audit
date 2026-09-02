# Tasks: Formulated Consolidated Scoring Columns

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~60 lines |
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
| 1 | Formulate 4 pillar columns and global compliance | PR 1 | `./venv-email-audit/bin/python -m unittest test_verification.py` | CLI runner | `email_dns_audit_neon.py`, `i18n.py` |

## Phase 1: i18n & Schema Definition

- [x] 1.1 Add bilingual pillar header keys (`col_cons_score_auth`, `col_cons_score_trans`, `col_cons_score_dns`, `col_cons_score_easm`) in `i18n.py`.

## Phase 2: Core Implementation in Excel Report Exporter

- [x] 2.1 Update `build_excel()` in `email_dns_audit_neon.py` to insert the 4 score breakdown columns into `Resumen_Consolidado`.
- [x] 2.2 Generate row formulas for the 4 pillars (Auth, Transport, DNS/Identity, EASM) and the global compliance sum formula in column `AB`.
- [x] 2.3 Retarget Cover sheet KPI cards `M5` and `J5` in `email_dns_audit_neon.py` to reference column `AB`.
- [x] 2.4 Update `add_sheet()` call for `Resumen_Consolidado` with `pct_col="AB"` and adjust column widths.

## Phase 3: Verification & Validation

- [x] 3.1 Update unit tests in `test_verification.py` to validate the 28 columns and formulated cells.
- [x] 3.2 Verify live single-domain audit in Spanish (`--lang es`) and inspect column `AB` formulas.
- [x] 3.3 Verify live single-domain audit in English (`--lang en`) and inspect cross-sheet references.
