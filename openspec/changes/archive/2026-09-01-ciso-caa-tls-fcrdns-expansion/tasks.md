# Tasks: CAA, TLS Certificate Health, FCrDNS, and External DMARC Verification

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~180 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR (additive expansion) |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Bilingual i18n Dictionary Expansion | PR 1 | `pytest tests/test_i18n.py` | `python3 -m unittest` | `i18n.py` |
| 2 | CAA, FCrDNS, TLS, & DMARC Probers | PR 1 | `pytest tests/test_expansion.py` | `python3 email_dns_audit_neon.py --domain example.com` | `email_dns_audit_neon.py` (probers) |
| 3 | Results Processing & Excel Columns | PR 1 | `pytest tests/test_excel.py` | `python3 email_dns_audit_neon.py --domain example.com --lang es` | `email_dns_audit_neon.py` (Excel logic) |

## Phase 1: Bilingual Foundation & i18n Keys

- [x] 1.1 Add Spanish and English translations for CAA policies, FCrDNS PTR alignment, TLS cert expiry, and external DMARC report authorization in `i18n.py`.
- [x] 1.2 Add finding templates and recommendations (`f_caa_none`, `f_fcrdns_fail`, `f_tls_exp_soon`, `f_dmarc_ext_unauth`) in `i18n.py`.

## Phase 2: DNS & Socket Probing Modules

- [x] 2.1 Implement `check_caa(domain, ro)` for RFC 8659 tags (`issue`, `issuewild`, `iodef`) in `email_dns_audit_neon.py`.
- [x] 2.2 Implement `check_fcrdns(mx_hosts, ro)` for reciprocal PTR ↔ A record verification in `email_dns_audit_neon.py`.
- [x] 2.3 Implement `check_tls_certificate_health(mx_host, port)` for expiration days, SAN matching, and weak ciphers in `email_dns_audit_neon.py`.
- [x] 2.4 Implement `check_dmarc_external_report_auth(domain, rua, ro)` for RFC 7489 §7.1 verification in `email_dns_audit_neon.py`.

## Phase 3: Integration & Excel Export

- [x] 3.1 Integrate probers into `audit_domain` `asyncio.gather` pipeline in `email_dns_audit_neon.py`.
- [x] 3.2 Update `process_results` to calculate FCrDNS, CAA, and TLS expiration findings in `email_dns_audit_neon.py`.
- [x] 3.3 Add CAA and FCrDNS data columns in `Inventario_Dominios`, `Complementos`, and `Resumen_Consolidado` sheets in `email_dns_audit_neon.py`.

## Phase 4: Verification & Automated Testing

- [x] 4.1 Write automated unit tests for CAA parser, FCrDNS validation, and TLS expiry calculation.
- [x] 4.2 Validate end-to-end CLI execution with `--domain` and `--lang es` / `--lang en` verifying generated `.xlsx` workbook.
