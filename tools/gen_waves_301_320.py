#!/usr/bin/env python3
"""Generate LedgerLive Waves 301-320: Phases 32-34 (partial).

Phase 32 (301-308): No-Code Blueprint Builder
Phase 33 (309-316): Atlassian Workflow Integration
Phase 34 partial (317-320): Airia Community Readiness (first 4)

Run: python tools/gen_waves_301_320.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SVC_DIR = ROOT / "apps" / "api" / "app" / "services"
RTR_DIR = ROOT / "apps" / "api" / "app" / "routers"
TST_DIR = ROOT / "apps" / "api" / "tests"
MAIN_PY = ROOT / "apps" / "api" / "app" / "main.py"

WAVES = [
    # ════════════════════════════════════════════════════════════════
    # PHASE 32: NO-CODE BLUEPRINT BUILDER (W301-W308)
    # ════════════════════════════════════════════════════════════════
    (301, "blueprint_builder_v1", "Blueprint Builder v1",
     "Visual step list editor with approvals/policies per step and deterministic export.",
     [("blueprint_id", "str"), ("name", "str"), ("steps", "list"),
      ("approval_policies", "list"), ("step_count", "int"),
      ("has_approvals", "bool"), ("export_format", "str"),
      ("export_checksum", "str"), ("version", "int"),
      ("created_by", "str"), ("deterministic", "bool"),
      ("status", "str"), ("created_at", "str")],
     [("list_blueprints", "GET", "/api/blueprint-builder", "List blueprints"),
      ("create_blueprint", "POST", "/api/blueprint-builder", "Create blueprint"),
      ("get_blueprint", "GET", "/api/blueprint-builder/{blueprint_id}", "Get blueprint details"),
      ("add_step", "POST", "/api/blueprint-builder/{blueprint_id}/add-step", "Add step to blueprint"),
      ("set_policy", "POST", "/api/blueprint-builder/{blueprint_id}/policy", "Set approval policy"),
      ("export_blueprint", "POST", "/api/blueprint-builder/{blueprint_id}/export", "Export blueprint deterministically"),
      ("blueprint_report", "GET", "/api/blueprint-builder/report", "Get blueprint builder report")]),

    (302, "blueprint_builder_v2", "Blueprint Builder v2",
     "Step dependency graph editing with validation and critical path preview.",
     [("graph_id", "str"), ("blueprint_ref", "str"), ("nodes", "list"),
      ("edges", "list"), ("critical_path", "list"),
      ("is_valid", "bool"), ("cycle_detected", "bool"),
      ("depth", "int"), ("parallelizable_steps", "int"),
      ("validation_errors", "list"), ("deterministic", "bool"),
      ("status", "str"), ("validated_at", "str")],
     [("list_graphs", "GET", "/api/blueprint-graph", "List dependency graphs"),
      ("create_graph", "POST", "/api/blueprint-graph", "Create dependency graph"),
      ("get_graph", "GET", "/api/blueprint-graph/{graph_id}", "Get graph details"),
      ("validate_graph", "POST", "/api/blueprint-graph/{graph_id}/validate", "Validate dependency graph"),
      ("critical_path", "POST", "/api/blueprint-graph/{graph_id}/critical-path", "Preview critical path"),
      ("graph_report", "GET", "/api/blueprint-graph/report", "Get graph report")]),

    (303, "blueprint_versioning", "Blueprint Versioning v1",
     "Immutable versions with diff viewer, rollback, and audit of blueprint changes.",
     [("version_id", "str"), ("blueprint_ref", "str"), ("version_num", "int"),
      ("snapshot", "dict"), ("diff_from_prev", "dict"),
      ("is_immutable", "bool"), ("rolled_back_from", "str"),
      ("change_audit", "list"), ("checksum", "str"),
      ("author", "str"), ("deterministic", "bool"),
      ("status", "str"), ("versioned_at", "str")],
     [("list_versions", "GET", "/api/blueprint-versioning", "List blueprint versions"),
      ("create_version", "POST", "/api/blueprint-versioning", "Create immutable version"),
      ("get_version", "GET", "/api/blueprint-versioning/{version_id}", "Get version details"),
      ("diff_versions", "POST", "/api/blueprint-versioning/{version_id}/diff", "Diff with previous version"),
      ("rollback_version", "POST", "/api/blueprint-versioning/{version_id}/rollback", "Rollback to version"),
      ("version_report", "GET", "/api/blueprint-versioning/report", "Get versioning report")]),

    (304, "generate_from_intent", "Generate from Intent v1",
     "Deterministic rules engine generates a blueprint from a short intent description (no LLM required).",
     [("intent_id", "str"), ("intent_text", "str"), ("matched_rules", "list"),
      ("generated_steps", "list"), ("confidence_score", "float"),
      ("blueprint_ref", "str"), ("rule_engine_version", "str"),
      ("ambiguity_flags", "list"), ("fallback_used", "bool"),
      ("deterministic", "bool"),
      ("status", "str"), ("generated_at", "str")],
     [("list_intents", "GET", "/api/generate-from-intent", "List generated intents"),
      ("generate_blueprint", "POST", "/api/generate-from-intent", "Generate blueprint from intent"),
      ("get_intent", "GET", "/api/generate-from-intent/{intent_id}", "Get intent details"),
      ("refine_intent", "POST", "/api/generate-from-intent/{intent_id}/refine", "Refine generated blueprint"),
      ("preview_intent", "POST", "/api/generate-from-intent/{intent_id}/preview", "Preview generated blueprint"),
      ("intent_report", "GET", "/api/generate-from-intent/report", "Get intent generation report")]),

    (305, "blueprint_to_template", "Blueprint-to-Template Compiler v1",
     "Compiles blueprint into Airia template artifacts (offline deterministic).",
     [("compile_id", "str"), ("blueprint_ref", "str"), ("template_output", "dict"),
      ("artifact_manifest", "list"), ("compilation_log", "list"),
      ("warnings", "list"), ("errors", "list"),
      ("output_checksum", "str"), ("compiler_version", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("compiled_at", "str")],
     [("list_compiles", "GET", "/api/blueprint-to-template", "List compilations"),
      ("compile_blueprint", "POST", "/api/blueprint-to-template", "Compile blueprint to template"),
      ("get_compile", "GET", "/api/blueprint-to-template/{compile_id}", "Get compilation details"),
      ("validate_output", "POST", "/api/blueprint-to-template/{compile_id}/validate", "Validate compilation output"),
      ("recompile", "POST", "/api/blueprint-to-template/{compile_id}/recompile", "Recompile blueprint"),
      ("compile_report", "GET", "/api/blueprint-to-template/report", "Get compilation report")]),

    (306, "template_validator_v3", "Template Validator v3",
     "Strict completeness checks with deterministic checksums for compiled templates.",
     [("validation_id", "str"), ("template_ref", "str"), ("check_results", "list"),
      ("completeness_score", "float"), ("is_complete", "bool"),
      ("missing_fields", "list"), ("checksum", "str"),
      ("checksum_match", "bool"), ("validator_version", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("validated_at", "str")],
     [("list_validations", "GET", "/api/template-validator-v3", "List template validations"),
      ("validate_template", "POST", "/api/template-validator-v3", "Validate template"),
      ("get_validation", "GET", "/api/template-validator-v3/{validation_id}", "Get validation details"),
      ("revalidate", "POST", "/api/template-validator-v3/{validation_id}/revalidate", "Revalidate template"),
      ("checksum_verify", "POST", "/api/template-validator-v3/{validation_id}/checksum", "Verify template checksum"),
      ("validation_report", "GET", "/api/template-validator-v3/report", "Get validation report")]),

    (307, "builder_e2e_suite", "Builder E2E Suite v1",
     "MCP E2E: create blueprint, preview, compile, validate, run canonical orchestration.",
     [("suite_id", "str"), ("test_name", "str"), ("steps_executed", "list"),
      ("blueprint_created", "bool"), ("preview_passed", "bool"),
      ("compile_passed", "bool"), ("validate_passed", "bool"),
      ("orchestration_passed", "bool"), ("all_passed", "bool"),
      ("execution_log", "list"), ("deterministic", "bool"),
      ("status", "str"), ("executed_at", "str")],
     [("list_suites", "GET", "/api/builder-e2e-suite", "List E2E suites"),
      ("run_suite", "POST", "/api/builder-e2e-suite", "Run builder E2E suite"),
      ("get_suite", "GET", "/api/builder-e2e-suite/{suite_id}", "Get suite details"),
      ("rerun_suite", "POST", "/api/builder-e2e-suite/{suite_id}/rerun", "Rerun E2E suite"),
      ("export_results", "POST", "/api/builder-e2e-suite/{suite_id}/export", "Export suite results"),
      ("suite_report", "GET", "/api/builder-e2e-suite/report", "Get E2E suite report")]),

    (308, "builder_proof", "Builder Proof Wave v1",
     "Full builder flow proof with determinism twice-run verification.",
     [("proof_id", "str"), ("builder_flow_ref", "str"), ("determinism_hash_1", "str"),
      ("determinism_hash_2", "str"), ("hashes_match", "bool"),
      ("tour_updated", "bool"), ("all_gates_pass", "bool"),
      ("evidence_refs", "list"), ("content_hash", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/builder-proof", "List builder proofs"),
      ("generate_proof", "POST", "/api/builder-proof", "Generate builder proof"),
      ("get_proof", "GET", "/api/builder-proof/{proof_id}", "Get proof details"),
      ("verify_determinism", "POST", "/api/builder-proof/{proof_id}/verify", "Verify determinism twice-run"),
      ("seal_proof", "POST", "/api/builder-proof/{proof_id}/seal", "Seal builder proof"),
      ("proof_report", "GET", "/api/builder-proof/report", "Get builder proof report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 33: ATLASSIAN WORKFLOW INTEGRATION (W309-W316)
    # ════════════════════════════════════════════════════════════════
    (309, "jira_adapter_v1", "Jira Adapter v1",
     "Mock server creating issues for blockers/incidents/overdue approvals. Idempotent and deterministic.",
     [("issue_id", "str"), ("issue_type", "str"), ("summary", "str"),
      ("description", "str"), ("priority", "str"), ("blocker_ref", "str"),
      ("incident_ref", "str"), ("approval_ref", "str"),
      ("idempotency_key", "str"), ("deep_link", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("created_at", "str")],
     [("list_issues", "GET", "/api/jira-adapter", "List Jira issues"),
      ("create_issue", "POST", "/api/jira-adapter", "Create Jira issue"),
      ("get_issue", "GET", "/api/jira-adapter/{issue_id}", "Get issue details"),
      ("update_issue", "POST", "/api/jira-adapter/{issue_id}/update", "Update issue"),
      ("transition_issue", "POST", "/api/jira-adapter/{issue_id}/transition", "Transition issue status"),
      ("resolve_issue", "POST", "/api/jira-adapter/{issue_id}/resolve", "Resolve issue"),
      ("issue_report", "GET", "/api/jira-adapter/report", "Get Jira adapter report")]),

    (310, "jira_cards_rc", "Jira Cards in Race Control v1",
     "Link Jira issues to Race Control blockers with deep links and deterministic ordering.",
     [("card_id", "str"), ("jira_issue_ref", "str"), ("blocker_ref", "str"),
      ("deep_link_url", "str"), ("display_order", "int"),
      ("lane_ref", "str"), ("severity", "str"),
      ("linked_at", "str"), ("is_resolved", "bool"),
      ("deterministic", "bool"),
      ("status", "str"), ("updated_at", "str")],
     [("list_cards", "GET", "/api/jira-cards-rc", "List Jira cards in RC"),
      ("create_card", "POST", "/api/jira-cards-rc", "Create Jira card link"),
      ("get_card", "GET", "/api/jira-cards-rc/{card_id}", "Get card details"),
      ("reorder_cards", "POST", "/api/jira-cards-rc/{card_id}/reorder", "Reorder cards"),
      ("resolve_card", "POST", "/api/jira-cards-rc/{card_id}/resolve", "Mark card resolved"),
      ("card_report", "GET", "/api/jira-cards-rc/report", "Get Jira cards RC report")]),

    (311, "confluence_adapter_v1", "Confluence Adapter v1",
     "Mock server generating Race Weekend Close Report pages from telemetry/court artifacts.",
     [("page_id", "str"), ("page_title", "str"), ("content_body", "str"),
      ("telemetry_ref", "str"), ("court_pack_ref", "str"),
      ("template_used", "str"), ("space_key", "str"),
      ("parent_page_ref", "str"), ("version_num", "int"),
      ("deterministic", "bool"),
      ("status", "str"), ("created_at", "str")],
     [("list_pages", "GET", "/api/confluence-adapter", "List Confluence pages"),
      ("create_page", "POST", "/api/confluence-adapter", "Create Confluence page"),
      ("get_page", "GET", "/api/confluence-adapter/{page_id}", "Get page details"),
      ("update_content", "POST", "/api/confluence-adapter/{page_id}/update", "Update page content"),
      ("render_preview", "POST", "/api/confluence-adapter/{page_id}/preview", "Render page preview"),
      ("page_report", "GET", "/api/confluence-adapter/report", "Get Confluence adapter report")]),

    (312, "confluence_templates", "Confluence Page Templates v1",
     "Deterministic rendering with citations to dossiers and evidence artifacts.",
     [("template_id", "str"), ("template_name", "str"), ("template_body", "str"),
      ("citation_refs", "list"), ("dossier_refs", "list"),
      ("evidence_refs", "list"), ("rendered_output", "str"),
      ("render_checksum", "str"), ("variable_slots", "list"),
      ("deterministic", "bool"),
      ("status", "str"), ("rendered_at", "str")],
     [("list_templates", "GET", "/api/confluence-templates", "List page templates"),
      ("create_template", "POST", "/api/confluence-templates", "Create page template"),
      ("get_template", "GET", "/api/confluence-templates/{template_id}", "Get template details"),
      ("render_template", "POST", "/api/confluence-templates/{template_id}/render", "Render template with data"),
      ("validate_citations", "POST", "/api/confluence-templates/{template_id}/citations", "Validate citations"),
      ("template_report", "GET", "/api/confluence-templates/report", "Get templates report")]),

    (313, "atlassian_routing", "Atlassian Routing Rules v1",
     "Which events create Jira issues or Confluence pages with frozen-time SLA escalation integration.",
     [("rule_id", "str"), ("event_type", "str"), ("target_system", "str"),
      ("target_action", "str"), ("sla_hours", "int"),
      ("escalation_enabled", "bool"), ("frozen_time_ref", "str"),
      ("conditions", "list"), ("priority_map", "dict"),
      ("last_triggered", "str"), ("deterministic", "bool"),
      ("status", "str"), ("created_at", "str")],
     [("list_rules", "GET", "/api/atlassian-routing", "List routing rules"),
      ("create_rule", "POST", "/api/atlassian-routing", "Create routing rule"),
      ("get_rule", "GET", "/api/atlassian-routing/{rule_id}", "Get rule details"),
      ("trigger_rule", "POST", "/api/atlassian-routing/{rule_id}/trigger", "Trigger routing rule"),
      ("test_rule", "POST", "/api/atlassian-routing/{rule_id}/test", "Test rule with sample event"),
      ("rule_report", "GET", "/api/atlassian-routing/report", "Get routing rules report")]),

    (314, "adapter_failure_sim", "Adapter Failure Simulation v1",
     "Adapter failures become incidents with deterministic recovery audit trails.",
     [("sim_id", "str"), ("adapter_name", "str"), ("failure_type", "str"),
      ("failure_injected", "bool"), ("incident_created", "bool"),
      ("incident_ref", "str"), ("recovery_action", "str"),
      ("recovery_successful", "bool"), ("audit_trail", "list"),
      ("deterministic", "bool"),
      ("status", "str"), ("simulated_at", "str")],
     [("list_sims", "GET", "/api/adapter-failure-sim", "List failure simulations"),
      ("create_sim", "POST", "/api/adapter-failure-sim", "Create failure simulation"),
      ("get_sim", "GET", "/api/adapter-failure-sim/{sim_id}", "Get simulation details"),
      ("inject_failure", "POST", "/api/adapter-failure-sim/{sim_id}/inject", "Inject adapter failure"),
      ("recover", "POST", "/api/adapter-failure-sim/{sim_id}/recover", "Attempt recovery"),
      ("sim_report", "GET", "/api/adapter-failure-sim/report", "Get simulation report")]),

    (315, "atlassian_e2e_suite", "Atlassian E2E Suite v1",
     "MCP E2E: overdue approval -> Jira issue created -> visible on RC; export Confluence report preview.",
     [("suite_id", "str"), ("test_name", "str"), ("steps_executed", "list"),
      ("jira_issue_created", "bool"), ("rc_visible", "bool"),
      ("confluence_exported", "bool"), ("all_passed", "bool"),
      ("execution_log", "list"), ("evidence_refs", "list"),
      ("deterministic", "bool"),
      ("status", "str"), ("executed_at", "str")],
     [("list_suites", "GET", "/api/atlassian-e2e-suite", "List E2E suites"),
      ("run_suite", "POST", "/api/atlassian-e2e-suite", "Run Atlassian E2E suite"),
      ("get_suite", "GET", "/api/atlassian-e2e-suite/{suite_id}", "Get suite details"),
      ("rerun_suite", "POST", "/api/atlassian-e2e-suite/{suite_id}/rerun", "Rerun E2E suite"),
      ("export_results", "POST", "/api/atlassian-e2e-suite/{suite_id}/export", "Export suite results"),
      ("suite_report", "GET", "/api/atlassian-e2e-suite/report", "Get Atlassian E2E report")]),

    (316, "atlassian_proof", "Atlassian Proof Wave v1",
     "Atlassian mock integration showcased end-to-end with determinism twice-run.",
     [("proof_id", "str"), ("integration_flow_ref", "str"), ("jira_tests_pass", "bool"),
      ("confluence_tests_pass", "bool"), ("routing_tests_pass", "bool"),
      ("failure_sim_pass", "bool"), ("determinism_hash_1", "str"),
      ("determinism_hash_2", "str"), ("hashes_match", "bool"),
      ("evidence_refs", "list"), ("deterministic", "bool"),
      ("status", "str"), ("verified_at", "str")],
     [("list_proofs", "GET", "/api/atlassian-proof", "List Atlassian proofs"),
      ("generate_proof", "POST", "/api/atlassian-proof", "Generate Atlassian proof"),
      ("get_proof", "GET", "/api/atlassian-proof/{proof_id}", "Get proof details"),
      ("verify_integration", "POST", "/api/atlassian-proof/{proof_id}/verify", "Verify integration"),
      ("seal_proof", "POST", "/api/atlassian-proof/{proof_id}/seal", "Seal Atlassian proof"),
      ("proof_report", "GET", "/api/atlassian-proof/report", "Get Atlassian proof report")]),

    # ════════════════════════════════════════════════════════════════
    # PHASE 34 (partial): AIRIA COMMUNITY READINESS (W317-W320)
    # ════════════════════════════════════════════════════════════════
    (317, "airia_listing_bundle", "Airia Listing Bundle v1",
     "Generate agent listing metadata (name, description, tags) and screenshots manifest.",
     [("bundle_id", "str"), ("agent_name", "str"), ("agent_description", "str"),
      ("tags", "list"), ("screenshots_manifest", "list"),
      ("icon_ref", "str"), ("category", "str"),
      ("listing_version", "int"), ("checksum", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("generated_at", "str")],
     [("list_bundles", "GET", "/api/airia-listing-bundle", "List listing bundles"),
      ("create_bundle", "POST", "/api/airia-listing-bundle", "Create listing bundle"),
      ("get_bundle", "GET", "/api/airia-listing-bundle/{bundle_id}", "Get bundle details"),
      ("update_metadata", "POST", "/api/airia-listing-bundle/{bundle_id}/metadata", "Update metadata"),
      ("generate_manifest", "POST", "/api/airia-listing-bundle/{bundle_id}/manifest", "Generate screenshots manifest"),
      ("bundle_report", "GET", "/api/airia-listing-bundle/report", "Get listing bundle report")]),

    (318, "airia_bundle_validator_v3", "Airia Bundle Validator v3",
     "Publish readiness strict check with deterministic file ordering and checksums.",
     [("validation_id", "str"), ("bundle_ref", "str"), ("checks_passed", "list"),
      ("checks_failed", "list"), ("is_ready", "bool"),
      ("file_ordering", "list"), ("ordering_checksum", "str"),
      ("missing_artifacts", "list"), ("validator_version", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("validated_at", "str")],
     [("list_validations", "GET", "/api/airia-bundle-validator-v3", "List bundle validations"),
      ("validate_bundle", "POST", "/api/airia-bundle-validator-v3", "Validate bundle for readiness"),
      ("get_validation", "GET", "/api/airia-bundle-validator-v3/{validation_id}", "Get validation details"),
      ("revalidate", "POST", "/api/airia-bundle-validator-v3/{validation_id}/revalidate", "Revalidate bundle"),
      ("fix_ordering", "POST", "/api/airia-bundle-validator-v3/{validation_id}/fix-ordering", "Fix file ordering"),
      ("validation_report", "GET", "/api/airia-bundle-validator-v3/report", "Get validation report")]),

    (319, "airia_story_gen", "Airia Story Generator v1",
     "Auto-write a short agent description from blueprint and capabilities (deterministic, no LLM).",
     [("story_id", "str"), ("blueprint_ref", "str"), ("capabilities", "list"),
      ("generated_title", "str"), ("generated_summary", "str"),
      ("generated_highlights", "list"), ("word_count", "int"),
      ("template_used", "str"), ("content_checksum", "str"),
      ("deterministic", "bool"),
      ("status", "str"), ("generated_at", "str")],
     [("list_stories", "GET", "/api/airia-story-gen", "List generated stories"),
      ("generate_story", "POST", "/api/airia-story-gen", "Generate agent story"),
      ("get_story", "GET", "/api/airia-story-gen/{story_id}", "Get story details"),
      ("regenerate_story", "POST", "/api/airia-story-gen/{story_id}/regenerate", "Regenerate story"),
      ("preview_story", "POST", "/api/airia-story-gen/{story_id}/preview", "Preview story rendering"),
      ("story_report", "GET", "/api/airia-story-gen/report", "Get story generation report")]),

    (320, "race_theme_pack_v2", "Race Theme Pack v2",
     "Ensure Race Control naming is consistent across bundles and UI.",
     [("theme_id", "str"), ("theme_name", "str"), ("naming_rules", "list"),
      ("inconsistencies_found", "list"), ("is_consistent", "bool"),
      ("bundle_refs_checked", "list"), ("ui_refs_checked", "list"),
      ("fix_suggestions", "list"), ("theme_version", "int"),
      ("deterministic", "bool"),
      ("status", "str"), ("checked_at", "str")],
     [("list_themes", "GET", "/api/race-theme-pack-v2", "List theme packs"),
      ("create_theme", "POST", "/api/race-theme-pack-v2", "Create theme pack check"),
      ("get_theme", "GET", "/api/race-theme-pack-v2/{theme_id}", "Get theme details"),
      ("check_consistency", "POST", "/api/race-theme-pack-v2/{theme_id}/check", "Check naming consistency"),
      ("apply_fixes", "POST", "/api/race-theme-pack-v2/{theme_id}/fix", "Apply naming fixes"),
      ("theme_report", "GET", "/api/race-theme-pack-v2/report", "Get theme pack report")]),
]


def _class_name(slug: str) -> str:
    return "".join(w.capitalize() for w in slug.split("_"))


def _default_value(type_str: str) -> str:
    if type_str in ("str", "str|None"):
        return '""'
    elif type_str == "int":
        return "0"
    elif type_str == "float":
        return "0.0"
    elif type_str == "bool":
        return "True"
    elif type_str == "list":
        return "[]"
    elif type_str in ("dict", "dict|None"):
        return "{}"
    return '""'


def _sample_create_data(fields: list) -> dict:
    data = {}
    for name, ftype in fields[1:]:
        if ftype in ("str", "str|None"):
            data[name] = f"test-{name}"
        elif ftype == "int":
            data[name] = 1
        elif ftype == "float":
            data[name] = 1.0
        elif ftype == "bool":
            data[name] = True
        elif ftype == "list":
            data[name] = []
        elif ftype in ("dict", "dict|None"):
            data[name] = {}
    return data


def gen_service(wave_num, slug, title, desc, fields, operations):
    id_field = fields[0][0]
    field_defs = "\n".join(f'        "{f[0]}": {_default_value(f[1])},' for f in fields)

    ops_code = []
    for op_name, method, path, op_desc in operations:
        if method == "GET" and "{" not in path:
            ops_code.append(f'''
    def {op_name}(self, **kwargs) -> list[dict]:
        """List/query items."""
        items = list(self._store.values())
        return items[:kwargs.get("limit", 100)]
''')
        elif method == "POST" and "{" not in path:
            ops_code.append(f'''
    def {op_name}(self, data: dict) -> dict:
        """Create/run: {op_desc}."""
        import uuid as _u
        item_id = str(_u.uuid4())
        item = {{**self._template(), **data, "{id_field}": item_id}}
        self._store[item_id] = item
        emit_audit_event("{op_name}", "{slug}", item_id, {{"data": data}})
        return item
''')
        elif method == "GET" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            ops_code.append(f'''
    def {op_name}(self, {param}: str) -> dict | None:
        """Get item by ID."""
        return self._store.get({param})
''')
        elif method == "PUT":
            param = re.search(r'\{(\w+)\}', path).group(1)
            ops_code.append(f'''
    def {op_name}(self, {param}: str, data: dict) -> dict | None:
        """Update: {op_desc}."""
        item = self._store.get({param})
        if not item:
            return None
        item.update(data)
        emit_audit_event("{op_name}", "{slug}", {param}, {{"data": data}})
        return item
''')
        elif method == "DELETE":
            param = re.search(r'\{(\w+)\}', path).group(1)
            ops_code.append(f'''
    def {op_name}(self, {param}: str) -> bool:
        """Delete: {op_desc}."""
        if {param} in self._store:
            del self._store[{param}]
            emit_audit_event("{op_name}", "{slug}", {param})
            return True
        return False
''')
        elif method == "POST" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            ops_code.append(f'''
    def {op_name}(self, {param}: str, data: dict | None = None) -> dict | None:
        """Action: {op_desc}."""
        item = self._store.get({param})
        if not item:
            return None
        if data:
            item.update(data)
        if "status" in item:
            item["status"] = "{op_name}d"
        emit_audit_event("{op_name}", "{slug}", {param}, {{"action": "{op_name}", "data": data or {{}}}})
        return item
''')

    return f'''"""Wave {wave_num}: {title} — {desc}

