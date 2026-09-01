# Proposal: Excel Grid Alignment and Missing Data Ingestion Fix

## Intent

Fix table grid alignment in the executive cover worksheet and resolve missing data rows across `Complementos` and `Inventario_Dominios` to deliver a flawless, production-ready CISO audit workbook.

## Scope

### In Scope
- **Executive Cover Grid Unification**: Align executive findings table cells with top KPI cards by merging row spans (`A` for ID, `B:C` for Domain, `D:E` for Control, `F:I` for Description, `J:K` for Severity, `L:N` for Action) or standardizing column layout, eliminating orphaned empty cells.
- **`Complementos` CAA & TLS Data Rows Ingestion**: Populate `data["caa_tls"]` in `process_results` with CAA allowed CAs, incident reporting (iodef), FCrDNS status, TLS certificate remaining days, and issuer strings for all audited domains.
- **`Inventario_Dominios` Column Alignment**: Fix column offset by supplying all 13 values matching headers (including CAA CAs and FCrDNS status before CISO Score).

### Out of Scope
- Modifying security scanning logic or adding external libraries.

## Capabilities

### Modified Capabilities
- `excel-report-exporter`: Generates well-aligned cover tables and complete rows for `Complementos` and `Inventario_Dominios`.

## Approach

1. Refactor `process_results` in `email_dns_audit_neon.py` to append structured tuples to `data["caa_tls"]` and ensure `data["inventario"]` matches its 13-column schema.
2. Refactor `build_excel` cover findings rendering to properly merge cell ranges across columns `A1:N1` per row or use clean contiguous column spans with unified borders.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `email_dns_audit_neon.py` | Modified | Fix row data population in `process_results` and table merging in `build_excel` |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Openpyxl merged cell styling quirks | Low | Apply border and alignment styles to top-left merged cell and iterate row borders |

## Rollback Plan

Revert git commit if workbook generation fails.

## Dependencies

- Existing `openpyxl` (zero new dependencies).

## Success Criteria

- [ ] Executive cover findings table has unified column structure without orphaned gaps.
- [ ] Section `CAA y Salud de Certificados TLS` in `Complementos` contains full row records for all audited domains.
- [ ] `Inventario_Dominios` rows align with all 13 header columns.
