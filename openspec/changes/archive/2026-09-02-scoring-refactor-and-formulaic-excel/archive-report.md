# Archive Report: Scoring Refactor and Formulaic Excel Export

## Change Information
- **Change ID**: `scoring-refactor-and-formulaic-excel`
- **Archive Date**: 2026-09-02
- **Status**: Completed & Archived
- **Target Repository**: `/home/erecinos/Downloads/email-dns-audit/`

## Synced Capabilities (Source of Truth)
The following capability specifications have been promoted to `openspec/specs/`:
1. `openspec/specs/domain-hygiene-scorer/spec.md` (Updated with Weighted Security Posture Scoring and Multi-Domain Audit Metric Aggregation).
2. `openspec/specs/excel-report-exporter/spec.md` (Updated with Executive Summary Dashboard Layout & Grid Alignment and Bilingual Dynamic Formula Generation).

## Summary of Shipped Artifacts
- **Scoring Engine Unification (`email_dns_audit_neon.py`)**:
  - Replaced flat unweighted `// 7` score with canonical 4-pillar CISO weighted posture model (Auth 40%, Transport 25%, Identity/DNS 20%, EASM 15%).
  - Unified `cumplimiento_pct` with `ciso_score` to eliminate contradictory executive reporting.
- **Dynamic Bilingual OpenPyXL Formulation (`email_dns_audit_neon.py`, `i18n.py`)**:
  - Replaced static strings with OOXML formulas (`COUNTA`, `COUNTIF`, `AVERAGE`, `ROUND`, `IF`) across cover KPI cards.
  - Dynamically bound localized sheet references (`Inventario_Dominios` vs `Domain_Inventory`, `Hallazgos` vs `Findings`) and criteria strings (`"Crítica"` vs `"Critical"`).
  - Formatted compliance cells as raw floating-point numbers with `0.0%` number formatting.
- **Multi-Domain Mean Aggregation (`email_dns_audit_neon.py`)**:
  - Accumulated audited domain records in `run_audit()` to compute real arithmetic means for `ciso_score` and `avg_compliance`.
  - Removed static fallback defaults (`88 (B)` and `85%`).

## Verification Evidence
- **Unit Tests**: 3/3 passing automated unit tests in `test_verification.py`.
- **Live Single-Domain Scans**: Tested in Spanish (`--lang es`, score 65 / D, 65.0%) and English (`--lang en`, score 65 / D, 65.0%).
- **Live Multi-Domain Batch Scan**: Verified arithmetic means with `google.com` (65) and `cloudflare.com` (75) producing 70 (C) and 70.0%.
- **Mechanical Readback**: `diff -r` verified with exit code 0.
