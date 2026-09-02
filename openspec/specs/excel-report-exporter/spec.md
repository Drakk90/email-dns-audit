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
The `Executive Summary` dashboard sheet MUST include executive title banner, metadata summary (author, CISO role, date), overall numerical score KPI card, total domains card, critical findings card, high findings card, average compliance KPI card, and an unbounded findings table where headers and findings rows span the exact column envelope (A for ID, B:C for Domain, D:E for Control, F:I for Description, J:K for Severity, L:N for Action) using merged cells with unified borders. KPI summary cards MUST use dynamic OpenPyXL formulas referencing detailed sheets, with CISO Score and Average Compliance referencing column AB of the Consolidated Summary worksheet.

#### Scenario: Exporting complete multi-domain findings with merged grid and dynamic formulas
- GIVEN an audit execution of multiple domains yielding critical and high findings
- WHEN generating the Executive Summary dashboard sheet
- THEN the system MUST render all critical and high findings in the table starting at row 10
- AND each finding row MUST merge `B:C`, `D:E`, `F:I`, `J:K`, and `L:N`
- AND display its ID, Domain, Control, Description, Severity, and Recommended Action
- AND the sheet background styling MUST dynamically encompass all generated rows
- AND KPI cards for Total Domains, Critical Findings, and High Findings MUST contain valid Excel formulas referencing detailed sheets
- AND the Average Compliance card MUST contain a formula evaluating the mean compliance referencing column AB of the Consolidated Summary worksheet.

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

### Requirement: Bilingual Dynamic Formula Generation
The Excel exporter MUST render all formulas using standard OOXML function identifiers (`COUNTA`, `COUNTIF`, `AVERAGE`) while dynamically resolving localized sheet names and filter criteria matching the active language (`--lang es` or `--lang en`).

#### Scenario: Dynamic formulas in Spanish audit
- GIVEN an audit configured with `--lang es`
- WHEN generating the executive cover sheet
- THEN the Total Domains cell MUST contain `=COUNTA('Inventario_Dominios'!B2:B{N})`
- AND the Critical Findings cell MUST contain `=COUNTIF('Hallazgos'!E2:E{N}, "Crítica")`
- AND the High Findings cell MUST contain `=COUNTIF('Hallazgos'!E2:E{N}, "Alta")`.

#### Scenario: Dynamic formulas in English audit
- GIVEN an audit configured with `--lang en`
- WHEN generating the executive cover sheet
- THEN the Total Domains cell MUST contain `=COUNTA('Domain_Inventory'!B2:B{N})`
- AND the Critical Findings cell MUST contain `=COUNTIF('Findings'!E2:E{N}, "Critical")`
- AND the High Findings cell MUST contain `=COUNTIF('Findings'!E2:E{N}, "High")`.

### Requirement: Formulated Consolidated Summary Scoring Breakdown
The system MUST include four dedicated, formulated score breakdown columns in `Resumen_Consolidado` / `Consolidated_Summary` corresponding to the CISO security pillars (Authentication, Transport, DNS/Identity, and EASM), and calculate the `Cumplimiento Global` / `Global Compliance` column via an Excel sum formula divided by 100 with `0.0%` number format.

#### Scenario: Formulating 4-pillar sub-scores and global compliance percentage
- GIVEN a consolidated domain audit result in `Resumen_Consolidado`
- WHEN the exporter writes each domain row
- THEN column X (`Score Autenticación (40)`) MUST contain an Excel formula evaluating SPF, DMARC, and DKIM
- AND column Y (`Score Transporte (25)`) MUST contain an Excel formula evaluating MTA-STS and TLS-RPT
- AND column Z (`Score DNS/Identidad (20)`) MUST contain an Excel formula evaluating DNSSEC and BIMI
- AND column AA (`Score Superficie EASM (15)`) MUST contain an Excel formula evaluating lookalike penalties
- AND column AB (`Cumplimiento Global`) MUST contain `=(X{r}+Y{r}+Z{r}+AA{r})/100` with number format `0.0%`.

#### Scenario: Dynamic formula references across bilingual worksheets
- GIVEN an audit executed with `--lang es` or `--lang en`
- WHEN generating the 4 pillar formulas in the consolidated summary
- THEN cross-sheet references in column X and AA MUST target the localized sheet names (`DKIM` or `Superficie_Ataque_Typosquats` / `Attack_Surface_Typosquats`)
- AND criteria matching strings MUST resolve to the active language without formula syntax errors.
