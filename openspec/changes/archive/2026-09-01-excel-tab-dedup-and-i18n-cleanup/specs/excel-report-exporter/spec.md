# Delta for Excel Report Exporter

## MODIFIED Requirements

### Requirement: Multi-Tab Executive Workbook Structure
The system MUST generate an `.xlsx` workbook containing structured sheets including a single executive summary dashboard (`Resumen` or `Summary`), `Inventario_Dominios` / `Domain_Inventory`, `SPF`, `DKIM`, `DMARC`, `DNSSEC`, `Complementos` / `Addons`, `Remitentes_Autorizados` / `Authorized_Senders`, `Hallazgos` / `Findings`, `Superficie_Ataque_Typosquats` / `Attack_Surface_Typosquats`, `Matriz_Cumplimiento_CISO` / `CISO_Compliance_Matrix`, and `Resumen_Consolidado`. The workbook MUST NOT contain duplicate or numbered suffix summary sheets (such as `Resumen1` or `Summary1`).

#### Scenario: Single executive dashboard generation
- GIVEN a completed domain evaluation dataset
- WHEN the exporter creates the Excel workbook
- THEN the system MUST produce exactly one executive dashboard sheet at index 0 titled `Resumen` (when `--lang es`) or `Summary` (when `--lang en`)
- AND the workbook MUST NOT contain any colliding `Resumen1` or `Summary1` sheets.

### Requirement: Executive Summary Dashboard Layout
The `Executive Summary` dashboard sheet MUST include executive title banner, metadata summary (author, CISO role, date), overall numerical score KPI card, total domains card, critical findings card, high findings card, average compliance KPI card, and a top priority findings table displaying the top critical and high severity findings.

#### Scenario: Exporting executive dashboard cards
- GIVEN audit results with calculated findings and compliance scores
- WHEN generating the executive summary sheet
- THEN the system MUST render formatted metric cards (Total Domains, Critical Findings, High Findings, CISO Risk Score, Average Compliance) with distinct color fills
- AND render a top findings table with ID, Domain, Control, Description, Severity, and Recommendation columns.

## ADDED Requirements

### Requirement: Strict Language Domain Localization
All worksheet titles, table column headers, KPI card labels, status strings, severity levels, and recommendation texts in the Excel workbook MUST strictly adhere to the active language configuration (`--lang es` or `--lang en`) with zero mixed slash-separated strings (`EN / ES`).

#### Scenario: Full Spanish localization
- GIVEN an audit execution configured with `--lang es`
- WHEN generating the Excel workbook
- THEN all 13 worksheet titles MUST be in Spanish
- AND all column headers MUST be pure Spanish (e.g. `Tipo`, `Marca / Entidad`, `Fecha de Expiración`, `Emisor de Correo`, `Propietario Interno`, `Acción Recomendada`)
- AND zero headers with bilingual slashes (e.g. `Type / Tipo`) shall be produced.

#### Scenario: Full English localization
- GIVEN an audit execution configured with `--lang en`
- WHEN generating the Excel workbook
- THEN all 13 worksheet titles MUST be in English (e.g. `Summary`, `Domain_Inventory`, `Findings`, `Attack_Surface_Typosquats`, `CISO_Compliance_Matrix`)
- AND all column headers MUST be pure English.