PROJECT_ID: LEDGERLIVE
"""
from app.main import emit_audit_event


class {_class_name(slug)}Service:
    """Domain service for {title}."""

    def __init__(self):
        self._store: dict[str, dict] = {{}}

    def _template(self) -> dict:
        return {{
{field_defs}
        }}

    def reset(self):
        """Clear all data (for testing)."""
        self._store.clear()

    @property
    def count(self) -> int:
        return len(self._store)
{"".join(ops_code)}

# Module-level singleton
service = {_class_name(slug)}Service()
'''


def gen_router(wave_num, slug, title, desc, fields, operations):
    svc_import = f"from app.services.w{wave_num:03d}_{slug} import service"

    sorted_ops = sorted(operations, key=lambda o: (1 if '{' in o[2] else 0, o[2]))

    routes = []
    for op_name, method, path, op_desc in sorted_ops:
        if method == "GET" and "{" not in path:
            routes.append(f'''
@router.get("{path}")
async def api_{slug}_w{wave_num}_{op_name}(limit: int = 100):
    """{op_desc}"""
    items = service.{op_name}(limit=limit)
    return {{"items": items, "total": len(items)}}
''')
        elif method == "POST" and "{" not in path:
            routes.append(f'''
@router.post("{path}", status_code=201)
async def api_{slug}_w{wave_num}_{op_name}(request: Request):
    """{op_desc}"""
    data = await request.json()
    item = service.{op_name}(data)
    return item
''')
        elif method == "GET" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.get("{path}")
async def api_{slug}_w{wave_num}_{op_name}({param}: str):
    """{op_desc}"""
    item = service.{op_name}({param})
    if not item:
        raise HTTPException(status_code=404, detail="{slug} not found")
    return item
''')
        elif method == "PUT":
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.put("{path}")
async def api_{slug}_w{wave_num}_{op_name}({param}: str, request: Request):
    """{op_desc}"""
    data = await request.json()
    item = service.{op_name}({param}, data)
    if not item:
        raise HTTPException(status_code=404, detail="{slug} not found")
    return item
''')
        elif method == "DELETE":
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.delete("{path}")
async def api_{slug}_w{wave_num}_{op_name}({param}: str):
    """{op_desc}"""
    ok = service.{op_name}({param})
    if not ok:
        raise HTTPException(status_code=404, detail="{slug} not found")
    return {{"deleted": True}}
''')
        elif method == "POST" and "{" in path:
            param = re.search(r'\{(\w+)\}', path).group(1)
            routes.append(f'''
@router.post("{path}")
async def api_{slug}_w{wave_num}_{op_name}({param}: str, request: Request):
    """{op_desc}"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.{op_name}({param}, data)
    if not item:
        raise HTTPException(status_code=404, detail="{slug} not found")
    return item
