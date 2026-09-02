# Tasks: Scoring Refactor and Formulaic Excel Export

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~90 lines |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | single-pr |
| Chain strategy | stacked-to-main |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: stacked-to-main
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Focused test command | Runtime harness | Rollback boundary |
|------|------|-----------|----------------------|-----------------|-------------------|
| 1 | Scoring unification and formulaic Excel export | PR 1 | `./venv-email-audit/bin/python email_dns_audit_neon.py --domain google.com --lang es` | CLI runner | `email_dns_audit_neon.py`, `i18n.py` |

## Phase 1: Foundation & Scoring Unification

- [x] 1.1 Attach `active_lang` attribute to `translate` callable in `i18n.py` to decouple logical rules from string comparisons.
- [x] 1.2 Update `evaluate_ciso_compliance_and_score()` and `check_lookalikes()` in `email_dns_audit_neon.py` to use `is_es` locale flag and centralized `i18n.py` keys instead of UI equality checks (`t("yes") == "Si"`).
- [x] 1.3 Refactor `process_results()` in `email_dns_audit_neon.py` to eliminate crude flat `// 7` calculation and bind `cumplimiento_pct` directly to the weighted CISO risk score.

## Phase 2: OpenPyXL Dynamic Formula Generator

- [x] 2.1 Update `build_excel()` in `email_dns_audit_neon.py` to generate standard OOXML formulas (`COUNTA`, `COUNTIF`, `AVERAGE`, `ROUND`, `IF`) in cover KPI cards.
- [x] 2.2 Interpolate localized sheet names (`Inventario_Dominios` vs `Domain_Inventory`, `Hallazgos` vs `Findings`) and criteria (`"Crítica"` vs `"Critical"`) dynamically based on active `--lang`.
- [x] 2.3 Store compliance in `data["resumen"]` as numeric float (`round(pct / 100.0, 4)`) and add `pct_col="X"` formatting with `0.0%` in `add_sheet()`.

## Phase 3: Multi-Domain Metric Aggregation & Terminal Integration

- [x] 3.1 Collect audited domain metadata in `run_audit()` in `email_dns_audit_neon.py` and compute real mean values for `stats["ciso_score"]` and `stats["avg_compliance"]`.
- [x] 3.2 Update `final_panel()` in `email_dns_audit_neon.py` to display dynamic CISO risk score and average compliance matching the Excel report.

## Phase 4: Verification & Validation

- [x] 4.1 Verify single domain scan in Spanish (`--lang es`) and confirm formula syntax in `Resumen`.
- [x] 4.2 Verify single domain scan in English (`--lang en`) and confirm formula syntax in `Summary`.
- [x] 4.3 Verify multi-domain batch scan and confirm arithmetic mean calculation across multiple domains.
