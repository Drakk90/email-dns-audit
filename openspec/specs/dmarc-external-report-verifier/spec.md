# DMARC External Report Verifier Specification

## Purpose
Direct DNS validation of third-party DMARC aggregate and forensic report destinations per RFC 7489 §7.1 to prevent silent report discarding and visibility loss.

## Requirements

### Requirement: External DMARC Authorization Record Verification
When a domain's DMARC `rua` or `ruf` specifies an external destination domain `target.com`, the system MUST query `{domain}._report._dmarc.{target.com}` for a valid TXT record starting with `v=DMARC1`.

#### Scenario: Authorized external DMARC reporting
- GIVEN a domain `company.com` with `rua=mailto:reports@dmarcanalytics.com` and a matching TXT record `company.com._report._dmarc.dmarcanalytics.com` containing `v=DMARC1`
- WHEN the external report verifier checks authorization
- THEN the system MUST confirm legitimate report delivery.

#### Scenario: Missing authorization record
- GIVEN a domain with external `rua` destination where no authorization TXT record is published
- WHEN the verifier checks authorization
- THEN the system MUST warn that mail receivers will drop aggregate reports
- AND flag a medium-severity reporting blind-spot.
