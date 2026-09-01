# Delta for Excel Report Exporter

## ADDED Requirements

### Requirement: Infrastructure Deliverability & Certificate Health Columns
The system MUST include dedicated columns for CAA governance, FCrDNS PTR status, and TLS certificate expiration days in the generated Excel worksheets.

#### Scenario: Exporting CAA and FCrDNS metrics
- GIVEN domain audit results containing CAA policies and MX FCrDNS evaluations
- WHEN generating the Excel report
- THEN the system MUST render CAA record tags, FCrDNS alignment status, and TLS certificate validity days with appropriate color-coding in English or Spanish.
