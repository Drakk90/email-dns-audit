# Proposal: Excel Summary Tab Deduplication and Complete i18n Localization

## Intent

Eliminate the duplicate worksheet naming collision (`Resumen1` vs `Resumen`) in the generated Excel report and enforce strict, 100% pure localization across all 13 worksheets, table headers, KPI cards, and finding descriptions, removing mixed slash-separated strings (`EN / ES`).

## Scope

### In Scope
- **Worksheet Deduplication**: Consolidate cover and metadata sheets into a single, cohesive `Resumen` (ES) or `Summary` (EN) executive dashboard at index 0 without openpyxl collisions.
- **Strict Bilingual Localization (`i18n.py`)**:
  - Add localized dictionaries for all table column headers across all 13 worksheets (`Inventory`, `SPF`, `DKIM`, `DMARC`, `DNSSEC`, `Addons/MTA-STS`, `BIMI`, `Senders`, `Findings`, `Attack Surface`, `Compliance`, `Consolidated Summary`).
  - Replace all bilingual slash strings (`Type / Tipo`, `Brand / Entity (Marca)`, `Author / Elaborado por`, `Action / Acción`) with pure language-specific terms.
  - Localize all card labels, section titles, and action recommendations.
- **Excel Builder Refactor (`email_dns_audit_neon.py`)**: Use `t(...)` translator keys for every generated string, cell header, and worksheet title.

### Out of Scope
- Adding new security check protocols or modifying core DNS querying logic.

## Capabilities

### Modified Capabilities
- `excel-report-exporter`: Generates a single unified cover sheet and renders 100% localized text per `--lang es` or `--lang en`.

## Approach

Refactor `build_excel` in `email_dns_audit_neon.py` so that the default workbook active sheet becomes the single executive summary dashboard, and route all column and header labels through expanded translation tables in `i18n.py`.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `i18n.py` | Modified | Add full column header dictionaries for both English and Spanish |
| `email_dns_audit_neon.py` | Modified | Update `build_excel` to eliminate duplicate sheets and apply localized headers |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Missing translation key | Low | Fallback to provided default in `t(key, default)` and unit test key symmetry |

## Rollback Plan

Revert changes in `i18n.py` and `email_dns_audit_neon.py` via git.

## Dependencies

- Existing `openpyxl`, `i18n.py` (zero new dependencies).

## Success Criteria

- [ ] Exactly one cover tab exists: `Resumen` for `--lang es` and `Summary` for `--lang en` (no `Resumen1` / `Summary1`).
- [ ] 100% of worksheet headers and cell values are pure Spanish in `--lang es` and pure English in `--lang en`.
- [ ] Zero slash-separated mixed strings (`EN / ES`) exist in the output `.xlsx`.
