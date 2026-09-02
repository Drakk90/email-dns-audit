# Delta for Domain Hygiene Scorer

## MODIFIED Requirements

### Requirement: Weighted Security Posture Scoring
The system MUST compute a unified composite score (0-100) and derived compliance percentage based on canonical category weights: Email Authentication (40%), Transport Encryption (25%), Attack Surface/Brand (15%), and DNS/Identity Infrastructure (20%), completely replacing unweighted flat scoring counters.
(Previously: Computed flat score // 7 independently from CISO weighted score)

#### Scenario: Full compliance calculation
- GIVEN a domain with strict DMARC (`p=reject`), valid SPF, MTA-STS enforced, TLS 1.3 on MX, and DNSSEC active
- WHEN the scorer evaluates the aggregate results
- THEN the system MUST assign a score of 95-100 (Grade A)
- AND calculate a compliance percentage of 95-100%
- AND identify zero high/critical risks.

#### Scenario: Partial compliance with weighted proportions
- GIVEN a domain with valid SPF and DKIM but missing DMARC, MTA-STS, and DNSSEC
- WHEN the scorer evaluates the results
- THEN the system MUST assign proportional score and compliance matching category weights without flat integer step jumps.

## ADDED Requirements

### Requirement: Multi-Domain Audit Metric Aggregation
The audit engine MUST calculate true mean averages across all audited domains for CISO risk score and compliance percentage, storing them in execution statistics for report rendering without static defaults.

#### Scenario: Aggregating multiple audited domains
- GIVEN three audited domains with scores 65, 50, and 58
- WHEN the audit engine completes the domain scan loop
- THEN the aggregate CISO score MUST equal 57.7
- AND the aggregate compliance percentage MUST equal the arithmetic mean of individual domain compliance values
- AND no fallback constant (such as 88 or 85%) SHALL be emitted.
