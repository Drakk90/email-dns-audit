# Transport Security Prober Specification

## Purpose
Direct network socket probing for SMTP STARTTLS, TLS certificate validation, cipher suite hygiene, and DNSSEC verification.

## Requirements

### Requirement: Direct SMTP STARTTLS Handshake Probing
The system MUST establish TCP connections to MX hostnames on port 25 and issue the `STARTTLS` command to negotiate TLS.

#### Scenario: MX server supports TLS 1.3
- GIVEN an MX hostname with port 25 accessible
- WHEN the prober initiates an SMTP STARTTLS handshake
- THEN the system MUST negotiate TLS
- AND record the TLS version, cipher suite, and certificate expiration.

#### Scenario: Port 25 blocked or STARTTLS missing
- GIVEN a network environment blocking port 25 or an MX rejecting STARTTLS
- WHEN the prober attempts the handshake
- THEN the system MUST report the connection failure gracefully without crashing
- AND flag transport encryption risk.

### Requirement: DNSSEC Integrity Check
The system MUST query authoritative nameservers with the DO (DNSSEC OK) bit and verify DS/DNSKEY records.

#### Scenario: Valid DNSSEC chain
- GIVEN a domain signed with DNSSEC and matching DS records in parent zone
- WHEN the prober validates DNSSEC
- THEN the system MUST mark DNS integrity as validated.
