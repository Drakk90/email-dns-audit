# Archive Report: Excel Grid Alignment and Missing Data Ingestion Fix

## Change Information
- **Change ID**: `excel-grid-and-data-alignment-fix`
- **Archive Date**: 2026-09-01
- **Status**: Completed & Archived
- **Target Repository**: `/home/erecinos/Downloads/email-dns-audit/`

## Synced Capabilities (Source of Truth)
The following capability specifications have been promoted to `openspec/specs/`:
1. `openspec/specs/excel-report-exporter/spec.md` (Updated with Executive Summary Dashboard Layout & Grid Alignment, and Infrastructure Deliverability & Certificate Health Data Population)

## Summary of Shipped Artifacts
- **Cover Findings Table Grid Merge (`email_dns_audit_neon.py`)**:
  - Merged row spans (`B:C`, `D:E`, `F:I`, `J:K`, `L:N`) for header and all finding rows, achieving perfect column alignment with top KPI cards and eliminating blank gaps.
- **`Complementos` / `Addons` Data Ingestion (`email_dns_audit_neon.py`)**:
  - Populated `data["caa_tls"]` in `process_results` to render CAA, FCrDNS, and TLS certificate records for each domain.
- **`Inventario_Dominios` / `Domain_Inventory` 13-Column Alignment (`email_dns_audit_neon.py`)**:
  - Fixed column offset so that `CISO Score` falls in column 13 (`Comentarios y Score` / `Comments & Score`).

## Verification Evidence
- **Unit Tests**: 2/2 passing unit tests in Spanish and English.
- **Live Scans**: Tested in Spanish (`--lang es`, 3 domains) and English (`--lang en`, 2 domains) with 100% clean grid alignment.
- **Mechanical Readback**: `diff -r` verified with exit code 0.
