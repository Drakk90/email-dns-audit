# Proposal: Free & Self-Contained CISO Domain and Email Evaluation Engine

## Intent

Build a 100% free, self-contained domain and email security evaluation engine for CISOs without third-party API keys, paid subscriptions, or external dependencies, generating executive Excel workbooks (.xlsx) and structured reports.

## Scope

### In Scope
- **Email Security Analyzer**: Direct DNS lookups and parsers for SPF (RFC 7208 lookup limits/syntax), DKIM selectors, DMARC (RFC 7489 policies/alignment), BIMI (SVG validation), and MTA-STS/TLS-RPT (RFC 8461/8460).
- **Direct Cryptography & Transport Prober**: Raw TLS handshakes over SMTP (STARTTLS port 25), HTTPS (443), and DNSSEC validation (DS/DNSKEY/RRSIG).
- **Zero-Cost Threat & Surface Intel**: Free RDAP domain queries, public DNSBL lookups, and crt.sh Certificate Transparency log lookups.
- **Local Attack Surface & Brand Protection**: Offline Levenshtein/homoglyph/IDN typosquatting generator and dangling CNAME (subdomain takeover) signature matcher.
- **CISO Executive Scoring & Compliance Engine**: 0-100 weighted risk scoring mapped to PCI-DSS v4.0 (Req 5.4), NIST CSF, and ISO 27001.
- **Excel Report Exporter**: Standalone multi-tab Excel (.xlsx) generator for CISO dashboards, executive summaries, finding logs, and compliance matrices.

### Out of Scope
- Commercial threat intel feeds requiring paid API keys (VirusTotal, SecurityScorecard).
- Inbound mail flow gateway proxying / inline email filtering.

## Capabilities

### New Capabilities
- `email-auth-analyzer`: Evaluates SPF, DKIM, DMARC, BIMI, MTA-STS, and TLS-RPT via direct DNS/HTTPS queries.
- `transport-security-prober`: Executes raw SMTP STARTTLS and TLS 1.3/1.2 handshake audits with cipher suite evaluation.
- `attack-surface-detector`: Generates typosquatting/homoglyph variants and detects dangling CNAME takeovers offline.
- `domain-hygiene-scorer`: Compiles multi-signal findings into an executive risk score and compliance matrix.
- `excel-report-exporter`: Generates styled executive .xlsx workbooks with summary cards, severity charts, finding breakdowns, and compliance tabs.

### Modified Capabilities
None.

## Approach

Implement a modular, zero-dependency architecture in Go or Python:
1. Concurrent DNS and socket probes using standard networking protocols.
2. Local parsing and validation against IETF RFC standards.
3. Offline heuristic evaluations for brand protection and risk scoring.
4. Native Excel generation using standard XML-based spreadsheet writers.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `pkg/analyzer/` | New | Protocol evaluators (SPF, DMARC, DKIM, MTA-STS) |
| `pkg/prober/` | New | Direct SMTP STARTTLS & TLS socket probers |
| `pkg/easm/` | New | Typosquatting heuristics & dangling DNS matcher |
| `pkg/scoring/` | New | CISO executive risk weighting and compliance mapper |
| `pkg/exporter/` | New | Multi-tab executive Excel workbook builder |
| `cmd/evaluator/` | New | CLI and runner pipeline |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Outbound Port 25 blocked by local ISP/cloud | Med | Fallback graceful degradation with clear port 25 diagnostics |
| DNSBL rate-limiting on high volume | Low | Cache DNSBL query results and query non-commercial endpoints directly |

## Rollback Plan

All code is isolated under `pkg/` and `cmd/`. Removal requires deleting the project directory.

## Dependencies

- Standard DNS, TLS, and spreadsheet libraries (zero external paid services).

## Success Criteria

- [ ] Evaluates any domain in under 3 seconds without API keys.
- [ ] Accurately detects SPF lookup limits, DMARC policy status, and SMTP STARTTLS support.
- [ ] Exports comprehensive executive Excel workbook (.xlsx) with multi-sheet audit results.
