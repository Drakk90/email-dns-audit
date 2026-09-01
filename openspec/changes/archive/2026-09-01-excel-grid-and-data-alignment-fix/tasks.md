# Tasks: Excel Grid Alignment and Missing Data Ingestion Fix

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~60 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR (Excel grid & data fix) |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Ingest `data["caa_tls"]` & Align `Inventario` | PR 1 | `pytest tests/test_data.py` | `python3 email_dns_audit_neon.py --domain example.com` | `email_dns_audit_neon.py` (`process_results`) |
| 2 | Merged Grid Findings Table in Cover | PR 1 | `pytest tests/test_cover.py` | `python3 email_dns_audit_neon.py --domain example.com` | `email_dns_audit_neon.py` (`build_excel`) |
| 3 | Automated Verification | PR 1 | `pytest tests/test_verify.py` | `python3 -m unittest` | `email_dns_audit_neon.py` |

## Phase 1: Data Ingestion and Column Alignment

- [x] 1.1 In `process_results`, append structured records to `data["caa_tls"]` for each domain containing CAA CAs, iodef, FCrDNS status, TLS cert days left, and issuer.
- [x] 1.2 In `process_results`, update `data["inventario"]` row appending to include all 13 columns (inserting CAA CAs and FCrDNS status before CISO Score).

## Phase 2: Executive Cover Merged Grid Alignment

- [x] 2.1 Update header row 9 in `ws_cover` to merge `B9:C9` (Domain), `D9:E9` (Control), `F9:I9` (Description), `J9:K9` (Severity), and `L9:N9` (Action).
- [x] 2.2 In `build_excel`, merge each finding row `idx` across `B{idx}:C{idx}`, `D{idx}:E{idx}`, `F{idx}:I{idx}`, `J{idx}:K{idx}`, and `L{idx}:N{idx}` with appropriate border styling.

## Phase 3: Automated Verification & Testing

- [x] 3.1 Write unit tests verifying that `Complementos` rows for CAA/TLS are populated and `Inventario_Dominios` columns align.
- [x] 3.2 Verify that `Resumen` findings table contains no unmerged blank columns.
