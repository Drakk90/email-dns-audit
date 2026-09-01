# Delta for Excel Report Exporter

## MODIFIED Requirements

### Requirement: Executive Summary Dashboard Layout & Grid Alignment
The `Executive Summary` dashboard sheet MUST include executive title banner, metadata summary, 5 KPI cards spanning columns A to N, and an unbounded findings table where headers and findings rows span the exact column envelope (A for ID, B:C for Domain, D:E for Control, F:I for Description, J:K for Severity, L:N for Action) using merged cells with unified borders, eliminating unmerged blank column gaps.

#### Scenario: Merged grid findings table rendering
- GIVEN a set of evaluated domain findings
- WHEN rendering the findings table in `ws_cover`
- THEN header row 9 MUST merge `B9:C9`, `D9:E9`, `F9:I9`, `J9:K9`, and `L9:N9`
- AND each finding row `idx` MUST merge `B{idx}:C{idx}`, `D{idx}:E{idx}`, `F{idx}:I{idx}`, `J{idx}:K{idx}`, and `L{idx}:N{idx}`
- AND apply consistent font and border styling across the merged row spans.

### Requirement: Infrastructure Deliverability & Certificate Health Data Population
The system MUST populate row entries for all evaluated domains in the `CAA y Salud de Certificados TLS` section of the `Complementos` / `Addons` worksheet and align all 13 columns in `Inventario_Dominios` / `Domain_Inventory`.

#### Scenario: Ingesting CAA and TLS rows into Complementos
- GIVEN audited domains with CAA and TLS probe results
- WHEN building the Excel report
- THEN the system MUST append row records into `data["caa_tls"]` for each domain
- AND render these rows under row 23 in the `Complementos` worksheet
- AND populate CAA CAs and FCrDNS status in columns 11 and 12 of `Inventario_Dominios`.
