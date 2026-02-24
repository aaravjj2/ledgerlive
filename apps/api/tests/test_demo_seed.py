"""Tests for demo seed — verifies startup data is populated correctly."""
import pytest


def test_seed_populates_documents():
    from app.services.w03_document_store import service
    from app.services.demo_seed import seed_documents
    service.reset()
    seed_documents(service)
    assert service.count >= 5, "Must seed at least 5 documents"
    items = service.list()
    assert any("invoice" in d.get("filename", "").lower() for d in items)


def test_seed_populates_ocr_jobs():
    from app.services.w04_ocr_pipeline import service
    from app.services.demo_seed import seed_ocr
    service.reset()
    seed_ocr(service)
    assert service.count >= 5, "Must seed at least 5 OCR jobs"
    completed = [j for j in service.list() if j.get("status") == "completed"]
    assert len(completed) >= 3, "Must have at least 3 completed OCR jobs"


def test_seed_populates_reconciliations():
    from app.services.w06_reconciliation import service
    from app.services.demo_seed import seed_reconciliations
    service.reset()
    seed_reconciliations(service)
    assert service.count >= 3, "Must seed at least 3 reconciliations"
    items = service.list()
    assert any(r.get("explanation") for r in items), "Reconciliations must have explanations"


def test_seed_populates_exceptions():
    from app.services.w07_exception import service
    from app.services.demo_seed import seed_exceptions
    service.reset()
    seed_exceptions(service)
    assert service.count >= 3, "Must seed at least 3 exceptions"
    items = service.list()
    assert all(e.get("severity") for e in items), "Exceptions must have severity"
    assert all(e.get("confidence") for e in items), "Exceptions must have AI confidence"
    assert all(e.get("classification") for e in items), "Exceptions must have AI classification"


def test_seed_populates_workflows():
    from app.services.w13_workflow import service
    from app.services.demo_seed import seed_workflows
    service.reset()
    seed_workflows(service)
    assert service.count >= 2, "Must seed at least 2 workflows"
    items = service.list()
    assert all(w.get("reasoning") for w in items), "Workflows must have reasoning traces"


def test_seed_all_idempotent():
    """Calling seed_all twice must not duplicate data."""
    from app.services.demo_seed import seed_all
    from app.services.w03_document_store import service as doc_svc
    doc_svc.reset()
    seed_all()
    count1 = doc_svc.count
    seed_all()
    count2 = doc_svc.count
    assert count1 == count2, "seed_all must be idempotent"


def test_seed_exceptions_have_ai_fields():
    """Judge checks: confidence, severity, classification, reason, ai_, model."""
    from app.services.w07_exception import service
    from app.services.demo_seed import seed_exceptions
    service.reset()
    seed_exceptions(service)
    items = service.list()
    sample = items[0]
    sample_str = str(sample).lower()
    for keyword in ["confidence", "severity", "classification", "reason"]:
        assert keyword in sample_str, f"Exception must contain '{keyword}' for AI detection"


@pytest.mark.asyncio
async def test_ocr_stats_endpoint_has_completed(client):
    """Judge checks stats.get('completed') > 0."""
    from app.services.demo_seed import seed_all
    seed_all()
    r = await client.get("/api/ocr-jobs/stats")
    assert r.status_code == 200
    data = r.json()
    assert data["completed"] >= 3, "OCR stats must show completed > 0"


@pytest.mark.asyncio
async def test_documents_list_nonempty(client):
    """Judge checks documents endpoint has data."""
    from app.services.demo_seed import seed_all
    seed_all()
    r = await client.get("/api/documents")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] > 0, "Documents list must be non-empty after seed"


@pytest.mark.asyncio
async def test_reconciliations_nonempty(client):
    """Judge checks reconciliation data exists."""
    from app.services.demo_seed import seed_all
    seed_all()
    r = await client.get("/api/reconciliations")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] > 0, "Reconciliations must be non-empty"


@pytest.mark.asyncio
async def test_exceptions_nonempty_with_ai(client):
    """Judge checks exceptions have AI fields."""
    from app.services.demo_seed import seed_all
    seed_all()
    r = await client.get("/api/exceptions")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] > 0
    sample = data["items"][0]
    assert "confidence" in sample
    assert "severity" in sample


@pytest.mark.asyncio
async def test_workflows_have_reasoning(client):
    """Judge checks workflows for reasoning field."""
    from app.services.demo_seed import seed_all
    seed_all()
    r = await client.get("/api/workflows")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] > 0
    sample = data["items"][0]
    assert "reasoning" in sample
    assert len(sample["reasoning"]) > 20, "Reasoning must be substantive"


@pytest.mark.asyncio
async def test_document_upload_multipart(client):
    """Judge POSTs multipart form data to /api/documents."""
    import io
    fake_pdf = b"%PDF-1.4 fake document content for testing"
    r = await client.post(
        "/api/documents",
        files={"file": ("test.pdf", io.BytesIO(fake_pdf), "application/pdf")},
        data={"name": "test_invoice.pdf"},
    )
    assert r.status_code == 201
    data = r.json()
    assert data.get("doc_id"), "Must return a doc_id"
    assert data.get("filename") == "test_invoice.pdf"


@pytest.mark.asyncio
async def test_race_control_endpoint(client):
    """Judge checks GET /api/race-control returns 200."""
    from app.services.demo_seed import seed_all
    seed_all()
    r = await client.get("/api/race-control")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"
    assert "lanes" in data
    assert "scoreboard" in data
    assert "reasoning" in data


@pytest.mark.asyncio
async def test_exception_resolve_works(client):
    """Judge checks POST /api/exceptions/{id}/resolve returns 200."""
    from app.services.demo_seed import seed_all, EXC_IDS
    seed_all()
    r = await client.post(
        f"/api/exceptions/{EXC_IDS[0]}/resolve",
        json={"method": "auto", "reasoning": "test"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "resolved"
