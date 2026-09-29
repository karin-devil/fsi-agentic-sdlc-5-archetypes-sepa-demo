---
name: pm-grill-me
description: "Stage 2 of EuroBank's 5-Stage Spec Pipeline (/ideate -> /pm-grill-me -> /write-prd -> /red-team-prd -> /decompose-epic): Conducts Socratic requirement hardening for Product Owners and Engineers before code generation."
---

# Socratic Requirement Interrogation Skill (`pm-grill-me`)

## Purpose
Extends the existing `spec-kit` foundation across EuroBank's Software Engineers and 1,500 Product Owners / Business Analysts (`CAPCom` VDI `A-23`). Before any code is generated, `pm-grill-me` interrogates draft Jira/PLM stories across 4 mandatory banking dimensions:

1. **Monetary Precision & Rounding**: Which rounding mode applies (`HALF_EVEN` vs `HALF_UP`), and what is the exact decimal scale?
2. **Boundary Inclusivity**: Are cutoff thresholds (`10,000 ms`, `€100,000.00`) inclusive (`<=`) or exclusive (`<`)?
3. **ISO-20022 & Legacy Error Taxonomy**: What exact `pacs.002` status reason code and legacy `TRACE`/`SecOffice` rule code must be emitted on rejection?
4. **BaFin MaRisk AT 7.2 / EU DORA Auditability**: Which rejections trigger mandatory compliance escalation (`bafinAuditRequired = true`)?
