# Tasks: Excel Summary Tab Deduplication and Complete i18n Localization

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~160 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR (localization & UI cleanup) |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Centralized Column Headers in i18n | PR 1 | `pytest tests/test_i18n.py` | `python3 -m unittest` | `i18n.py` |
| 2 | Excel Workbook Dedup & Refactor | PR 1 | `pytest tests/test_excel.py` | `python3 email_dns_audit_neon.py --domain example.com` | `email_dns_audit_neon.py` (`build_excel`) |
| 3 | Verification & Bilingual Output Audit | PR 1 | `pytest tests/test_excel.py` | `python3 email_dns_audit_neon.py --domain example.com --lang es` | `email_dns_audit_neon.py` |

## Phase 1: Comprehensive i18n Dictionary Expansion

- [x] 1.1 Add dedicated Spanish and English column header dictionaries in `i18n.py` for all 13 worksheets (`inventario`, `spf`, `dkim`, `dmarc`, `dnssec`, `mtasts`, `tlsrpt`, `bimi`, `remit`, `findings`, `easm`, `compliance`, `resumen_consolidado`).
- [x] 1.2 Remove all mixed slash strings (`Type / Tipo`, `Brand / Entity (Marca)`, `Author / Elaborado por`, `Action / Acción`, `Status / Estado`) from `i18n.py`.
- [x] 1.3 Add localized cover sheet banner texts and table headers (`top_findings_title`, `col_finding_desc`, `col_rec_action`) in `i18n.py`.

## Phase 2: Excel Builder Single-Cover Refactoring

- [x] 2.1 Refactor `build_excel` in `email_dns_audit_neon.py` so the initial active sheet `wb.active` is configured directly as the single Executive Dashboard (`t('sheet_summary')`), eliminating `Resumen1` / `Summary1` duplicate sheet collisions.
- [x] 2.2 Route every worksheet header list through `t(...)` translator keys in `email_dns_audit_neon.py`.
- [x] 2.3 Ensure cover sheet cards, metadata labels, and top findings table use pure localized strings without slash delimiters.

## Phase 3: Verification & Automated Quality Assurance

- [x] 3.1 Write automated tests asserting that generated workbooks contain exactly one summary sheet (`Resumen` in ES, `Summary` in EN) and zero duplicate sheets (`Resumen1`/`Summary1`).
- [x] 3.2 Validate that 100% of headers and status strings in `--lang es` and `--lang en` match their respective pure language dictionary.
