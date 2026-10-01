#!/usr/bin/env python3
"""EuroBank AG (Tier-1 Regulated FSI) × Google Cloud — 5 Agent Archetypes & /teamwork-preview Live Demo Workbench.

Provides a fast interactive Web UI and live execution endpoints in Karina's Argolis project
(`your-gcp-project-id`, `europe-west3`) for demonstrating:
1. The 5 EuroBank Agent Archetypes (.agents/agents/*.md & 5-part handoffs)
2. The 20-Minute 5-Act /teamwork-preview CoreMod 2030 SEPA Instant Modernization Demo
3. The Lane 1 PreToolUse PII/IBAN Guardrail Hook & Live SEPA Instant Validator Playground
4. The 3 Persona Workflows (Engineer, 1,500 POs/Test Analysts, OneCI) & DASY OSCAL Dossier
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

BASE_DIR = Path(__file__).resolve().parent
DEMO_REPO = BASE_DIR / "demo_repo"
sys.path.insert(0, str(DEMO_REPO))

import verify_5_tiers  # noqa: E402

app = FastAPI(title="EuroBank AG (Tier-1 Regulated FSI)Y & /teamwork-preview Live Demo Workbench")


def _read_rel(rel_path: str) -> str:
    p = DEMO_REPO / rel_path
    return p.read_text(encoding="utf-8") if p.is_file() else f"File not found: {rel_path}"


@app.get("/api/state")
async def get_state() -> JSONResponse:
    archetype_files = [
        ("fsi-01-sentinel-spec-refiner", "Archetype 1: Sentinel & 5-Stage Spec Refiner", "Act 1 / Persona 1 (PO & Engineer)", ".agents/agents/fsi-01-sentinel-spec-refiner.md", ".agents/teamwork/handoffs/01_sentinel_handoff.md"),
        ("fsi-02-explorer-doku-miner", "Archetype 2: Explorer, Spec Miner & Spanner Graph Doku Agent", "Act 2 / 10M-LoC Spanner Graph MCP", ".agents/agents/fsi-02-explorer-doku-miner.md", ".agents/teamwork/handoffs/02_explorer_doku_handoff.md"),
        ("fsi-03-opaque-e2e-test-architect", "Archetype 3: Opaque-Box 5-Tier E2E Test Architect & BDD Synthesizer", "Act 3 (Track 2) / Persona 2 (1,500 Test Analysts)", ".agents/agents/fsi-03-opaque-e2e-test-architect.md", ".agents/teamwork/handoffs/03_opaque_test_architect_handoff.md"),
        ("fsi-04-armed-codmod-worker", "Archetype 4: Armed Modernization Worker (CodMod Java 21 Engineer)", "Act 3 (Track 1) / Exclusive Write-Owner", ".agents/agents/fsi-04-armed-codmod-worker.md", ".agents/teamwork/handoffs/04_armed_codmod_worker_handoff.md"),
        ("fsi-05-forensic-auditor-dasy-gate", "Archetype 5: 6-Eyes Reviewer, Challenger, Forensic Auditor & DASY Gate", "Act 4 & 5 / Persona 3 (OneCI & Enterprise DASY)", ".agents/agents/fsi-05-forensic-auditor-dasy-gate.md", ".agents/teamwork/handoffs/05_forensic_auditor_handoff.md"),
    ]
    archetypes = [
        {
            "id": aid,
            "title": title,
            "stage": stage,
            "path": md_path,
            "markdown": _read_rel(md_path),
            "handoff": _read_rel(h_path),
        }
        for aid, title, stage, md_path, h_path in archetype_files
    ]

    artifacts = {
        "ORIGINAL_REQUEST.md": _read_rel(".agents/teamwork/ORIGINAL_REQUEST.md"),
        "PROJECT.md": _read_rel(".agents/teamwork/PROJECT.md"),
        "TEST_INFRA.md": _read_rel(".agents/teamwork/TEST_INFRA.md"),
        "GATE_STATUS.md": _read_rel(".agents/teamwork/GATE_STATUS.md"),
        "DEAD_ENDS.md": _read_rel(".agents/teamwork/DEAD_ENDS.md"),
        "TEST_READY.md": _read_rel(".agents/teamwork/TEST_READY.md"),
        "trace_sepa_instant_cutoff.xslt": _read_rel("legacy/trace_sepa_instant_cutoff.xslt"),
        "secoffice_limit_check.apt": _read_rel("legacy/secoffice_limit_check.apt"),
        "SepaInstantValidator.java": _read_rel("src/main/java/com/fsi/payments/SepaInstantValidator.java"),
        "SepaInstantValidatorTest.java": _read_rel("src/test/java/com/fsi/payments/SepaInstantValidatorTest.java"),
        "sepa_instant_cutoff.feature": _read_rel("src/test/resources/features/sepa_instant_cutoff.feature"),
        "fsi_java21_bafin_rules.md": _read_rel(".agents/rules/fsi_java21_bafin_rules.md"),
        "living_architecture_sepa.md": _read_rel("docs/living_architecture_sepa.md"),
        "Antigravity-Business.code-profile": _read_rel("profiles/Antigravity-Business.code-profile"),
        "dasy_compliance_dossier.json": _read_rel("build/dasy_compliance_dossier.json"),
    }

    return JSONResponse({
        "project": os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id"),
        "region": "europe-west3 (Frankfurt)",
        "adk_orchestrator_url": os.environ.get(
            "ADK_ORCHESTRATOR_URL",
            "https://fsi-adk-orchestrator.europe-west3.run.app/dev-ui/",
        ),
        "archetypes": archetypes,
        "artifacts": artifacts,
    })


@app.post("/api/run-demo")
async def run_demo() -> JSONResponse:
    res = subprocess.run(
        ["bash", str(DEMO_REPO / "run_all_fsi_demos.sh")],
        cwd=str(DEMO_REPO),
        capture_output=True,
        text=True,
        timeout=60,
    )
    return JSONResponse({
        "exit_code": res.returncode,
        "output": (res.stdout or "") + ("\n" + res.stderr if res.stderr else ""),
        "dossier": _read_rel("build/dasy_compliance_dossier.json"),
    })


@app.post("/api/test-hook")
async def test_hook(req: Request) -> JSONResponse:
    body = await req.json()
    payload = body.get("payload", "")
    res = subprocess.run(
        [
            sys.executable,
            str(DEMO_REPO / ".agents" / "hooks" / "lane1_pii_iban_guard.py"),
            "--event=PreToolUse",
            f"--input-text={payload}",
        ],
        cwd=str(DEMO_REPO),
        capture_output=True,
        text=True,
        timeout=10,
    )
    try:
        parsed = json.loads(res.stdout)
    except Exception:
        parsed = {"raw": res.stdout}
    return JSONResponse({"exit_code": res.returncode, "result": parsed})


@app.post("/api/validate-sepa")
async def validate_sepa(req: Request) -> JSONResponse:
    body = await req.json()
    res = verify_5_tiers.reference_validate(
        amount_eur=str(body.get("amount_eur", "2500.00")),
        liquidity_eur=str(body.get("liquidity_eur", "150000.00")),
        elapsed_ms=int(body.get("elapsed_ms", 420)),
        debtor_iban=str(body.get("debtor_iban", "DE89500105170532013000")),
        debtor_bic=str(body.get("debtor_bic", "EUBKDEFFXXX")),
        creditor_bic=str(body.get("creditor_bic", "DEUTDEFFXXX")),
        account_status=str(body.get("account_status", "ACTIVE")),
        aml_status=str(body.get("aml_status", "CLEAR")),
    )
    return JSONResponse(res)


HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EuroBank AG (Tier-1 Regulated FSI) × Google Cloud — 5 Agent Archetypes & /teamwork-preview Live Demo Hub</title>
<style>
  :root {
    --fsi-yellow: #FFCC00;
    --fsi-petrol: #002E3C;
    --fsi-petrol-light: #004154;
    --bg: #07131a;
    --card: #0d212c;
    --border: #1b3d4f;
    --text: #eef6f9;
    --muted: #9ab5c2;
    --green: #10b981;
    --red: #ef4444;
    --blue: #38bdf8;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
  }
  header {
    background: linear-gradient(135deg, var(--fsi-petrol) 0%, #051821 100%);
    border-bottom: 3px solid var(--fsi-yellow);
    padding: 18px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 14px;
  }
  .brand-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #fff;
  }
  .brand-sub {
    font-size: 0.85rem;
    color: var(--fsi-yellow);
    margin-top: 2px;
  }
  .header-actions {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }
  .btn {
    background: var(--fsi-yellow);
    color: #00202b;
    border: none;
    padding: 9px 16px;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.85rem;
    cursor: pointer;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }
  .btn-secondary {
    background: #143342;
    color: var(--text);
    border: 1px solid var(--border);
  }
  .tabs {
    display: flex;
    gap: 6px;
    padding: 12px 28px 0;
    background: #091922;
    border-bottom: 1px solid var(--border);
    overflow-x: auto;
  }
  .tab {
    padding: 10px 18px;
    border-radius: 8px 8px 0 0;
    background: transparent;
    color: var(--muted);
    border: 1px solid transparent;
    border-bottom: none;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.9rem;
  }
  .tab.active {
    background: var(--card);
    color: var(--fsi-yellow);
    border-color: var(--border);
  }
  main {
    max-width: 1440px;
    margin: 0 auto;
    padding: 24px 28px;
  }
  .panel { display: none; }
  .panel.active { display: block; }
  .grid-5 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 12px;
    margin-bottom: 20px;
  }
  .arch-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px;
    cursor: pointer;
    transition: all 0.15s;
  }
  .arch-card.active, .arch-card:hover {
    border-color: var(--fsi-yellow);
    box-shadow: 0 0 0 1px var(--fsi-yellow);
  }
  .badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 99px;
    font-size: 0.72rem;
    font-weight: 700;
    background: rgba(255,204,0,0.15);
    color: var(--fsi-yellow);
    margin-bottom: 6px;
  }
  .split {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }
  @media (max-width: 960px) { .split { grid-template-columns: 1fr; } }
  .box {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
  }
  .box h3 {
    margin: 0 0 10px 0;
    font-size: 1rem;
    color: var(--fsi-yellow);
  }
  pre {
    background: #040d12;
    border: 1px solid #132c3a;
    border-radius: 6px;
    padding: 12px;
    overflow-x: auto;
    font-size: 0.8rem;
    color: #d6ecf5;
    max-height: 480px;
    white-space: pre-wrap;
  }
  .form-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 10px;
    margin-bottom: 12px;
  }
  label {
    display: block;
    font-size: 0.78rem;
    color: var(--muted);
    margin-bottom: 4px;
  }
  input, select {
    width: 100%;
    padding: 8px 10px;
    border-radius: 6px;
    border: 1px solid var(--border);
    background: #051118;
    color: var(--text);
    font-size: 0.85rem;
  }
  .pill-bar {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 12px;
  }
</style>
</head>
<body>
<header>
  <div>
    <div class="brand-title">EuroBank AG (Tier-1 Regulated FSI) × Google Cloud — 5 Agent Archetypes &amp; /teamwork-preview Live Workbench</div>
    <div class="brand-sub">Argolis Project: your-gcp-project-id (europe-west3 Frankfurt) | Dual-Lane AGY Architecture + CoreMod 2030 SEPA Instant Modernization</div>
  </div>
  <div class="header-actions">
    <button class="btn" onclick="executeFullDemo()">▶ Run All 5 Acts &amp; 5-Tier JVM Suite Live</button>
    <a id="adkLink" href="https://fsi-adk-orchestrator.europe-west3.run.app/dev-ui/" target="_blank" class="btn btn-secondary">🤖 Open Google ADK 2.0 Multi-Agent UI (/dev-ui/) ↗</a>
  </div>
</header>

<div class="tabs">
  <button class="tab active" onclick="switchTab('tab-archetypes', this)">1. The 5 Agent Archetypes (.agents/agents/)</button>
  <button class="tab" onclick="switchTab('tab-acts', this)">2. 20-Min 5-Act /teamwork-preview Runner</button>
  <button class="tab" onclick="switchTab('tab-playground', this)">3. Live Lane 1 PII Hook &amp; SEPA Instant Playground</button>
  <button class="tab" onclick="switchTab('tab-personas', this)">4. 3 Personas &amp; Signed DASY OSCAL 1.1.2 Dossier</button>
</div>

<main>
  <!-- TAB 1: 5 AGENT ARCHETYPES -->
  <section id="tab-archetypes" class="panel active">
    <div id="archCards" class="grid-5"></div>
    <div class="split">
      <div class="box">
        <h3 id="archSpecTitle">Agent Archetype Specification (.agents/agents/*.md)</h3>
        <pre id="archSpecPre">Loading...</pre>
      </div>
      <div class="box">
        <h3 id="archHandoffTitle">5-Part Structured Handoff (.agents/teamwork/handoffs/*.md)</h3>
        <pre id="archHandoffPre">Loading...</pre>
      </div>
    </div>
  </section>

  <!-- TAB 2: 5-ACT /teamwork-preview RUNNER -->
  <section id="tab-acts" class="panel">
    <div class="pill-bar">
      <button class="btn btn-secondary" onclick="showArtifact('ORIGINAL_REQUEST.md')">Act 1: ORIGINAL_REQUEST.md</button>
      <button class="btn btn-secondary" onclick="showArtifact('PROJECT.md')">Act 2: PROJECT.md (Mined Rules)</button>
      <button class="btn btn-secondary" onclick="showArtifact('trace_sepa_instant_cutoff.xslt')">Legacy: TRACE XSLT</button>
      <button class="btn btn-secondary" onclick="showArtifact('secoffice_limit_check.apt')">Legacy: SecOffice GuptaTD 4GL</button>
      <button class="btn btn-secondary" onclick="showArtifact('SepaInstantValidator.java')">Act 3 (Track 1): SepaInstantValidator.java</button>
      <button class="btn btn-secondary" onclick="showArtifact('SepaInstantValidatorTest.java')">Act 3 (Track 2): Opaque-Box JVM Tests</button>
      <button class="btn btn-secondary" onclick="showArtifact('GATE_STATUS.md')">Act 4: GATE_STATUS.md (6-Eyes + Forensic Veto)</button>
      <button class="btn btn-secondary" onclick="showArtifact('DEAD_ENDS.md')">Act 4: DEAD_ENDS.md</button>
      <button class="btn btn-secondary" onclick="showArtifact('TEST_READY.md')">Act 5: TEST_READY.md</button>
      <button class="btn" onclick="executeFullDemo()">▶ Execute Live 5-Tier &amp; JVM Verification Now</button>
    </div>
    <div class="split">
      <div class="box">
        <h3 id="artViewerTitle">Selected Artifact</h3>
        <pre id="artViewerPre">Select an Act artifact above...</pre>
      </div>
      <div class="box">
        <h3>Live Argolis Execution Output (`run_all_fsi_demos.sh` &amp; OpenJDK 21 JVM)</h3>
        <pre id="liveRunPre">Click "▶ Execute Live 5-Tier & JVM Verification Now" to run all 5 Acts live on Cloud Run...</pre>
      </div>
    </div>
  </section>

  <!-- TAB 3: LANE 1 HOOK & SEPA VALIDATOR PLAYGROUND -->
  <section id="tab-playground" class="panel">
    <div class="split">
      <div class="box">
        <h3>🛡️ Lane 1 PreToolUse PII / IBAN / .fsi Guardrail Tester (`.agents/hooks/lane1_pii_iban_guard.py`)</h3>
        <div class="pill-bar">
          <button class="btn btn-secondary" onclick="setHookInput('Query oracle.intranet.fsi for customer IBAN DE44500105175407324931')">Preset 1: Real IBAN + .intranet.fsi (MUST DENY)</button>
          <button class="btn btn-secondary" onclick="setHookInput('Validate synthetic SEPA Instant IBAN DE89500105170532013000')">Preset 2: Bundesbank Synthetic IBAN (MUST ALLOW)</button>
        </div>
        <label>Prompt / Tool Payload to Evaluate</label>
        <input id="hookInput" value="Query oracle.intranet.fsi for customer IBAN DE44500105175407324931" style="margin-bottom:10px;">
        <button class="btn" onclick="runHookTest()">Evaluate Lane 1 Hook Now</button>
        <pre id="hookResultPre" style="margin-top:12px;">Click "Evaluate Lane 1 Hook Now"...</pre>
      </div>

      <div class="box">
        <h3>💶 Live Java 21 SEPA Instant (`pacs.008.001.08`) Boundary &amp; HALF_EVEN Validator</h3>
        <div class="pill-bar">
          <button class="btn btn-secondary" onclick="setSepaPreset('100000.00', 10000, 'EUBKDEFFXXX', 'DEUTDEFFXXX', 'ACTIVE', 'CLEAR', '150000.00')">Boundary: €100,000.00 @ 10,000ms (ACCP)</button>
          <button class="btn btn-secondary" onclick="setSepaPreset('100000.01', 1200, 'EUBKDEFFXXX', 'DEUTDEFFXXX', 'ACTIVE', 'CLEAR', '200000.00')">+1 Cent: €100,000.01 (AM02)</button>
          <button class="btn btn-secondary" onclick="setSepaPreset('5000.00', 10001, 'EUBKDEFFXXX', 'DEUTDEFFXXX', 'ACTIVE', 'CLEAR', '50000.00')">+1 ms: 10,001ms (AB05)</button>
          <button class="btn btn-secondary" onclick="setSepaPreset('15000.00', 400, 'EUBKDEFFXXX', 'DEUTDEFFXXX', 'ACTIVE', 'FREEZE', '50000.00')">BaFin AML Freeze (RR04)</button>
        </div>
        <div class="form-row">
          <div><label>Amount (EUR)</label><input id="sepaAmt" value="100000.00"></div>
          <div><label>Latency (ms)</label><input id="sepaMs" type="number" value="10000"></div>
          <div><label>Creditor BIC</label><input id="sepaBic" value="DEUTDEFFXXX"></div>
          <div><label>Account Status</label><select id="sepaAcct"><option>ACTIVE</option><option>CLOSED</option></select></div>
          <div><label>BaFin AML Status</label><select id="sepaAml"><option>CLEAR</option><option>FREEZE</option></select></div>
          <div><label>Liquidity (EUR)</label><input id="sepaLiq" value="150000.00"></div>
        </div>
        <button class="btn" onclick="runSepaValidate()">Validate SEPA Instant Payment</button>
        <pre id="sepaResultPre" style="margin-top:12px;">Click "Validate SEPA Instant Payment"...</pre>
      </div>
    </div>
  </section>

  <!-- TAB 4: 3 PERSONAS & DASY OSCAL DOSSIER -->
  <section id="tab-personas" class="panel">
    <div class="pill-bar">
      <button class="btn btn-secondary" onclick="showPersonaDoc('sepa_instant_cutoff.feature')">Persona 2 (1,500 Test Analysts): Cucumber BDD (.feature)</button>
      <button class="btn btn-secondary" onclick="showPersonaDoc('Antigravity-Business.code-profile')">Persona 2: CAPCom VDI Profile (.code-profile)</button>
      <button class="btn btn-secondary" onclick="showPersonaDoc('living_architecture_sepa.md')">Persona 1: Spanner Graph Doku Agent C4 Output</button>
      <button class="btn btn-secondary" onclick="showPersonaDoc('fsi_java21_bafin_rules.md')">Engineering Rules: fsi_java21_bafin_rules.md</button>
    </div>
    <div class="split">
      <div class="box">
        <h3 id="personaDocTitle">Persona Deliverable (`sepa_instant_cutoff.feature`)</h3>
        <pre id="personaDocPre">Loading...</pre>
      </div>
      <div class="box">
        <h3>📋 Governance Lead's Signed DASY OSCAL 1.1.2 Compliance Dossier (`build/dasy_compliance_dossier.json`)</h3>
        <pre id="oscalPre">Loading...</pre>
      </div>
    </div>
  </section>
</main>

<script>
let STATE = null;

function switchTab(id, btn) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
}

function selectArchetype(idx) {
  const arch = STATE.archetypes[idx];
  document.querySelectorAll('.arch-card').forEach((c, i) => c.classList.toggle('active', i === idx));
  document.getElementById('archSpecTitle').textContent = arch.title + ' (' + arch.path + ')';
  document.getElementById('archSpecPre').textContent = arch.markdown;
  document.getElementById('archHandoffTitle').textContent = '5-Part Handoff — ' + arch.id;
  document.getElementById('archHandoffPre').textContent = arch.handoff;
}

function showArtifact(name) {
  document.getElementById('artViewerTitle').textContent = name;
  document.getElementById('artViewerPre').textContent = STATE.artifacts[name] || '';
}

function showPersonaDoc(name) {
  document.getElementById('personaDocTitle').textContent = name;
  document.getElementById('personaDocPre').textContent = STATE.artifacts[name] || '';
}

async function executeFullDemo() {
  const pre = document.getElementById('liveRunPre');
  pre.textContent = 'Running run_all_fsi_demos.sh (5 Agent Archetypes + 5-Tier JVM Suite + DASY OSCAL Exporter)...';
  const res = await fetch('/api/run-demo', {method: 'POST'});
  const data = await res.json();
  pre.textContent = data.output;
  document.getElementById('oscalPre').textContent = data.dossier;
}

function setHookInput(val) {
  document.getElementById('hookInput').value = val;
  runHookTest();
}

async function runHookTest() {
  const payload = document.getElementById('hookInput').value;
  const res = await fetch('/api/test-hook', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({payload})
  });
  const data = await res.json();
  document.getElementById('hookResultPre').textContent =
    'Hook Exit Code: ' + data.exit_code + '\\n\\n' + JSON.stringify(data.result, null, 2);
}

function setSepaPreset(amt, ms, dbic, cbic, acct, aml, liq) {
  document.getElementById('sepaAmt').value = amt;
  document.getElementById('sepaMs').value = ms;
  document.getElementById('sepaBic').value = cbic;
  document.getElementById('sepaAcct').value = acct;
  document.getElementById('sepaAml').value = aml;
  document.getElementById('sepaLiq').value = liq;
  runSepaValidate();
}

async function runSepaValidate() {
  const body = {
    amount_eur: document.getElementById('sepaAmt').value,
    elapsed_ms: parseInt(document.getElementById('sepaMs').value, 10),
    creditor_bic: document.getElementById('sepaBic').value,
    account_status: document.getElementById('sepaAcct').value,
    aml_status: document.getElementById('sepaAml').value,
    liquidity_eur: document.getElementById('sepaLiq').value
  };
  const res = await fetch('/api/validate-sepa', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(body)
  });
  const data = await res.json();
  document.getElementById('sepaResultPre').textContent = JSON.stringify(data, null, 2);
}

async function init() {
  const res = await fetch('/api/state');
  STATE = await res.json();
  document.getElementById('adkLink').href = STATE.adk_orchestrator_url;
  const cardsEl = document.getElementById('archCards');
  cardsEl.innerHTML = STATE.archetypes.map((a, i) => `
    <div class="arch-card ${i===0?'active':''}" onclick="selectArchetype(${i})">
      <div class="badge">${a.stage}</div>
      <div style="font-weight:700;font-size:0.92rem;color:#fff;">${a.title}</div>
      <div style="font-size:0.78rem;color:#9ab5c2;margin-top:4px;"><code>${a.id}</code></div>
    </div>
  `).join('');
  selectArchetype(0);
  showArtifact('PROJECT.md');
  showPersonaDoc('sepa_instant_cutoff.feature');
  document.getElementById('oscalPre').textContent = STATE.artifacts['dasy_compliance_dossier.json'];
  runHookTest();
  runSepaValidate();
}
init();
</script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse(HTML_PAGE)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    uvicorn.run(app, host="0.0.0.0", port=port)