''')

    return f'''"""Wave {wave_num}: {title} Router — {desc}

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

{svc_import}

router = APIRouter(tags=["{title}"])
{"".join(routes)}'''


def gen_tests(wave_num, slug, title, desc, fields, operations):
    id_field = fields[0][0]
    svc_import = f"from app.services.w{wave_num:03d}_{slug} import service"

    create_op = list_op = get_op = update_op = delete_op = None
    action_ops = []

    for op_name, method, path, op_desc in operations:
        if method == "POST" and "{" not in path and create_op is None:
            create_op = (op_name, method, path)
        elif method == "GET" and "{" not in path and list_op is None:
            list_op = (op_name, method, path)
        elif method == "GET" and "{" in path and get_op is None:
            get_op = (op_name, method, path)
        elif method == "PUT" and update_op is None:
            update_op = (op_name, method, path)
        elif method == "DELETE" and delete_op is None:
            delete_op = (op_name, method, path)
        elif method == "POST" and "{" in path:
            action_ops.append((op_name, method, path))

    sample_data = _sample_create_data(fields)
    tests = []

    tests.append(f'''
@pytest.fixture(autouse=True)
def _reset():
    service.reset()
    yield
    service.reset()
''')

    tests.append(f'''
def test_w{wave_num:03d}_service_starts_empty():
    assert service.count == 0
''')

    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_create(client):
    r = await client.post("{cpath}", json={sample_data})
    assert r.status_code == 201
    data = r.json()
    assert "{id_field}" in data
    assert service.count == 1
''')

    if list_op and create_op:
        _, _, lpath = list_op
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_list(client):
    await client.post("{cpath}", json={sample_data})
    await client.post("{cpath}", json={sample_data})
    r = await client.get("{lpath}")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2
''')

    if get_op and create_op:
        _, _, gpath = get_op
        _, _, cpath = create_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_t = gpath.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_get_by_id(client):
    r = await client.post("{cpath}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.get(f"{gpath_t}")
    assert r2.status_code == 200
    assert r2.json()["{id_field}"] == item_id
''')

    if get_op:
        _, _, gpath = get_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_404 = gpath.replace("{" + param + "}", "nonexistent-id")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_get_not_found(client):
    r = await client.get("{gpath_404}")
    assert r.status_code == 404
''')

    if action_ops and create_op:
        _, _, cpath = create_op
        for aname, _, apath in action_ops[:3]:
            param = re.search(r'\{(\w+)\}', apath).group(1)
            apath_t = apath.replace("{" + param + "}", "{item_id}")
            tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_{aname}(client):
    r = await client.post("{cpath}", json={sample_data})
    item_id = r.json()["{id_field}"]
    r2 = await client.post(f"{apath_t}", json={{}})
    assert r2.status_code == 200
    assert r2.json()["{id_field}"] == item_id
''')

    if action_ops:
        aname, _, apath = action_ops[0]
        param = re.search(r'\{(\w+)\}', apath).group(1)
        apath_404 = apath.replace("{" + param + "}", "nonexistent-id")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_{aname}_not_found(client):
    r = await client.post("{apath_404}", json={{}})
    assert r.status_code == 404
''')

    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_audit_event_emitted(client):
    from app.main import AUDIT_LOG
    await client.post("{cpath}", json={sample_data})
    assert len(AUDIT_LOG) >= 1
    event = AUDIT_LOG[-1]
    assert event["entity_type"] == "{slug}"
    assert "trace_id" in event
''')

    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_determinism(client):
    """Same input produces consistent structure."""
    r1 = await client.post("{cpath}", json={sample_data})
    service.reset()
    from app.main import AUDIT_LOG
    AUDIT_LOG.clear()
    r2 = await client.post("{cpath}", json={sample_data})
    d1, d2 = r1.json(), r2.json()
    assert set(d1.keys()) == set(d2.keys())
    for k in d1:
        if k != "{id_field}":
            assert type(d1[k]) == type(d2[k])
''')

    if create_op:
        _, _, cpath = create_op
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_break_it_empty_body(client):
    """Empty body should still create with defaults."""
    r = await client.post("{cpath}", json={{}})
    assert r.status_code == 201
''')

    if create_op and list_op and get_op:
        _, _, cpath = create_op
        _, _, lpath = list_op
        _, _, gpath = get_op
        param = re.search(r'\{(\w+)\}', gpath).group(1)
        gpath_t = gpath.replace("{" + param + "}", "{item_id}")
        tests.append(f'''
@pytest.mark.asyncio
async def test_w{wave_num:03d}_integration_create_list_get(client):
    """Integration: create -> list -> get by ID."""
    r1 = await client.post("{cpath}", json={sample_data})
    assert r1.status_code == 201
    item_id = r1.json()["{id_field}"]
    r2 = await client.get("{lpath}")
    assert r2.status_code == 200
    assert r2.json()["total"] >= 1
    r3 = await client.get(f"{gpath_t}")
    assert r3.status_code == 200
    assert r3.json()["{id_field}"] == item_id
''')

    return f'''"""Tests for Wave {wave_num}: {title}

