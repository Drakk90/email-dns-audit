# Domain Hygiene Scorer Specification

## Purpose
Aggregate multi-source protocol and surface findings into an executive risk score (0-100 / Grade A-F) and map vulnerabilities to standard security frameworks (PCI-DSS, NIST, ISO 27001).

## Requirements

### Requirement: Weighted Security Posture Scoring
The system MUST compute a composite score based on category weights: Email Authentication (40%), Transport Encryption (25%), Attack Surface/Brand (20%), and Infrastructure (15%).

#### Scenario: Full compliance calculation
- GIVEN a domain with strict DMARC (`p=reject`), valid SPF, MTA-STS enforced, TLS 1.3 on MX, and DNSSEC active
- WHEN the scorer evaluates the aggregate results
- THEN the system MUST assign a score of 95-100 (Grade A)
- AND identify zero high/critical risks.

### Requirement: Regulatory Compliance Mapping
The system MUST cross-reference findings against compliance standards including PCI-DSS v4.0 Requirement 5.4 (DMARC anti-phishing mandate).

#### Scenario: PCI-DSS v4.0 non-compliance detection
- GIVEN a domain with `p=none` or missing DMARC
- WHEN the scorer runs compliance checks
- THEN the system MUST flag non-compliance for PCI-DSS v4.0 Requirement 5.4.
