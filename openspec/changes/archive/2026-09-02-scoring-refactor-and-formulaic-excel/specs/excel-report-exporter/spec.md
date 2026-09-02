# Delta for Excel Report Exporter

## MODIFIED Requirements

### Requirement: Executive Summary Dashboard Layout & Grid Alignment
The `Executive Summary` dashboard sheet MUST include executive title banner, metadata summary (author, CISO role, date), overall numerical score KPI card, total domains card, critical findings card, high findings card, average compliance KPI card, and an unbounded findings table where headers and findings rows span the exact column envelope (A for ID, B:C for Domain, D:E for Control, F:I for Description, J:K for Severity, L:N for Action) using merged cells with unified borders. KPI summary cards MUST use dynamic OpenPyXL formulas instead of static string or integer literals, and store compliance as a numeric value formatted as a percentage.
(Previously: Rendered static literal strings and integers in KPI card row 5)

#### Scenario: Exporting complete multi-domain findings with merged grid and dynamic formulas
- GIVEN an audit execution of multiple domains yielding critical and high findings
- WHEN generating the Executive Summary dashboard sheet
- THEN the system MUST render all critical and high findings in the table starting at row 10
- AND each finding row MUST merge `B:C`, `D:E`, `F:I`, `J:K`, and `L:N`
- AND display its ID, Domain, Control, Description, Severity, and Recommended Action
- AND the sheet background styling MUST dynamically encompass all generated rows
- AND KPI cards for Total Domains, Critical Findings, and High Findings MUST contain valid Excel formulas referencing detailed sheets
- AND the Average Compliance card MUST contain a formula evaluating the mean compliance.

## ADDED Requirements

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
