# Archive Report: Formulated Consolidated Scoring Columns

## Overview
- **Change**: `formulated-consolidated-scoring-columns`
- **Completed**: 2026-09-02
- **Verdict**: PASS

## Work Shipped
1. Added 4 formulated scoring breakdown columns in `Resumen_Consolidado` / `Consolidated_Summary`:
   - Column X: `Score Autenticación (40)` / `Auth Score (40)`
   - Column Y: `Score Transporte (25)` / `Transport Score (25)`
   - Column Z: `Score DNS/Identidad (20)` / `DNS & Identity Score (20)`
   - Column AA: `Score Superficie EASM (15)` / `EASM Score (15)`
2. Formulated `Cumplimiento Global` / `Global Compliance` in column AB:
   - Evaluated as `=(X{r} + Y{r} + Z{r} + AA{r}) / 100` with number format `0.0%`.
3. Retargeted Executive Summary cover sheet KPI cards `M5` (`Cumplimiento Promedio`) and `J5` (`Score CISO`) to calculate dynamic averages across column `AB`.
4. Full bilingual support in English and Spanish across sheet cross-references and table headers.

## Verification
- Unit test suite: 3/3 passed.
- Live executions in `--lang es` and `--lang en` verified cleanly.
