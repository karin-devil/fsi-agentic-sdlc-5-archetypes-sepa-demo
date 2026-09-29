---
name: sepa-modernization
description: "AppRaMo 2030 Legacy Modernization Skill: Guides translation of TRACE XML/XSLT stylesheets and SecOffice Gupta Team Developer (.apt) 4GL modules into high-assurance Java 21 / Spring Boot 3.4 microservices."
---

# AppRaMo 2030 SEPA Instant Modernization Skill (`sepa-modernization`)

## Overview
Standardizes the migration of EuroBank's legacy payment and settlement components (`TRACE` XSLT 1.0/2.0 stylesheets and `SecOffice` Gupta Team Developer `.apt` 4GL routines) into Java 21 (`SepaInstantValidator.java`).

## Mandatory Mapping Table
| Legacy Artifact | Legacy Construct | Target Java 21 Construct | ISO-20022 Code |
|---|---|---|---|
| `trace_sepa_instant_cutoff.xslt` | `elapsed_ms > 10000` (`SCT_INST_TIMEOUT_10S`) | `elapsedMs > 10_000L` | `AB05` |
| `trace_sepa_instant_cutoff.xslt` | `substring(bic, 1, 4) = 'XX00'` (`AT_018_INVALID_BIC_ROUTING`) | `BIC_PATTERN` & `!bic.startsWith("XX00")` | `RC01` |
| `secoffice_limit_check.apt` | `nAmount > 100000.00` (`SECOFFICE_LIMIT_EXCEEDED_100K`) | `roundedAmount.compareTo(MAX_INSTANT_AMOUNT_EUR) > 0` | `AM02` |
| `secoffice_limit_check.apt` | `SalNumberRound(nAmount * 0.0015, 2)` | `BigDecimal.multiply(FEE_RATE).setScale(2, RoundingMode.HALF_EVEN)` | N/A |
| `secoffice_limit_check.apt` | `sAmlStatus = 'FREEZE'` (`DE_BAFIN_AML_FREEZE`) | `"FREEZE".equalsIgnoreCase(req.amlStatus())` | `RR04` |
| `secoffice_limit_check.apt` | `nAvailLiquidity < nAmount` (`INSUFFICIENT_LIQUIDITY`) | `req.availableLiquidityEur().compareTo(roundedAmount) < 0` | `AM04` |
