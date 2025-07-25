from fastapi import APIRouter, HTTPException, Depends
from ..interfaces.access_point import AccessPointCreate, AccessPointUpdate, AccessPointOut,CreateAPResponse
from ...Business_Layer.services.access_point_service import AccessPointService
from ..JWT.jwt_validator.auth.dependencies import get_current_user, admin_required
from typing import Dict, List

router = APIRouter()

service_factory = AccessPointService()

@router.get("/modules", response_model=List[str])
def get_all_modules(_: dict = Depends(admin_required)):
    return service_factory.list_modules()

@router.post("/", response_model=CreateAPResponse)
def create_ap(data: AccessPointCreate, _: dict = Depends(admin_required)):
    return service_factory.create_access_point(data)

@router.get("/", response_model=List[AccessPointOut])
def list_aps(_: dict = Depends(admin_required)):
    return service_factory.list()

@router.get("/{access_id}", response_model=AccessPointOut)
def get_ap(access_id: int, _: dict = Depends(admin_required)):
    return service_factory.get(access_id)

@router.put("/{access_id}", response_model=AccessPointOut)
def update_ap(access_id: int, data: AccessPointUpdate, _: dict = Depends(admin_required)):
    return service_factory.update(access_id, data)

@router.delete("/{access_id}")
def delete_ap(access_id: int, _: dict = Depends(admin_required)):
    return service_factory.delete(access_id)
