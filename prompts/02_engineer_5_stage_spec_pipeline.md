# Prompt 02: Software Engineer 5-Stage Spec Pipeline & Spanner Graph Impact Analysis

## Goal of Using This Prompt
Demonstrates **Persona 1 (Software Engineer)** using `Archetype 1 (fsi-01-sentinel-spec-refiner)` and `Archetype 2 (fsi-02-explorer-doku-miner)` to run Socratic requirement refinement (`/pm-grill-me`) and sub-200ms 10M-LoC Spanner Graph impact analysis before writing code.

## Copy-Paste Prompt
```text
Delegate to fsi_01_sentinel_spec_refiner and fsi_02_explorer_doku_miner:
1. Run /pm-grill-me and /write-prd on Story COREMOD-4821 (migrating legacy/trace_sepa_instant_cutoff.xslt and legacy/secoffice_limit_check.apt into Java 21).
2. Run multi-hop impact analysis against data/spanner_graph/enterprise_sdlc_knowledge_graph.gql and update docs/living_architecture_sepa.md with the C4 component and BaFin MaRisk AT 7.2 traceability matrix.
```