PROJECT_ID: LEDGERLIVE
"""
import pytest
{svc_import}

{"".join(tests)}'''


def gen_main_additions(waves):
    imports = []
    includes = []
    for wave_num, slug, *_ in waves:
        imports.append(f"from app.routers.w{wave_num:03d}_{slug} import router as w{wave_num:03d}_router")
        includes.append(f"app.include_router(w{wave_num:03d}_router)")
    return "\n".join(imports) + "\n\n" + "\n".join(includes) + "\n"


def main():
    print(f"Generating {len(WAVES)} waves (301-320)...")

    for wave_num, slug, title, desc, fields, operations in WAVES:
        svc_path = SVC_DIR / f"w{wave_num:03d}_{slug}.py"
        svc_path.write_text(gen_service(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        rtr_path = RTR_DIR / f"w{wave_num:03d}_{slug}.py"
        rtr_path.write_text(gen_router(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        tst_path = TST_DIR / f"test_w{wave_num:03d}_{slug}.py"
        tst_path.write_text(gen_tests(wave_num, slug, title, desc, fields, operations), encoding="utf-8")

        print(f"  W{wave_num:03d} {slug}: service + router + tests")

    main_content = MAIN_PY.read_text(encoding="utf-8")
    additions = gen_main_additions(WAVES)
    main_content = main_content.rstrip() + "\n\n" + additions
    MAIN_PY.write_text(main_content, encoding="utf-8")
    print(f"\n  main.py updated with {len(WAVES)} new router registrations")

    print(f"\nDone! Generated {len(WAVES)} services, routers, and test files.")


if __name__ == "__main__":
    main()
