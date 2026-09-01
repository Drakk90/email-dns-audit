# Proposal: CAA, TLS Certificate Health, FCrDNS, and External DMARC Verification

## Intent

Enhance the CISO email and DNS evaluation suite with infrastructure deliverability and certificate security checks: CAA record policy validation (RFC 8659), direct TLS certificate health/expiry probing on MX servers, Forward-Confirmed reverse DNS (FCrDNS / PTR alignment), and external DMARC report authorization verification (RFC 7489 §7.1), using existing Python libraries with zero external paid APIs.

## Scope

### In Scope
- **CAA Policy Analyzer**: Queries and parses DNS `CAA` records (`issue`, `issuewild`, `iodef`) to verify CA issuance restrictions and incident reporting endpoints.
- **TLS Certificate Health Prober**: Connects directly via socket/STARTTLS (ports 25, 443) using Python `ssl` and `cryptography` to evaluate leaf certificate validity, days until expiration (<30d warning, <7d critical), SAN alignment, and protocol support.
- **FCrDNS & PTR Validator**: Resolves MX IPs, executes reverse PTR lookups, and validates forward A matching (RFC 7601) to detect anti-spam deliverability blocks.
- **External DMARC Report Verifier**: Validates third-party DMARC report authorization records (`{domain}._report._dmarc.{target_domain}`) per RFC 7489 §7.1 to identify silent report drops.
- **Excel Export & i18n**: Updates workbook sheets with dedicated CAA, FCrDNS, and TLS certificate columns in English and Spanish.

### Out of Scope
- Commercial certificate monitoring APIs or automated CA certificate issuance/renewal pipelines.

## Capabilities

### New Capabilities
- `caa-policy-analyzer`: Evaluates DNS CAA issuance restrictions and incident reporting emails.
- `tls-certificate-prober`: Probes active MX/Web certificates for expiration horizons, SAN matching, and weak cipher signatures.
- `fcrdns-alignment-validator`: Validates forward and reverse DNS consistency on mail exchangers.
- `dmarc-external-report-verifier`: Checks RFC 7489 authorization records for external DMARC `rua` endpoints.

### Modified Capabilities
- `excel-report-exporter`: Adds CAA, FCrDNS, and TLS certificate health data points to audit sheets.

## Approach

Leverage existing `dnspython`, `cryptography`, `httpx`, and stdlib `ssl`/`socket` packages inside `email_dns_audit_neon.py` to run asynchronous probes in parallel during domain evaluation without adding new dependencies.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `i18n.py` | Modified | Add bilingual translation keys for CAA, FCrDNS, TLS expiry, and DMARC verification |
| `email_dns_audit_neon.py` | Modified | Integrate async CAA, FCrDNS, TLS certificate probers, and update Excel sheets |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Port 25 timeouts on firewalled MX | Med | 3-second connect timeout with graceful fallback |
| Missing PTR on secondary MX | Low | Flag as partial deliverability warning rather than critical crash |

## Rollback Plan

Revert changes in `email_dns_audit_neon.py` and `i18n.py` using git.

## Dependencies

- Existing `dnspython`, `cryptography`, `httpx`, `openpyxl` (zero new dependencies).

## Success Criteria

- [ ] Identifies CAA records, `issue` authorities, and `iodef` emails.
- [ ] Detects expiring TLS certificates (<30 days) on MX servers.
- [ ] Validates FCrDNS (PTR -> Forward A) on all active MX hostnames.
- [ ] Verifies external DMARC `rua` authorization per RFC 7489 §7.1.
- [ ] Exports all findings into bilingual Excel (.xlsx) reports.
