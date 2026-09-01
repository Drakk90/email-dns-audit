# Attack Surface Detector Specification

## Purpose
Identify external attack surface exposures, homoglyphic lookalike domains, typosquatting registrations, and dangling DNS subdomain takeovers across audited organizational domains.

## Requirements

### Requirement: Lookalike and Typosquatting Permutation Engine
The system MUST generate permutation candidates for audited domains using homoglyphs (e.g. `o` -> `0`, `l` -> `1`, `rn` -> `m`), character omissions (Levenshtein distance 1), character transpositions, alternative TLD variations (`.co`, `.net`, `.org`, `.info`), and brand-phishing prefixes (`login-`, `secure-`, `support-`).

#### Scenario: Generating domain variations
- GIVEN a domain `example.com`
- WHEN generating candidate attack surface variations
- THEN the system MUST produce at least 15 unique permutation candidates.

### Requirement: Active Candidate Resolution and Threat Classification
The system MUST asynchronously query `A` and `MX` records for each generated candidate and classify threat level as `Critical` (active MX server), `High` (active A record without MX), or `Info` (unregistered / defensive opportunity).

#### Scenario: Classifying threat of active mail exchange
- GIVEN a lookalike domain `examp1e.com` with active MX records
- WHEN probing DNS records
- THEN the system MUST assign `Critical` threat severity and recommend `Bloquear / Monitorear MX`.

### Requirement: Subdomain Takeover Signature Probing
The system MUST resolve DNS CNAME records for common subdomains (`mail`, `webmail`, `portal`, `dev`, `stage`, `cdn`, `assets`, `docs`, `status`, `help`, `app`) and probe for dangling third-party service provider fingerprints (GitHub Pages, AWS S3, Heroku, Azure, Zendesk, Fastly, Shopify, Cloudfront).

#### Scenario: Detecting dangling CNAME provider
- GIVEN a subdomain `status.example.com` pointing to `unregistered.herokuapp.com`
- WHEN probing HTTP responses and DNS
- THEN the system MUST identify the dangling CNAME and generate a `Critical` finding for Subdomain Takeover.

### Requirement: Granular Findings, Typosquats Data Tables & On-Disk Evidence Files
The system MUST export detailed findings with RFC references in `Email & DNS Posture` and resolved IP/MX status for each generated lookalike in `Attack Surface & Typosquats`, and MUST write raw evidence artifacts for typosquatting scans and subdomain takeover probes into the output `{outdir}/evidencias/` directory for every audited domain.

#### Scenario: Writing EASM and Takeover raw evidence files
- GIVEN a domain undergoing attack surface and subdomain takeover evaluation
- WHEN probing lookalike variations and CNAME targets
- THEN the system MUST write `{outdir}/evidencias/{domain}_easm.txt` containing resolved IPs and MX servers for all lookalike candidates
- AND write `{outdir}/evidencias/{domain}_takeover.txt` containing scanned CNAME records and status checks.
