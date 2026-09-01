# Tasks: Audit Evidence Completeness and Unbounded Findings Dashboard

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~90 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR (evidence completeness & UI) |
| Delivery strategy | exception-ok |
| Chain strategy | size-exception |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: size-exception
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Unbounded Cover Table & Background Range | PR 1 | `pytest tests/test_excel.py` | `python3 email_dns_audit_neon.py --domain example.com` | `email_dns_audit_neon.py` (`build_excel`) |
| 2 | Raw Evidence Generation for EASM & Takeover | PR 1 | `pytest tests/test_easm.py` | `python3 email_dns_audit_neon.py --domain example.com` | `email_dns_audit_neon.py` (probers) |
| 3 | Automated Multi-Domain Verification | PR 1 | `pytest tests/test_multi.py` | `python3 -m unittest` | `email_dns_audit_neon.py` |

## Phase 1: Unbounded Cover Sheet Findings Table

- [x] 1.1 Remove artificial `[:15]` row limit in `build_excel` in `email_dns_audit_neon.py` to render 100% of Critical and High findings for all audited domains.
- [x] 1.2 Dynamically calculate white background fill range in `ws_cover` based on total findings count (`max(45, 12 + len(crit_high_findings))`).

## Phase 2: Complete On-Disk Raw Evidence Generation

- [x] 2.1 Update `check_lookalikes` to write `{domain}_easm.txt` containing full details of lookalike permutations and resolved DNS/MX targets into `outdir / "evidencias"`.
- [x] 2.2 Update `check_subdomain_takeover` to write `{domain}_takeover.txt` detailing all tested CNAMEs and responses into `outdir / "evidencias"`.
- [x] 2.3 Verify `check_caa`, `check_fcrdns`, and `check_tls_certificate_health` write raw diagnostic files to `outdir / "evidencias"`.

## Phase 3: Verification & Automated Quality Assurance

- [x] 3.1 Write automated unit tests verifying that multi-domain audits render all findings from all domains in `ws_cover`.
- [x] 3.2 Validate that all raw evidence files are generated on disk in the `evidencias/` directory.
