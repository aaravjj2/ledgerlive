"""Wave 222: Task DAG Builder v1 Router — Builds directed acyclic graph of close tasks. Nodes are close activities, edges are dependencies. Validates acyclicity, computes topological order, and tracks completion.

PROJECT_ID: LEDGERLIVE
"""
from fastapi import APIRouter, HTTPException, Request

from app.services.w222_task_dag import service

router = APIRouter(tags=["Task DAG Builder v1"])

@router.get("/api/task-dag")
async def api_task_dag_w222_list_dags(limit: int = 100):
    """List task DAGs"""
    items = service.list_dags(limit=limit)
    return {"items": items, "total": len(items)}

@router.post("/api/task-dag", status_code=201)
async def api_task_dag_w222_create_dag(request: Request):
    """Create task DAG"""
    data = await request.json()
    item = service.create_dag(data)
    return item

@router.get("/api/task-dag/report")
async def api_task_dag_w222_dag_report(limit: int = 100):
    """Get task DAG report"""
    items = service.dag_report(limit=limit)
    return {"items": items, "total": len(items)}

@router.get("/api/task-dag/{dag_id}")
async def api_task_dag_w222_get_dag(dag_id: str):
    """Get DAG details"""
    item = service.get_dag(dag_id)
    if not item:
        raise HTTPException(status_code=404, detail="task_dag not found")
    return item

@router.post("/api/task-dag/{dag_id}/edge")
async def api_task_dag_w222_add_edge(dag_id: str, request: Request):
    """Add dependency edge"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_edge(dag_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="task_dag not found")
    return item

@router.post("/api/task-dag/{dag_id}/node")
async def api_task_dag_w222_add_node(dag_id: str, request: Request):
    """Add node to DAG"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.add_node(dag_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="task_dag not found")
    return item

@router.post("/api/task-dag/{dag_id}/validate")
async def api_task_dag_w222_validate_dag(dag_id: str, request: Request):
    """Validate DAG acyclicity"""
    try:
        data = await request.json()
    except Exception:
        data = None
    item = service.validate_dag(dag_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="task_dag not found")
    return item
