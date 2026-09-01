# Proposal: Audit Evidence Completeness and Unbounded Findings Dashboard

## Intent

Ensure 100% evidentiary completeness across all audited domains by eliminating artificial truncation in the executive dashboard findings table and generating granular on-disk technical evidence files for all probing modules (EASM, Takeover, CAA, FCrDNS, TLS certificates, and email authentication).

## Scope

### In Scope
- **Unbounded Executive Dashboard Table**: Render all Critical and High security findings for all audited domains dynamically on the `Resumen` / `Summary` worksheet without fixed slicing limits (`[:15]`), dynamically sizing the background styling and borders.
- **Complete On-Disk Technical Evidence**: Ensure all probing modules (including `check_lookalikes`, `check_subdomain_takeover`, `check_caa`, `check_fcrdns`, and `check_tls_certificate_health`) write detailed raw evidence logs to `{outdir}/evidencias/{domain}_*.txt` for audit compliance.
- **Cross-Domain Findings Integrity**: Verify that multi-domain audits populate complete row datasets across all 13 worksheets.

### Out of Scope
- Modifying scoring formulas or adding third-party paid API dependencies.

## Capabilities

### Modified Capabilities
- `excel-report-exporter`: Renders dynamic, unbounded findings tables in the executive dashboard.
- `attack-surface-detector`: Writes lookalike DNS resolution and subdomain takeover scan evidence files to disk.
- `caa-policy-analyzer`: Writes raw CAA record responses to `{outdir}/evidencias/`.
- `fcrdns-alignment-validator`: Writes reciprocal PTR and A record validation logs to disk.
- `tls-certificate-prober`: Writes leaf certificate details and SAN lists to disk.

## Approach

Refactor `build_excel` in `email_dns_audit_neon.py` to iterate over all critical and high findings without truncation, and update prober functions in `email_dns_audit_neon.py` to write raw evidence files to `outdir / "evidencias"`.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `email_dns_audit_neon.py` | Modified | Remove row slicing in `build_excel` and add evidence file writes to probers |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Large workbook row count on mass scans | Low | Openpyxl supports up to 1M rows; auto-height and banded formatting applied dynamically |

## Rollback Plan

Revert changes in `email_dns_audit_neon.py` via git.

## Dependencies

- Existing `openpyxl`, `dnspython`, `httpx` (zero new dependencies).

## Success Criteria

- [ ] Executive summary table on `Resumen` / `Summary` renders 100% of Critical and High findings across all audited domains.
- [ ] Raw technical evidence files exist under `evidencias/` for every domain and every probed control.
