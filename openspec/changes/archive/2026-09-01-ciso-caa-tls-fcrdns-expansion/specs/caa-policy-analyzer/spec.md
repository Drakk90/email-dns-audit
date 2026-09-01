# CAA Policy Analyzer Specification

## Purpose
Direct DNS evaluation of Certificate Authority Authorization (CAA) records per RFC 8659 / RFC 6844 to enforce certificate issuance governance and incident reporting.

## Requirements

### Requirement: CAA Record and Property Tag Parsing
The system MUST query `CAA` records for the target domain and parse standard property tags (`issue`, `issuewild`, `iodef`).

#### Scenario: Valid CAA record with defined CAs and iodef
- GIVEN a domain configured with `CAA 0 issue "letsencrypt.org"` and `CAA 0 iodef "mailto:security@example.com"`
- WHEN the CAA analyzer evaluates the domain
- THEN the system MUST record the authorized CAs
- AND extract the incident notification endpoint `iodef`
- AND mark the CAA status as compliant.

#### Scenario: Missing CAA record
- GIVEN a domain with no CAA DNS records published
- WHEN the analyzer evaluates the domain
- THEN the system MUST warn that any public CA can issue certificates
- AND report an informational hygiene finding.
