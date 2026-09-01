# TLS Certificate Prober Specification

## Purpose
Direct network socket probing over SMTP STARTTLS (port 25) and HTTPS (port 443) to extract and validate leaf X.509 certificates, expiration horizons, SAN matching, and cipher hygiene using Python standard libraries.

## Requirements

### Requirement: Certificate Expiration Horizon Auditing
The system MUST connect to target hostnames and calculate remaining days until certificate expiration (`not_valid_after_utc`).

#### Scenario: Certificate expiring in under 30 days
- GIVEN a mail server whose TLS certificate expires in 18 days
- WHEN the TLS certificate prober inspects the endpoint
- THEN the system MUST flag a medium-severity expiring certificate warning.

#### Scenario: Certificate expiring in under 7 days
- GIVEN an endpoint whose TLS certificate expires in 3 days
- WHEN the prober inspects the endpoint
- THEN the system MUST flag a critical-severity expiration alert.

### Requirement: Subject Alternative Names (SAN) Alignment
The system MUST verify that the connecting hostname matches at least one entry in the certificate's `subjectAltName` extension.

#### Scenario: Hostname matches certificate SAN
- GIVEN a connection to `mail.example.com` where the certificate includes `DNS:mail.example.com`
- WHEN the prober evaluates the SAN extension
- THEN the system MUST validate hostname alignment.
