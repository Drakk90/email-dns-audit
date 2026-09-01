# Excel Report Exporter Specification

## Purpose
Generate formatted, multi-tab Microsoft Excel (.xlsx) workbooks designed for executive CISO reviews, audit teams, and remediation engineers without external service dependencies.

## Requirements

### Requirement: Multi-Tab Executive Workbook Structure
The system MUST generate an `.xlsx` workbook containing at least 4 structured sheets: `Executive Summary`, `Email & DNS Posture`, `Attack Surface & Typosquats`, and `Compliance Matrix`.

#### Scenario: Successful multi-tab generation
- GIVEN a completed domain evaluation dataset
- WHEN the exporter writes the output file
- THEN the system MUST produce a valid `.xlsx` file containing all 4 formatted worksheets with professional headers, severity color-coding (Red/Amber/Green), and column auto-widths.

### Requirement: Executive Summary Dashboard Layout
The `Executive Summary` sheet MUST include domain metadata, overall numerical score (0-100), letter grade (A-F), total findings count categorized by severity (Critical, High, Medium, Low, Info), and prioritized top 3 remediation actions.

#### Scenario: Exporting executive summary metrics
- GIVEN domain audit results with 2 Critical and 3 Medium findings
- WHEN generating the Executive Summary worksheet
- THEN the system MUST render summary metric cards with formatted KPIs and highlighted remediation actions.

### Requirement: Granular Findings and Typosquats Data Tables
The system MUST export detailed findings with RFC references in `Email & DNS Posture` and resolved IP/MX status for each generated lookalike in `Attack Surface & Typosquats`.

#### Scenario: Exporting typosquatting threat table
- GIVEN 20 discovered lookalike domain candidates
- WHEN exporting the Attack Surface worksheet
- THEN the system MUST tabulate Candidate Domain, Mutation Type (Homoglyph/Bitsquat), Registration Status, Resolved IPs, and Threat Level.
