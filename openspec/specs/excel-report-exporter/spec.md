# Excel Report Exporter Specification

## Purpose
Generate formatted, multi-tab Microsoft Excel (.xlsx) workbooks designed for executive CISO reviews, audit teams, and remediation engineers without external service dependencies.

## Requirements

### Requirement: Multi-Tab Executive Workbook Structure & Column Integrity
The system MUST generate an `.xlsx` workbook containing structured sheets including a single executive summary dashboard (`Resumen` or `Summary`), `Inventario_Dominios` / `Domain_Inventory`, `SPF`, `DKIM`, `DMARC`, `DNSSEC`, `Complementos` / `Addons`, `Remitentes_Autorizados` / `Authorized_Senders`, `Hallazgos` / `Findings`, `Superficie_Ataque_Typosquats` / `Attack_Surface_Typosquats`, `Matriz_Cumplimiento_CISO` / `CISO_Compliance_Matrix`, and `Resumen_Consolidado`. The workbook MUST NOT contain duplicate or numbered suffix summary sheets (such as `Resumen1` or `Summary1`), MUST align all 13 columns in `Inventario_Dominios`, and MUST populate all data rows in `Complementos`.

#### Scenario: Single executive dashboard generation
- GIVEN a completed domain evaluation dataset
- WHEN the exporter creates the Excel workbook
- THEN the system MUST produce exactly one executive dashboard sheet at index 0 titled `Resumen` (when `--lang es`) or `Summary` (when `--lang en`)
- AND the workbook MUST NOT contain any colliding `Resumen1` or `Summary1` sheets.

### Requirement: Executive Summary Dashboard Layout & Grid Alignment
The `Executive Summary` dashboard sheet MUST include executive title banner, metadata summary (author, CISO role, date), overall numerical score KPI card, total domains card, critical findings card, high findings card, average compliance KPI card, and an unbounded findings table where headers and findings rows span the exact column envelope (A for ID, B:C for Domain, D:E for Control, F:I for Description, J:K for Severity, L:N for Action) using merged cells with unified borders, eliminating unmerged blank column gaps.

#### Scenario: Exporting complete multi-domain findings with merged grid
- GIVEN an audit execution of multiple domains yielding critical and high findings
- WHEN generating the Executive Summary dashboard sheet
- THEN the system MUST render all critical and high findings in the table starting at row 10
- AND each finding row MUST merge `B:C`, `D:E`, `F:I`, `J:K`, and `L:N`
- AND display its ID, Domain, Control, Description, Severity, and Recommended Action
- AND the sheet background styling MUST dynamically encompass all generated rows.

### Requirement: Granular Findings and Typosquats Data Tables
The system MUST export detailed findings with RFC references in `Email & DNS Posture` and resolved IP/MX status for each generated lookalike in `Attack Surface & Typosquats`.

#### Scenario: Exporting typosquatting threat table
- GIVEN 20 discovered lookalike domain candidates
- WHEN exporting the Attack Surface worksheet
- THEN the system MUST tabulate Candidate Domain, Mutation Type (Homoglyph/Bitsquat), Registration Status, Resolved IPs, and Threat Level.

### Requirement: Infrastructure Deliverability & Certificate Health Data Population
The system MUST include dedicated columns and populated data rows for CAA governance, FCrDNS PTR status, and TLS certificate expiration days in the generated Excel worksheets.

#### Scenario: Ingesting CAA and TLS rows into Complementos
- GIVEN domain audit results containing CAA policies and MX FCrDNS evaluations
- WHEN generating the Excel report
- THEN the system MUST append row records into `data["caa_tls"]` for each domain
- AND render these rows under row 23 in the `Complementos` worksheet
- AND populate CAA CAs and FCrDNS status in columns 11 and 12 of `Inventario_Dominios`.

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
