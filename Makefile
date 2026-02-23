# LedgerLive — Finance Ops Close Agent
# ──────────────────────────────────────────────

PYTHON  := apps/api/.venv/Scripts/python.exe
PIP     := apps/api/.venv/Scripts/pip.exe
UVICORN := apps/api/.venv/Scripts/uvicorn.exe
NPM     := npm
NPX     := npx

.PHONY: dev demo test e2e proof release proof-index gates

# ── Dev ──────────────────────────────────────
dev:
	cd apps/api && $(UVICORN) app.main:app --host 127.0.0.1 --port 8090 --reload &
	cd apps/web && $(NPM) run dev

demo:
	@echo "LedgerLive DEMO mode"
	APP_MODE=LOCAL LLM_PROVIDER=DEMO cd apps/api && $(UVICORN) app.main:app --host 127.0.0.1 --port 8090

# ── Test ─────────────────────────────────────
test:
	cd apps/api && $(PYTHON) -m pytest tests/ -v --tb=short

e2e-mcp:
	cd apps/web && $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed

e2e-mcp-twice:
	cd apps/web && $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed
	cd apps/web && $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed

# ── Gates ────────────────────────────────────
gates:
	$(PYTHON) tools/gates/no_apex_references.py
	$(PYTHON) tools/gates/no_network_in_tests.py

# ── Proof ────────────────────────────────────
proof:
	$(PYTHON) tools/proof/generate_proof_pack.py

proof-index:
	@echo "Proof packs:" && dir /b artifacts\\proof 2>nul || echo "(none)"

# ── Release ──────────────────────────────────
release:
	@echo "Run: git tag v$$(cat VERSION) && git push origin v$$(cat VERSION)"
