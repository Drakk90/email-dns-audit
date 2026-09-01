# Email Auth Analyzer Specification

## Purpose
Direct DNS and HTTPS protocol evaluation for core email authentication standards: SPF (RFC 7208), DKIM (RFC 6376), DMARC (RFC 7489), BIMI, and MTA-STS/TLS-RPT (RFC 8461/8460).

## Requirements

### Requirement: SPF Syntax and Lookup Limit Evaluation
The system MUST parse TXT SPF records and count recursive DNS lookups against the RFC 7208 limit of 10.

#### Scenario: SPF lookup limit exceeded
- GIVEN a domain with an SPF record requiring 11 DNS lookups
- WHEN the email auth analyzer evaluates the SPF configuration
- THEN the system MUST flag an RFC 7208 PermError violation
- AND assign a high-severity finding.

#### Scenario: Insecure SPF catch-all
- GIVEN a domain with an SPF record ending in `+all` or `?all`
- WHEN the analyzer evaluates the record
- THEN the system MUST report insecure permissive authentication.

### Requirement: DMARC Policy and Alignment Enforcement Check
The system MUST query `_dmarc.{domain}` and evaluate policy strength (`p=reject`, `quarantine`, `none`) and reporting addresses (`rua`/`ruf`).

#### Scenario: DMARC policy in monitor-only mode
- GIVEN a domain with `v=DMARC1; p=none;`
- WHEN the analyzer evaluates the DMARC policy
- THEN the system MUST warn that spoofing is not blocked
- AND recommend migration to `p=reject`.

### Requirement: MTA-STS and TLS-RPT Validation
The system MUST query `_mta-sts.{domain}` and fetch `https://mta-sts.{domain}/.well-known/mta-sts.txt`.

#### Scenario: Valid MTA-STS policy in enforce mode
- GIVEN a domain with an active MTA-STS DNS record and reachable policy file with `mode: enforce`
- WHEN the analyzer verifies MTA-STS
- THEN the system MUST validate strict transport security enforcement.
