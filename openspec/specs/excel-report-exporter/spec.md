# Excel Report Exporter Specification

## Purpose
Generate formatted, multi-tab Microsoft Excel (.xlsx) workbooks designed for executive CISO reviews, audit teams, and remediation engineers without external service dependencies.

## Requirements

### Requirement: Multi-Tab Executive Workbook Structure
The system MUST generate an `.xlsx` workbook containing structured sheets including a single executive summary dashboard (`Resumen` or `Summary`), `Inventario_Dominios` / `Domain_Inventory`, `SPF`, `DKIM`, `DMARC`, `DNSSEC`, `Complementos` / `Addons`, `Remitentes_Autorizados` / `Authorized_Senders`, `Hallazgos` / `Findings`, `Superficie_Ataque_Typosquats` / `Attack_Surface_Typosquats`, `Matriz_Cumplimiento_CISO` / `CISO_Compliance_Matrix`, and `Resumen_Consolidado`. The workbook MUST NOT contain duplicate or numbered suffix summary sheets (such as `Resumen1` or `Summary1`).

#### Scenario: Single executive dashboard generation
- GIVEN a completed domain evaluation dataset
- WHEN the exporter creates the Excel workbook
- THEN the system MUST produce exactly one executive dashboard sheet at index 0 titled `Resumen` (when `--lang es`) or `Summary` (when `--lang en`)
- AND the workbook MUST NOT contain any colliding `Resumen1` or `Summary1` sheets.

### Requirement: Executive Summary Dashboard Layout & Evidentiary Completeness
The `Executive Summary` dashboard sheet MUST include executive title banner, metadata summary (author, CISO role, date), overall numerical score KPI card, total domains card, critical findings card, high findings card, average compliance KPI card, and an unbounded findings table displaying 100% of all critical and high severity findings across all audited domains without artificial truncation limits.

#### Scenario: Exporting complete multi-domain findings
- GIVEN an audit execution of multiple domains yielding critical and high findings
- WHEN generating the Executive Summary dashboard sheet
- THEN the system MUST render all critical and high findings in the table starting at row 10
- AND each finding MUST display its ID, Domain, Control, Description, Severity, and Recommended Action
- AND the sheet background styling MUST dynamically encompass all generated rows.

### Requirement: Granular Findings and Typosquats Data Tables
The system MUST export detailed findings with RFC references in `Email & DNS Posture` and resolved IP/MX status for each generated lookalike in `Attack Surface & Typosquats`.

#### Scenario: Exporting typosquatting threat table
- GIVEN 20 discovered lookalike domain candidates
- WHEN exporting the Attack Surface worksheet
- THEN the system MUST tabulate Candidate Domain, Mutation Type (Homoglyph/Bitsquat), Registration Status, Resolved IPs, and Threat Level.

### Requirement: Infrastructure Deliverability & Certificate Health Columns
The system MUST include dedicated columns for CAA governance, FCrDNS PTR status, and TLS certificate expiration days in the generated Excel worksheets.

#### Scenario: Exporting CAA and FCrDNS metrics
- GIVEN domain audit results containing CAA policies and MX FCrDNS evaluations
- WHEN generating the Excel report
- THEN the system MUST render CAA record tags, FCrDNS alignment status, and TLS certificate validity days with appropriate color-coding in English or Spanish.

### Requirement: Strict Language Domain Localization
All worksheet titles, table column headers, KPI card labels, status strings, severity levels, and recommendation texts in the Excel workbook MUST strictly adhere to the active language configuration (`--lang es` or `--lang en`) with zero mixed slash-separated strings (`EN / ES`).

#### Scenario: Full Spanish localization
- GIVEN an audit execution configured with `--lang es`
- WHEN generating the Excel workbook
- THEN all 13 worksheet titles MUST be in Spanish
- AND all column headers MUST be pure Spanish
- AND zero headers with bilingual slashes shall be produced.

#### Scenario: Full English localization
- GIVEN an audit execution configured with `--lang en`
- WHEN generating the Excel workbook
- THEN all 13 worksheet titles MUST be in English
- AND all column headers MUST be pure English.
