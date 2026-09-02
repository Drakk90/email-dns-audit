# Proposal: Scoring Refactor and Formulaic Excel Export

## Intent

Fix the critical discrepancy between hardcoded cover KPIs and actual domain compliance, unify contradictory scoring systems into a single RFC/CISO weighted model, and implement dynamic OpenPyXL formulas across bilingual report workbooks.

## Scope

### In Scope
- **Unified Scoring Model**: Replace unweighted `score * 100 // 7` with the 4-pillar CISO weighted model (Authentication 40%, Transport 25%, DNS/Identity 20%, Surface 15%), calculating continuous percentages.
- **Aggregation Fix in `run_audit`**: Populate `stats["ciso_score"]` and `stats["avg_compliance"]` with actual domain averages instead of falling back to hardcoded `88 (B)` and `85%`.
- **Dynamic OpenPyXL Formulas**: Replace static text literals in executive cards and summary columns with native Excel formulas (`COUNTA`, `COUNTIF`, `AVERAGE`).
- **Bilingual Formula Resolution**: Dynamically bind formula arguments (sheet names, localized severity criteria like `"Crítica"` vs `"Critical"`) based on active `--lang [es|en]`.
- **Native Numeric Formatting**: Store compliance percentages as raw floats (`0.85`) with `0.0%` number formatting and scores as integers for spreadsheet interoperability.

### Out of Scope
- Adding new DNS/TLS protocol checks or external dependencies beyond `openpyxl`.
- Modifying CLI terminal layouts in Rich.

## Capabilities

### Modified Capabilities
- `domain-hygiene-scorer`: Replaces crude flat scoring with unified weighted framework aggregation and fixes domain-to-audit KPI metrics.
- `excel-report-exporter`: Implements native dynamic formulas and bilingual sheet/criteria resolution across generated workbooks.

## Approach

1. **Scoring Unification**: Harmonize `cumplimiento_pct` and `ciso_score` into a single canonical calculation in `domain-hygiene-scorer`. Calculate running and final averages across domains in `run_audit`.
2. **Formula Generator**: Build a helper in `build_excel` that renders formula strings using standard English OOXML function names (`COUNTIF`, `COUNTA`, `AVERAGE`) while interpolating localized sheet names (`Resumen` vs `Summary`, `Hallazgos` vs `Findings`) and criteria tokens.
3. **OpenPyXL Number Formatting**: Set raw numeric values on cells and assign `number_format = '0.0%'` or integer formats.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `email_dns_audit_neon.py` | Modified | Unify scoring calculations, aggregate metrics in `run_audit`, implement formulas in `build_excel` |
| `i18n.py` | Modified | Add any missing formula token mappings or methodology strings |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Localized formula syntax corruption | High | Always use English formula names (`COUNTIF`, not `CONTAR.SI`) per OOXML specification |
| Broken cross-sheet formula refs | Medium | Dynamically interpolate active sheet titles from `t("sheet_*")` |

## Rollback Plan

Revert changes specifically to tracked code files (`email_dns_audit_neon.py` and `i18n.py`) via scoped `git restore` or `git checkout`, preserving untracked local Zona 2 memory files.

## Dependencies

- None (uses existing `openpyxl`).

## Success Criteria

- [ ] Executive cover cards in `.xlsx` contain dynamic formulas referencing detail sheets.
- [ ] No hardcoded default KPIs (`88 (B)`, `85%`) remain in codebase or output.
- [ ] Workbooks generated with `--lang es` and `--lang en` open cleanly without `#REF!` or `#NAME?` errors in Excel.
- [ ] Compliance percentages are stored as numeric floats with percentage formatting.
