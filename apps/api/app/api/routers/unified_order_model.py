"""Wave 212 router — Unified Order Model v1."""
from __future__ import annotations
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel
from app.domain.unified_order_model import get_unified_order_model_service

router = APIRouter(tags=["unified-order-model"])


class CreateOrderReq(BaseModel):
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None
    stop_price: Optional[float] = None


class SubmitReq(BaseModel):
    order_id: str


class FillReq(BaseModel):
    order_id: str
    fill_qty: float
    fill_price: float


class CancelReq(BaseModel):
    order_id: str


class RejectReq(BaseModel):
    order_id: str
    reason: str = ""


@router.post("/unified-order-model/orders")
async def create_order(req: CreateOrderReq):
    svc = get_unified_order_model_service()
    o = svc.create_order(req.symbol, req.side, req.order_type, req.quantity, req.price, req.stop_price)
    return {"order_id": o.order_id, "symbol": o.symbol, "side": o.side, "order_type": o.order_type, "quantity": o.quantity, "status": o.status}


@router.post("/unified-order-model/submit")
async def submit_order(req: SubmitReq):
    svc = get_unified_order_model_service()
    o = svc.submit_order(req.order_id)
    return {"order_id": o.order_id, "status": o.status}


@router.post("/unified-order-model/fill")
async def fill_order(req: FillReq):
    svc = get_unified_order_model_service()
    o = svc.fill_order(req.order_id, req.fill_qty, req.fill_price)
    return {"order_id": o.order_id, "status": o.status, "filled_quantity": o.filled_quantity, "filled_avg_price": o.filled_avg_price}


@router.post("/unified-order-model/cancel")
async def cancel_order(req: CancelReq):
    svc = get_unified_order_model_service()
    o = svc.cancel_order(req.order_id)
    return {"order_id": o.order_id, "status": o.status}


@router.post("/unified-order-model/reject")
async def reject_order(req: RejectReq):
    svc = get_unified_order_model_service()
    o = svc.reject_order(req.order_id, req.reason)
    return {"order_id": o.order_id, "status": o.status}


@router.get("/unified-order-model/orders")
async def list_orders():
    svc = get_unified_order_model_service()
    return [{"order_id": o.order_id, "symbol": o.symbol, "side": o.side, "status": o.status, "quantity": o.quantity} for o in svc.list_orders()]


@router.get("/unified-order-model/orders/{order_id}")
async def get_order(order_id: str):
    svc = get_unified_order_model_service()
    o = svc.get_order(order_id)
    return {"order_id": o.order_id, "symbol": o.symbol, "side": o.side, "order_type": o.order_type, "status": o.status, "quantity": o.quantity, "filled_quantity": o.filled_quantity}


@router.get("/unified-order-model/timeline/{order_id}")
async def get_timeline(order_id: str):
    svc = get_unified_order_model_service()
    return svc.get_timeline(order_id)


@router.get("/unified-order-model/events")
async def get_events():
    svc = get_unified_order_model_service()
    return [{"event_id": e.event_id, "order_id": e.order_id, "event_type": e.event_type, "timestamp": e.timestamp} for e in svc.get_events()]
