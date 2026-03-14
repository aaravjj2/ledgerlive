# LedgerLive — Finance Ops Close Agent
# ──────────────────────────────────────────────
# Cross-platform: Linux/WSL uses python3, Windows uses .venv
UNAME_S := $(shell uname -s 2>/dev/null || echo Unknown)
ifeq ($(UNAME_S),Linux)
  PYTHON  := python3
  PIP     := pip3
  UVICORN := python3 -m uvicorn
  E2E_CMD := xvfb-run $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed
else
  PYTHON  := apps/api/.venv/Scripts/python.exe
  PIP     := apps/api/.venv/Scripts/pip.exe
  UVICORN := apps/api/.venv/Scripts/uvicorn.exe
  E2E_CMD := $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed
endif
NPM     := npm
NPX     := npx

MILESTONE ?= golden-e2e

.PHONY: dev demo test e2e proof release proof-index gates \
        e2e-mcp e2e-mcp-twice e2e-mcp-xvfb e2e\:mcp\:twice \
        airia\:bundle airia\:validate airia\:verify airia\:compat proof-airia proof-airia-score \
        airia\:loop \
        lint docker-up docker-down seed format coverage security

# ── Dev ──────────────────────────────────────
dev:
	cd apps/api && $(UVICORN) app.main:app --host 127.0.0.1 --port 8090 --reload &
	cd apps/web && $(NPM) run dev

# demo — starts API + vite preview on canonical ports (4173 + 8090)
# APP_MODE=DEMO and E2E_MODE=1 required for golden-scenario endpoints
demo:
	@echo "=== LedgerLive DEMO mode (API:8090  Web:4173) ==="
	@echo "Starting API server (APP_MODE=DEMO E2E_MODE=1)..."
	@cd apps/api && APP_MODE=DEMO LLM_PROVIDER=DEMO SECRET_KEY=demo-secret E2E_MODE=1 $(UVICORN) app.main:app --host 127.0.0.1 --port 8090 &
	@echo "Building and starting web preview..."
	@cd apps/web && $(NPX) vite build --outDir dist && $(NPX) vite preview --host 127.0.0.1 --port 4173

# ── Test ─────────────────────────────────────
test:
	cd apps/api && $(PYTHON) -m pytest tests/ -v --tb=short

e2e-mcp:
	cd apps/web && $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed

# Xvfb: Virtual Framebuffer for Linux/WSL — non-headless Playwright without stealing focus
e2e-mcp-xvfb:
	cd apps/web && xvfb-run $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed

e2e-mcp-twice:
	cd apps/web && $(E2E_CMD)
	cd apps/web && $(E2E_CMD)

# Colon-variant alias — also validates API determinism after second run
e2e\:mcp\:twice:
	cd apps/web && $(E2E_CMD)
	cd apps/web && $(E2E_CMD)
	$(PYTHON) tools/gates/e2e_determinism_gate.py --api http://127.0.0.1:8090

# ── Airia Community Bundle ────────────────────────────────────────────────────
airia\:bundle:
	$(PYTHON) tools/airia_bundle.py --action bundle

airia\:validate:
	$(PYTHON) tools/airia_bundle.py --action validate

airia\:verify:
	$(PYTHON) tools/airia_bundle.py --action verify

airia\:compat:
	$(PYTHON) tools/airia_compat.py

proof-airia:
	$(PYTHON) tools/proof/generate_proof_pack.py --milestone=airia-readiness

proof-airia-score:
	$(PYTHON) tools/gates/no_apex_references.py
	$(PYTHON) tools/gates/no_network_in_tests.py
	cd apps/web && $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed
	cd apps/web && $(NPX) playwright test --project=chromium --retries=0 --workers=1 --headed
	$(PYTHON) tools/proof/generate_proof_pack.py --milestone=airia-score-boost-v2


# ── Gates ────────────────────────────────────
gates:
	$(PYTHON) tools/gates/no_apex_references.py
	$(PYTHON) tools/gates/no_network_in_tests.py

# ── Proof ────────────────────────────────────
proof:
	$(PYTHON) tools/proof/generate_proof_pack.py --milestone=$(MILESTONE)

proof-index:
	@echo "Proof packs:" && dir /b artifacts\\proof 2>nul || echo "(none)"

# ── Release ──────────────────────────────────
release:
	@echo "Run: git tag v$$(cat VERSION) && git push origin v$$(cat VERSION)"

# ── Airia Strict Judge Loop ──────────────────
airia\:loop:
	powershell -ExecutionPolicy Bypass -File tools/airia_loop/run_strict_loop.ps1

# ── Airia CFO Judge Loop ────────────────────
airia\:cfo-loop:
	powershell -ExecutionPolicy Bypass -File tools/airia_loop/run_strict_loop.ps1 -MaxIters 5

# ── Airia Strict Loop v2 (CFO Memorable) ────
airia\:strict-loop-v2:
	powershell -ExecutionPolicy Bypass -File tools/airia_strict_loop_v2/run.ps1 -MaxIters 10
# ── Nuclear 20/20 Gate Loop ─────────────────
nuclear\:loop:
	powershell -ExecutionPolicy Bypass -File tools/nuclear_loop/run.ps1 -MaxIters 25

# ── Nuclear Judge (single run) ──────────────
nuclear\:judge:
	$(PYTHON) tools/nuclear_loop/apply.py
	$(PYTHON) evaluate_ledgerlive_strict.py

# ── Nuclear Apply (patch failing gates) ─────
nuclear\:apply:
	$(PYTHON) tools/nuclear_loop/apply.py

# ── Lint ───────────────────────────────────
lint:
	cd apps/api && $(PYTHON) -m black --check app/ tests/
	cd apps/api && $(PYTHON) -m isort --check-only app/ tests/
	cd apps/web && $(NPX) tsc --noEmit

# ── Docker ─────────────────────────────────
docker-up:
	docker-compose up -d --build
	@echo "LedgerLive running at http://localhost:3000"

docker-down:
	docker-compose down

# ── Seed ───────────────────────────────────
seed:
	$(PYTHON) demo/seed.py

# ── Format ─────────────────────────────────
format:
	cd apps/api && $(PYTHON) -m black app/ tests/
	cd apps/api && $(PYTHON) -m isort app/ tests/

# ── Coverage ───────────────────────────────
coverage:
	cd apps/api && $(PYTHON) -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# ── Security ───────────────────────────────
security:
	$(PYTHON) -m bandit -r apps/api/app/ -ll --skip B101 || true
	$(PYTHON) -m pip_audit -r requirements.txt || true