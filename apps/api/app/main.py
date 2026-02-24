"""LedgerLive — Finance Ops Close Agent API

This is the main FastAPI application entry point.
PROJECT_ID: LEDGERLIVE
"""
from __future__ import annotations

import uuid
import datetime as dt
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_MODE, PROJECT_ID, LLM_PROVIDER


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan — startup / shutdown."""
    print(f"[LedgerLive] Starting in {APP_MODE} mode | LLM={LLM_PROVIDER}")
    yield
    print("[LedgerLive] Shutting down")


app = FastAPI(
    title="LedgerLive API",
    description="Finance Ops Close Agent",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────
@app.get("/healthz")
async def healthz():
    return {
        "project": PROJECT_ID,
        "status": "ok",
        "mode": APP_MODE,
        "llm": LLM_PROVIDER,
        "ts": dt.datetime.utcnow().isoformat(),
    }


# ── Audit event spine ────────────────────────────────────────────────
AUDIT_LOG: list[dict] = []


def emit_audit_event(
    action: str,
    entity_type: str,
    entity_id: str,
    detail: dict | None = None,
    trace_id: str | None = None,
) -> dict:
    """Append-only audit event emitter. Every state mutation MUST call this."""
    event = {
        "event_id": str(uuid.uuid4()),
        "trace_id": trace_id or str(uuid.uuid4()),
        "ts": dt.datetime.utcnow().isoformat(),
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "detail": detail or {},
    }
    AUDIT_LOG.append(event)
    return event


@app.get("/api/audit")
async def get_audit_log(limit: int = 100):
    """Return the most recent audit events."""
    return {"events": AUDIT_LOG[-limit:], "total": len(AUDIT_LOG)}


# ── Wave routers will be registered below this line ──────────────────
from app.routers.w01_close_period import router as w01_router
from app.routers.w02_entity import router as w02_router
from app.routers.w03_document_store import router as w03_router
from app.routers.w04_ocr_pipeline import router as w04_router
from app.routers.w05_extraction import router as w05_router
from app.routers.w06_reconciliation import router as w06_router
from app.routers.w07_exception import router as w07_router
from app.routers.w08_review_queue import router as w08_router
from app.routers.w09_evidence_binder import router as w09_router
from app.routers.w10_eval_harness import router as w10_router
from app.routers.w11_tenant import router as w11_router
from app.routers.w12_auth import router as w12_router
from app.routers.w13_workflow import router as w13_router
from app.routers.w14_notification import router as w14_router
from app.routers.w15_connector import router as w15_router
from app.routers.w16_vendor_master import router as w16_router
from app.routers.w17_chart_of_accounts import router as w17_router
from app.routers.w18_continuous_close import router as w18_router
from app.routers.w19_audit_integrity import router as w19_router
from app.routers.w20_signed_export import router as w20_router
from app.routers.w21_report import router as w21_router
from app.routers.w22_search_index import router as w22_router
from app.routers.w23_compliance_bundle import router as w23_router
from app.routers.w24_retention import router as w24_router
from app.routers.w25_data_privacy import router as w25_router
from app.routers.w26_performance import router as w26_router
from app.routers.w27_release_bundle import router as w27_router
from app.routers.w28_judge_demo import router as w28_router
from app.routers.w29_deploy_config import router as w29_router
from app.routers.w30_hardening import router as w30_router

app.include_router(w01_router)
app.include_router(w02_router)
app.include_router(w03_router)
app.include_router(w04_router)
app.include_router(w05_router)
app.include_router(w06_router)
app.include_router(w07_router)
app.include_router(w08_router)
app.include_router(w09_router)
app.include_router(w10_router)
app.include_router(w11_router)
app.include_router(w12_router)
app.include_router(w13_router)
app.include_router(w14_router)
app.include_router(w15_router)
app.include_router(w16_router)
app.include_router(w17_router)
app.include_router(w18_router)
app.include_router(w19_router)
app.include_router(w20_router)
app.include_router(w21_router)
app.include_router(w22_router)
app.include_router(w23_router)
app.include_router(w24_router)
app.include_router(w25_router)
app.include_router(w26_router)
app.include_router(w27_router)
app.include_router(w28_router)
app.include_router(w29_router)
app.include_router(w30_router)

from app.routers.w31_close_calendar import router as w31_router
from app.routers.w32_consolidation import router as w32_router
from app.routers.w33_je_posting import router as w33_router
from app.routers.w34_three_way_match import router as w34_router
from app.routers.w35_cash_application import router as w35_router
from app.routers.w36_accruals_deferrals import router as w36_router
from app.routers.w37_controls_catalog import router as w37_router
from app.routers.w38_audit_portal import router as w38_router
from app.routers.w39_vendor_master_v2 import router as w39_router
from app.routers.w40_evidence_binder_v2 import router as w40_router
from app.routers.w41_connector_framework_v2 import router as w41_router
from app.routers.w42_qbo_connector import router as w42_router
from app.routers.w43_xero_connector import router as w43_router
from app.routers.w44_plaid_connector import router as w44_router
from app.routers.w45_mapping_studio import router as w45_router
from app.routers.w46_data_quality import router as w46_router
from app.routers.w47_continuous_close_v2 import router as w47_router
from app.routers.w48_perf_suite import router as w48_router
from app.routers.w49_release_bundle_v2 import router as w49_router
from app.routers.w50_judge_demo_v2 import router as w50_router
from app.routers.w51_budgeting import router as w51_router
from app.routers.w52_forecasting import router as w52_router
from app.routers.w53_driver_planning import router as w53_router
from app.routers.w54_scenario_engine import router as w54_router
from app.routers.w55_treasury import router as w55_router
from app.routers.w56_covenants import router as w56_router
from app.routers.w57_cost_allocation import router as w57_router
from app.routers.w58_kpi_framework import router as w58_router
from app.routers.w59_board_pack import router as w59_router
from app.routers.w60_ops_bundle import router as w60_router

app.include_router(w31_router)
app.include_router(w32_router)
app.include_router(w33_router)
app.include_router(w34_router)
app.include_router(w35_router)
app.include_router(w36_router)
app.include_router(w37_router)
app.include_router(w38_router)
app.include_router(w39_router)
app.include_router(w40_router)
app.include_router(w41_router)
app.include_router(w42_router)
app.include_router(w43_router)
app.include_router(w44_router)
app.include_router(w45_router)
app.include_router(w46_router)
app.include_router(w47_router)
app.include_router(w48_router)
app.include_router(w49_router)
app.include_router(w50_router)
app.include_router(w51_router)
app.include_router(w52_router)
app.include_router(w53_router)
app.include_router(w54_router)
app.include_router(w55_router)
app.include_router(w56_router)
app.include_router(w57_router)
app.include_router(w58_router)
app.include_router(w59_router)
app.include_router(w60_router)

from app.routers.w061_testid_guard import router as w061_router
from app.routers.w062_e2e_ops import router as w062_router
from app.routers.w063_route_sweep import router as w063_router
from app.routers.w064_role_sweep import router as w064_router
from app.routers.w065_close_flow_e2e import router as w065_router
from app.routers.w066_integration_flow_e2e import router as w066_router
from app.routers.w067_fpa_flow_e2e import router as w067_router
from app.routers.w068_determinism_harness import router as w068_router
from app.routers.w069_tour_spec import router as w069_router
from app.routers.w070_e2e_gate import router as w070_router
from app.routers.w071_exception_classifier import router as w071_router
from app.routers.w072_auto_fix import router as w072_router
from app.routers.w073_accrual_suggest import router as w073_router
from app.routers.w074_je_suggest import router as w074_router
from app.routers.w075_triage_queue_v2 import router as w075_router
from app.routers.w076_recon_explain import router as w076_router
from app.routers.w077_no_floating_claim import router as w077_router
from app.routers.w078_close_scorecard import router as w078_router
from app.routers.w079_binder_v3 import router as w079_router
from app.routers.w080_exc_flow_e2e import router as w080_router
from app.routers.w081_intercompany_v2 import router as w081_router
from app.routers.w082_fx_v3 import router as w082_router
from app.routers.w083_cashflow_consol import router as w083_router
from app.routers.w084_statement_notes import router as w084_router
from app.routers.w085_consol_adj_lock import router as w085_router
from app.routers.w086_multi_entity_cal import router as w086_router
from app.routers.w087_consol_e2e import router as w087_router
from app.routers.w088_consol_regression import router as w088_router
from app.routers.w089_consol_perf import router as w089_router
from app.routers.w090_consol_tour import router as w090_router
from app.routers.w091_workflow_plugin import router as w091_router
from app.routers.w092_workflow_marketplace import router as w092_router
from app.routers.w093_report_marketplace import router as w093_router
from app.routers.w094_mapping_marketplace import router as w094_router
from app.routers.w095_template_governance import router as w095_router
from app.routers.w096_marketplace_e2e import router as w096_router
from app.routers.w097_breaking_change import router as w097_router
from app.routers.w098_execution_lineage import router as w098_router
from app.routers.w099_template_proof import router as w099_router
from app.routers.w100_demo_marketplace import router as w100_router
from app.routers.w101_soc2_evidence import router as w101_router
from app.routers.w102_iso_mapping import router as w102_router
from app.routers.w103_ediscovery import router as w103_router
from app.routers.w104_gdpr_redaction import router as w104_router
from app.routers.w105_key_management import router as w105_router
from app.routers.w106_compliance_signing import router as w106_router
from app.routers.w107_compliance_e2e import router as w107_router
from app.routers.w108_compliance_chaos import router as w108_router
from app.routers.w109_compliance_regression import router as w109_router
from app.routers.w110_compliance_tour import router as w110_router
from app.routers.w111_data_lake_export import router as w111_router
from app.routers.w112_lineage_manifest import router as w112_router
from app.routers.w113_query_language import router as w113_router
from app.routers.w114_deterministic_paging import router as w114_router
from app.routers.w115_query_export_e2e import router as w115_router
from app.routers.w116_dq_export_gate import router as w116_router
from app.routers.w117_data_perf_25x import router as w117_router
from app.routers.w118_schema_versioning import router as w118_router
from app.routers.w119_data_proof import router as w119_router
from app.routers.w120_release_data_bundle import router as w120_router
from app.routers.w121_abac_engine import router as w121_router
from app.routers.w122_sso_scim import router as w122_router
from app.routers.w123_admin_console import router as w123_router
from app.routers.w124_rbac_abac_e2e import router as w124_router
from app.routers.w125_policy_regression import router as w125_router
from app.routers.w126_legal_holds_abac import router as w126_router
from app.routers.w127_export_perm_gate import router as w127_router
from app.routers.w128_access_audit import router as w128_router
from app.routers.w129_policy_proof import router as w129_router
from app.routers.w130_policy_chaos import router as w130_router
from app.routers.w131_chaos_matrix import router as w131_router
from app.routers.w132_mutation_budget import router as w132_router
from app.routers.w133_proof_of_proof import router as w133_router
from app.routers.w134_judge_loop_20x import router as w134_router
from app.routers.w135_recon_export_budget import router as w135_router
from app.routers.w136_stability_e2e import router as w136_router
from app.routers.w137_verifier_guard import router as w137_router
from app.routers.w138_trace_explorer import router as w138_router
from app.routers.w139_incident_sim import router as w139_router
from app.routers.w140_reliability_proof import router as w140_router
from app.routers.w141_fixture_100x import router as w141_router
from app.routers.w142_db_partitioning import router as w142_router
from app.routers.w143_caching_proof import router as w143_router
from app.routers.w144_large_fixture_e2e import router as w144_router
from app.routers.w145_perf_budgets_enforced import router as w145_router
from app.routers.w146_export_budget import router as w146_router
from app.routers.w147_ui_pagination import router as w147_router
from app.routers.w148_batch_workflow_perf import router as w148_router
from app.routers.w149_perf_proof import router as w149_router
from app.routers.w150_release_perf_bundle import router as w150_router
from app.routers.w151_release_v3 import router as w151_router
from app.routers.w152_hash_equality_gate import router as w152_router
from app.routers.w153_proof_verifier import router as w153_router
from app.routers.w154_judge_demo_v3 import router as w154_router
from app.routers.w155_lineage_strict import router as w155_router
from app.routers.w156_release_ui_e2e import router as w156_router
from app.routers.w157_docs_verify import router as w157_router
from app.routers.w158_no_drift_guard import router as w158_router
from app.routers.w159_final_proof_pack import router as w159_router
from app.routers.w160_release_finale import router as w160_router

app.include_router(w061_router)
app.include_router(w062_router)
app.include_router(w063_router)
app.include_router(w064_router)
app.include_router(w065_router)
app.include_router(w066_router)
app.include_router(w067_router)
app.include_router(w068_router)
app.include_router(w069_router)
app.include_router(w070_router)
app.include_router(w071_router)
app.include_router(w072_router)
app.include_router(w073_router)
app.include_router(w074_router)
app.include_router(w075_router)
app.include_router(w076_router)
app.include_router(w077_router)
app.include_router(w078_router)
app.include_router(w079_router)
app.include_router(w080_router)
app.include_router(w081_router)
app.include_router(w082_router)
app.include_router(w083_router)
app.include_router(w084_router)
app.include_router(w085_router)
app.include_router(w086_router)
app.include_router(w087_router)
app.include_router(w088_router)
app.include_router(w089_router)
app.include_router(w090_router)
app.include_router(w091_router)
app.include_router(w092_router)
app.include_router(w093_router)
app.include_router(w094_router)
app.include_router(w095_router)
app.include_router(w096_router)
app.include_router(w097_router)
app.include_router(w098_router)
app.include_router(w099_router)
app.include_router(w100_router)
app.include_router(w101_router)
app.include_router(w102_router)
app.include_router(w103_router)
app.include_router(w104_router)
app.include_router(w105_router)
app.include_router(w106_router)
app.include_router(w107_router)
app.include_router(w108_router)
app.include_router(w109_router)
app.include_router(w110_router)
app.include_router(w111_router)
app.include_router(w112_router)
app.include_router(w113_router)
app.include_router(w114_router)
app.include_router(w115_router)
app.include_router(w116_router)
app.include_router(w117_router)
app.include_router(w118_router)
app.include_router(w119_router)
app.include_router(w120_router)
app.include_router(w121_router)
app.include_router(w122_router)
app.include_router(w123_router)
app.include_router(w124_router)
app.include_router(w125_router)
app.include_router(w126_router)
app.include_router(w127_router)
app.include_router(w128_router)
app.include_router(w129_router)
app.include_router(w130_router)
app.include_router(w131_router)
app.include_router(w132_router)
app.include_router(w133_router)
app.include_router(w134_router)
app.include_router(w135_router)
app.include_router(w136_router)
app.include_router(w137_router)
app.include_router(w138_router)
app.include_router(w139_router)
app.include_router(w140_router)
app.include_router(w141_router)
app.include_router(w142_router)
app.include_router(w143_router)
app.include_router(w144_router)
app.include_router(w145_router)
app.include_router(w146_router)
app.include_router(w147_router)
app.include_router(w148_router)
app.include_router(w149_router)
app.include_router(w150_router)
app.include_router(w151_router)
app.include_router(w152_router)
app.include_router(w153_router)
app.include_router(w154_router)
app.include_router(w155_router)
app.include_router(w156_router)
app.include_router(w157_router)
app.include_router(w158_router)
app.include_router(w159_router)
app.include_router(w160_router)

from app.routers.w161_demo_contract import router as w161_router
from app.routers.w162_e2e_reset_v2 import router as w162_router
from app.routers.w163_tool_registry import router as w163_router
from app.routers.w164_agent_runtime import router as w164_router
from app.routers.w165_session_sim import router as w165_router
from app.routers.w166_agent_console import router as w166_router
from app.routers.w167_close_orchestrator import router as w167_router
from app.routers.w168_hackpack_gen import router as w168_router
from app.routers.w169_connector_mocks import router as w169_router
from app.routers.w170_connector_realmode import router as w170_router
from app.routers.w171_ml_dataset import router as w171_router
from app.routers.w172_ml_baseline import router as w172_router
from app.routers.w173_ml_inference import router as w173_router
from app.routers.w174_model_governance import router as w174_router
from app.routers.w175_evidence_search import router as w175_router
from app.routers.w176_reliability_harness import router as w176_router
from app.routers.w177_gemini_adapter import router as w177_router
from app.routers.w178_airia_adapter import router as w178_router
from app.routers.w179_gradient_adapter import router as w179_router
from app.routers.w180_submission_harden import router as w180_router

app.include_router(w161_router)
app.include_router(w162_router)
app.include_router(w163_router)
app.include_router(w164_router)
app.include_router(w165_router)
app.include_router(w166_router)
app.include_router(w167_router)
app.include_router(w168_router)
app.include_router(w169_router)
app.include_router(w170_router)
app.include_router(w171_router)
app.include_router(w172_router)
app.include_router(w173_router)
app.include_router(w174_router)
app.include_router(w175_router)
app.include_router(w176_router)
app.include_router(w177_router)
app.include_router(w178_router)
app.include_router(w179_router)
app.include_router(w180_router)

from app.routers.w181_gemini_live_provider import router as w181_router
from app.routers.w182_cloudrun_deploy import router as w182_router
from app.routers.w183_session_resume import router as w183_router
from app.routers.w184_airia_finalizer import router as w184_router
from app.routers.w185_gradient_training import router as w185_router
from app.routers.w186_gradient_inference import router as w186_router
from app.routers.w187_connector_runbooks import router as w187_router
from app.routers.w188_audit_seal import router as w188_router
from app.routers.w189_decision_dossier import router as w189_router
from app.routers.w190_evidence_highlighter import router as w190_router
from app.routers.w191_explanation_graph import router as w191_router
from app.routers.w192_policy_engine import router as w192_router
from app.routers.w193_claim_enforcement import router as w193_router
from app.routers.w194_audit_narrative import router as w194_router
from app.routers.w195_cloudrun_deploy_v2 import router as w195_router
from app.routers.w196_do_deploy import router as w196_router
from app.routers.w197_release_bundle import router as w197_router
from app.routers.w198_chaos_hooks import router as w198_router
from app.routers.w199_hackpack_v2 import router as w199_router
from app.routers.w200_submit_all import router as w200_router

app.include_router(w181_router)
app.include_router(w182_router)
app.include_router(w183_router)
app.include_router(w184_router)
app.include_router(w185_router)
app.include_router(w186_router)
app.include_router(w187_router)
app.include_router(w188_router)
app.include_router(w189_router)
app.include_router(w190_router)
app.include_router(w191_router)
app.include_router(w192_router)
app.include_router(w193_router)
app.include_router(w194_router)
app.include_router(w195_router)
app.include_router(w196_router)
app.include_router(w197_router)
app.include_router(w198_router)
app.include_router(w199_router)
app.include_router(w200_router)

from app.routers.w201_parity_harness import router as w201_router
from app.routers.w202_live_reconnect import router as w202_router
from app.routers.w203_exactly_once import router as w203_router
from app.routers.w204_adversarial_corpus import router as w204_router
from app.routers.w205_smoke_recorder import router as w205_router
from app.routers.w206_transcript_export import router as w206_router
from app.routers.w207_multi_tenant import router as w207_router
from app.routers.w208_fail_closed import router as w208_router
from app.routers.w209_run_artifact_store import router as w209_router
from app.routers.w210_replay_engine import router as w210_router
from app.routers.w211_replay_viewer import router as w211_router
from app.routers.w212_binder_regen import router as w212_router
from app.routers.w213_regression_harness import router as w213_router
from app.routers.w214_court_pack import router as w214_router
from app.routers.w215_model_impact import router as w215_router
from app.routers.w216_drift_budgets import router as w216_router
from app.routers.w217_gradient_provenance import router as w217_router
from app.routers.w218_arch_diagram import router as w218_router
from app.routers.w219_checklist_verifier import router as w219_router
from app.routers.w220_submit_all_v3 import router as w220_router

app.include_router(w201_router)
app.include_router(w202_router)
app.include_router(w203_router)
app.include_router(w204_router)
app.include_router(w205_router)
app.include_router(w206_router)
app.include_router(w207_router)
app.include_router(w208_router)
app.include_router(w209_router)
app.include_router(w210_router)
app.include_router(w211_router)
app.include_router(w212_router)
app.include_router(w213_router)
app.include_router(w214_router)
app.include_router(w215_router)
app.include_router(w216_router)
app.include_router(w217_router)
app.include_router(w218_router)
app.include_router(w219_router)
app.include_router(w220_router)

from app.routers.w221_close_calendar import router as w221_router
from app.routers.w222_task_dag import router as w222_router
from app.routers.w223_dependency_resolver import router as w223_router
from app.routers.w224_sla_monitor import router as w224_router
from app.routers.w225_blocker_tracker import router as w225_router
from app.routers.w226_handoff_protocol import router as w226_router
from app.routers.w227_progress_aggregator import router as w227_router
from app.routers.w228_close_checkpoint import router as w228_router
from app.routers.w229_rc_state_machine import router as w229_router
from app.routers.w230_lane_status import router as w230_router
from app.routers.w231_critical_path import router as w231_router
from app.routers.w232_live_scoreboard import router as w232_router
from app.routers.w233_incident_log import router as w233_router
from app.routers.w234_control_export import router as w234_router
from app.routers.w235_rc_rules import router as w235_router
from app.routers.w236_rc_notifications import router as w236_router
from app.routers.w237_rc_playbook import router as w237_router
from app.routers.w238_rc_dry_run import router as w238_router
from app.routers.w239_rc_approval import router as w239_router
from app.routers.w240_rc_proof_pack import router as w240_router

app.include_router(w221_router)
app.include_router(w222_router)
app.include_router(w223_router)
app.include_router(w224_router)
app.include_router(w225_router)
app.include_router(w226_router)
app.include_router(w227_router)
app.include_router(w228_router)
app.include_router(w229_router)
app.include_router(w230_router)
app.include_router(w231_router)
app.include_router(w232_router)
app.include_router(w233_router)
app.include_router(w234_router)
app.include_router(w235_router)
app.include_router(w236_router)
app.include_router(w237_router)
app.include_router(w238_router)
app.include_router(w239_router)
app.include_router(w240_router)

from app.routers.w241_next_actions_engine import router as w241_router
from app.routers.w242_plan_preview import router as w242_router
from app.routers.w243_verifier_gate_ui import router as w243_router
from app.routers.w244_execute_from_plan import router as w244_router
from app.routers.w245_rc_why_dossier import router as w245_router
from app.routers.w246_fail_closed_escalation import router as w246_router
from app.routers.w247_pit_crew_routing import router as w247_router
from app.routers.w248_channel_action_int import router as w248_router
from app.routers.w249_replay_hook import router as w249_router
from app.routers.w250_agent_rc_proof import router as w250_router
from app.routers.w251_policy_events import router as w251_router
from app.routers.w252_security_timeline import router as w252_router
from app.routers.w253_tool_scope_matrix import router as w253_router
from app.routers.w254_exfil_detector_v2 import router as w254_router
from app.routers.w255_safe_fix_path import router as w255_router
from app.routers.w256_audit_integrity_badge import router as w256_router
from app.routers.w257_tamper_simulation import router as w257_router
from app.routers.w258_security_posture_pack import router as w258_router
from app.routers.w259_adversarial_corpus_v2 import router as w259_router
from app.routers.w260_security_proof import router as w260_router

app.include_router(w241_router)
app.include_router(w242_router)
app.include_router(w243_router)
app.include_router(w244_router)
app.include_router(w245_router)
app.include_router(w246_router)
app.include_router(w247_router)
app.include_router(w248_router)
app.include_router(w249_router)
app.include_router(w250_router)
app.include_router(w251_router)
app.include_router(w252_router)
app.include_router(w253_router)
app.include_router(w254_router)
app.include_router(w255_router)
app.include_router(w256_router)
app.include_router(w257_router)
app.include_router(w258_router)
app.include_router(w259_router)
app.include_router(w260_router)

from app.routers.w261_replay_viewer_v3 import router as w261_router
from app.routers.w262_court_pack_v4 import router as w262_router
from app.routers.w263_telemetry_pack_v3 import router as w263_router
from app.routers.w264_reproduce_close import router as w264_router
from app.routers.w265_replay_regression import router as w265_router
from app.routers.w266_narrative_export_v2 import router as w266_router
from app.routers.w267_audit_qa_pack import router as w267_router
from app.routers.w268_replay_performance import router as w268_router
from app.routers.w269_rc_gate_extension import router as w269_router
from app.routers.w270_replay_court_proof import router as w270_router
from app.routers.w271_email_inbox_v2 import router as w271_router
from app.routers.w272_chat_workspace_v2 import router as w272_router
from app.routers.w273_browser_ext_v2 import router as w273_router
from app.routers.w274_notification_hub_v4 import router as w274_router
from app.routers.w275_cross_channel_audit import router as w275_router
from app.routers.w276_channel_reliability import router as w276_router
from app.routers.w277_rc_channel_actions import router as w277_router
from app.routers.w278_collab_v3 import router as w278_router
from app.routers.w279_ops_pack_export import router as w279_router
from app.routers.w280_everywhere_proof import router as w280_router

app.include_router(w261_router)
app.include_router(w262_router)
app.include_router(w263_router)
app.include_router(w264_router)
app.include_router(w265_router)
app.include_router(w266_router)
app.include_router(w267_router)
app.include_router(w268_router)
app.include_router(w269_router)
app.include_router(w270_router)
app.include_router(w271_router)
app.include_router(w272_router)
app.include_router(w273_router)
app.include_router(w274_router)
app.include_router(w275_router)
app.include_router(w276_router)
app.include_router(w277_router)
app.include_router(w278_router)
app.include_router(w279_router)
app.include_router(w280_router)

from app.routers.w281_payment_scheduling_v2 import router as w281_router
from app.routers.w282_tie_out_engine_v2 import router as w282_router
from app.routers.w283_fraud_red_flag_v2 import router as w283_router
from app.routers.w284_controls_coverage_v2 import router as w284_router
from app.routers.w285_data_quality_gate_v2 import router as w285_router
from app.routers.w286_multi_entity_v3 import router as w286_router
from app.routers.w287_fpa_insight_panel import router as w287_router
from app.routers.w288_ml_impact_v4 import router as w288_router
from app.routers.w289_perf_budgets_v5 import router as w289_router
from app.routers.w290_finance_proof import router as w290_router
from app.routers.w291_rc_gate_v3 import router as w291_router
from app.routers.w292_route_coverage_gate import router as w292_router
from app.routers.w293_determinism_super_gate import router as w293_router
from app.routers.w294_proof_of_proof import router as w294_router
from app.routers.w295_incident_simulator_v2 import router as w295_router
from app.routers.w296_self_healing_playbook import router as w296_router
from app.routers.w297_doc_truth_gate import router as w297_router
from app.routers.w298_security_regression import router as w298_router
from app.routers.w299_perf_regression import router as w299_router
from app.routers.w300_final_rc_proof import router as w300_router

app.include_router(w281_router)
app.include_router(w282_router)
app.include_router(w283_router)
app.include_router(w284_router)
app.include_router(w285_router)
app.include_router(w286_router)
app.include_router(w287_router)
app.include_router(w288_router)
app.include_router(w289_router)
app.include_router(w290_router)
app.include_router(w291_router)
app.include_router(w292_router)
app.include_router(w293_router)
app.include_router(w294_router)
app.include_router(w295_router)
app.include_router(w296_router)
app.include_router(w297_router)
app.include_router(w298_router)
app.include_router(w299_router)
app.include_router(w300_router)

from app.routers.w301_blueprint_builder_v1 import router as w301_router
from app.routers.w302_blueprint_builder_v2 import router as w302_router
from app.routers.w303_blueprint_versioning import router as w303_router
from app.routers.w304_generate_from_intent import router as w304_router
from app.routers.w305_blueprint_to_template import router as w305_router
from app.routers.w306_template_validator_v3 import router as w306_router
from app.routers.w307_builder_e2e_suite import router as w307_router
from app.routers.w308_builder_proof import router as w308_router
from app.routers.w309_jira_adapter_v1 import router as w309_router
from app.routers.w310_jira_cards_rc import router as w310_router
from app.routers.w311_confluence_adapter_v1 import router as w311_router
from app.routers.w312_confluence_templates import router as w312_router
from app.routers.w313_atlassian_routing import router as w313_router
from app.routers.w314_adapter_failure_sim import router as w314_router
from app.routers.w315_atlassian_e2e_suite import router as w315_router
from app.routers.w316_atlassian_proof import router as w316_router
from app.routers.w317_airia_listing_bundle import router as w317_router
from app.routers.w318_airia_bundle_validator_v3 import router as w318_router
from app.routers.w319_airia_story_gen import router as w319_router
from app.routers.w320_race_theme_pack_v2 import router as w320_router

app.include_router(w301_router)
app.include_router(w302_router)
app.include_router(w303_router)
app.include_router(w304_router)
app.include_router(w305_router)
app.include_router(w306_router)
app.include_router(w307_router)
app.include_router(w308_router)
app.include_router(w309_router)
app.include_router(w310_router)
app.include_router(w311_router)
app.include_router(w312_router)
app.include_router(w313_router)
app.include_router(w314_router)
app.include_router(w315_router)
app.include_router(w316_router)
app.include_router(w317_router)
app.include_router(w318_router)
app.include_router(w319_router)
app.include_router(w320_router)

from app.routers.w321_bundle_integrity_proof import router as w321_router
from app.routers.w322_readiness_e2e_suite import router as w322_router
from app.routers.w323_readiness_dashboard import router as w323_router
from app.routers.w324_readiness_proof import router as w324_router
from app.routers.w325_data_classification_tiers import router as w325_router
from app.routers.w326_tool_scope_diffing import router as w326_router
from app.routers.w327_redaction_events_v1 import router as w327_router
from app.routers.w328_security_scoreboard_v1 import router as w328_router
from app.routers.w329_policy_regression_budgets import router as w329_router
from app.routers.w330_adversarial_corpus_v3 import router as w330_router
from app.routers.w331_security_e2e_suite import router as w331_router
from app.routers.w332_security_gov_proof import router as w332_router
from app.routers.w333_lap_time_telemetry import router as w333_router
from app.routers.w334_productivity_roi import router as w334_router
from app.routers.w335_pit_stop_optimizer import router as w335_router
from app.routers.w336_one_cockpit import router as w336_router
from app.routers.w337_unified_why_verify_v4 import router as w337_router
from app.routers.w338_golden_scenario_gate import router as w338_router
from app.routers.w339_final_rc_gate_v4 import router as w339_router
from app.routers.w340_race_wow_proof import router as w340_router
from app.routers.golden_scenario import router as golden_scenario_router
from app.routers.airia_bundle import router as airia_bundle_router
from app.routers.race_weekend import router as race_weekend_router
from app.routers.mcp_server import router as mcp_router

app.include_router(w321_router)
app.include_router(w322_router)
app.include_router(w323_router)
app.include_router(w324_router)
app.include_router(w325_router)
app.include_router(w326_router)
app.include_router(w327_router)
app.include_router(w328_router)
app.include_router(w329_router)
app.include_router(w330_router)
app.include_router(w331_router)
app.include_router(w332_router)
app.include_router(w333_router)
app.include_router(w334_router)
app.include_router(w335_router)
app.include_router(w336_router)
app.include_router(w337_router)
app.include_router(w338_router)
app.include_router(w339_router)
app.include_router(w340_router)
app.include_router(golden_scenario_router)
app.include_router(airia_bundle_router)
app.include_router(race_weekend_router)
app.include_router(mcp_router)
