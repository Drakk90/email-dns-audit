# Tasks: CISO Domain & Email Evaluation Engine Integration

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~350 lines |
| 400-line budget risk | Medium |
| Chained PRs recommended | No |
| Suggested split | Single PR (atomic feature integration) |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Bilingual i18n & EASM/CISO Models | PR 1 | `pytest tests/test_i18n.py` | `python3 -m unittest` | `i18n.py` |
| 2 | Typosquatting & Subdomain Takeover Engine | PR 1 | `pytest tests/test_easm.py` | `python3 email_dns_audit_neon.py --domain example.com` | `email_dns_audit_neon.py` (EASM functions) |
| 3 | CISO Scoring & Excel Multi-Tab Exporter | PR 1 | `pytest tests/test_excel.py` | `python3 email_dns_audit_neon.py --domain example.com --lang es` | `email_dns_audit_neon.py` (Excel tabs) |

## Phase 1: Bilingual Foundation & i18n Dictionary Expansion

- [x] 1.1 Add Spanish and English translations for Typosquatting, Homoglyphs, Subdomain Takeover, and CISO Risk Scoring in `i18n.py`.
- [x] 1.2 Add PCI-DSS v4.0 Req 5.4, NIST CSF, and ISO 27001 compliance strings in `i18n.py`.
- [x] 1.3 Add helper functions for localized severity and finding descriptions in `i18n.py`.

## Phase 2: Local Attack Surface & Typosquatting Engine

- [x] 2.1 Implement offline permutation algorithms (Levenshtein, bit-squatting, IDN homoglyphs) in `email_dns_audit_neon.py`.
- [x] 2.2 Add concurrent DNS A/MX resolution prober for generated lookalike domains in `email_dns_audit_neon.py`.
- [x] 2.3 Implement signature-based dangling CNAME takeover checker (AWS S3, GitHub Pages, Azure, Zendesk) in `email_dns_audit_neon.py`.

## Phase 3: CISO Executive Risk Scoring & Compliance Mapper

- [x] 3.1 Implement weighted multi-signal scoring algorithm (0-100 / Grade A-F) in `email_dns_audit_neon.py`.
- [x] 3.2 Implement regulatory compliance matrix evaluator (PCI-DSS v4.0, NIST, ISO) in `email_dns_audit_neon.py`.

## Phase 4: Multi-Tab Excel (.xlsx) Exporter Enhancement

- [x] 4.1 Create `Attack Surface & Typosquats` sheet with lookalike domain findings and threat ratings in `email_dns_audit_neon.py`.
- [x] 4.2 Create `CISO Compliance Matrix` sheet with requirement-by-requirement gap analysis in `email_dns_audit_neon.py`.
- [x] 4.3 Update `Executive Summary` sheet with overall risk score, letter grade, and top prioritized remediation actions in `email_dns_audit_neon.py`.
- [x] 4.4 Ensure all Excel headers, cell values, and conditional formats dynamically adapt to `--lang es` or `--lang en` in `email_dns_audit_neon.py`.

## Phase 5: Verification & CLI Integration

- [x] 5.1 Test CLI execution with `--domain` and `--lang es` / `--lang en` outputting full `.xlsx` workbook.
- [x] 5.2 Validate offline execution without external API keys or paid subscriptions.
