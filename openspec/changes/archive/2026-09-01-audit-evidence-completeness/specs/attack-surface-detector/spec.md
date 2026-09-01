# Delta for Attack Surface Detector

## MODIFIED Requirements

### Requirement: Granular Findings and Typosquats Data Tables & Evidence Files
The system MUST export detailed findings with RFC references in `Email & DNS Posture` and resolved IP/MX status for each generated lookalike in `Attack Surface & Typosquats`, and MUST write raw evidence artifacts for typosquatting scans and subdomain takeover probes into the output `{outdir}/evidencias/` directory for every audited domain.

#### Scenario: Writing EASM and Takeover raw evidence files
- GIVEN a domain undergoing attack surface and subdomain takeover evaluation
- WHEN probing lookalike variations and CNAME targets
- THEN the system MUST write `{outdir}/evidencias/{domain}_easm.txt` containing resolved IPs and MX servers for all lookalike candidates
- AND write `{outdir}/evidencias/{domain}_takeover.txt` containing scanned CNAME records and status checks.
