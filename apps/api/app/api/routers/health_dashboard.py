"""Wave 250 router — Health Dashboard v1."""
from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from app.domain.health_dashboard import get_health_dashboard_service

router = APIRouter(tags=["health-dashboard"])


class CreateReq(BaseModel):
    component: str
    status: str
    details: dict


class UpdateStatusReq(BaseModel):
    item_id: str
    status: str


@router.post("/health-dashboard/items")
async def create(req: CreateReq):
    svc = get_health_dashboard_service()
    item = svc.create(req.component, req.status, req.details)
    return {"entry_id": item.entry_id, "component": item.component, "status": item.status, "details": item.details}


@router.get("/health-dashboard/items")
async def list_all():
    svc = get_health_dashboard_service()
    return [{"entry_id": i.entry_id, "component": i.component, "status": i.status, "details": i.details} for i in svc.list_all()]


@router.get("/health-dashboard/items/{item_id}")
async def get_one(item_id: str):
    svc = get_health_dashboard_service()
    item = svc.get(item_id)
    return {"entry_id": item.entry_id, "component": item.component, "status": item.status, "details": item.details}


@router.post("/health-dashboard/status")
async def update_status(req: UpdateStatusReq):
    svc = get_health_dashboard_service()
    item = svc.update_status(req.item_id, req.status)
    return {"entry_id": item.entry_id, "status": item.status}


@router.delete("/health-dashboard/items/{item_id}")
async def delete_item(item_id: str):
    svc = get_health_dashboard_service()
    return svc.delete(item_id)


@router.get("/health-dashboard/audit")
async def audit():
    return get_health_dashboard_service().get_audit()
