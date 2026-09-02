# Delta for Excel Report Exporter

## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Executive Summary Dashboard Layout & Grid Alignment
The `Executive Summary` dashboard sheet MUST include executive title banner, metadata summary (author, CISO role, date), overall numerical score KPI card, total domains card, critical findings card, high findings card, average compliance KPI card, and an unbounded findings table where headers and findings rows span the exact column envelope (A for ID, B:C for Domain, D:E for Control, F:I for Description, J:K for Severity, L:N for Action) using merged cells with unified borders. KPI summary cards MUST use dynamic OpenPyXL formulas referencing detailed sheets, with CISO Score and Average Compliance referencing column AB of the Consolidated Summary worksheet.
(Previously: Referenced column X of the Consolidated Summary worksheet)

#### Scenario: Exporting complete multi-domain findings with merged grid and dynamic formulas
- GIVEN an audit execution of multiple domains yielding critical and high findings
- WHEN generating the Executive Summary dashboard sheet
- THEN the system MUST render all critical and high findings in the table starting at row 10
- AND each finding row MUST merge `B:C`, `D:E`, `F:I`, `J:K`, and `L:N`
- AND display its ID, Domain, Control, Description, Severity, and Recommended Action
- AND the sheet background styling MUST dynamically encompass all generated rows
- AND KPI cards for Total Domains, Critical Findings, and High Findings MUST contain valid Excel formulas referencing detailed sheets
- AND the Average Compliance card MUST contain a formula evaluating the mean compliance referencing column AB of the Consolidated Summary worksheet.
