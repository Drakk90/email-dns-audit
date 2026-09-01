# FCrDNS Alignment Validator Specification

## Purpose
Direct DNS validation of Forward-Confirmed reverse DNS (FCrDNS / PTR alignment per RFC 7601 and RFC 8601) on mail exchanger IP addresses to prevent anti-spam deliverability blocks.

## Requirements

### Requirement: Reverse PTR and Forward A Record Consistency
The system MUST resolve IP addresses for all MX records, query their reverse `PTR` records, and forward-resolve each returned PTR hostname to ensure reciprocal IP matching.

#### Scenario: Full FCrDNS reciprocal alignment
- GIVEN an MX hostname resolving to `192.0.2.1` whose PTR is `mail.example.com` and `mail.example.com` resolves back to `192.0.2.1`
- WHEN the FCrDNS validator evaluates the server
- THEN the system MUST mark FCrDNS as valid
- AND confirm optimal deliverability posture.

#### Scenario: Missing PTR or forward mismatch
- GIVEN an MX IP with no reverse PTR record or a PTR hostname resolving to a different IP
- WHEN the validator evaluates the server
- THEN the system MUST flag an FCrDNS deliverability failure
- AND assign a high-severity anti-spam risk.
