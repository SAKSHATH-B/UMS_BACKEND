from fastapi import APIRouter, Depends, HTTPException
from ...Business_Layer.services.permission_service import PermissionService
from ..interfaces.permission_management import (
    PermissionBase,
    PermissionOut,
    PermissionCreate,
    PermissionGroupUpdate,
    PermissionCreateU
)

from ..JWT.jwt_validator.auth.dependencies import get_current_user

router = APIRouter()
service = PermissionService()


@router.get("/", response_model=list[PermissionOut])
def list_permissions(current_user: dict = Depends(get_current_user)):
    return service.list_permissions()


@router.get("/unmapped")
def get_unmapped_permissions(current_user: dict = Depends(get_current_user)):
    return service.list_unmapped_permissions()


@router.get("/{permission_id}", response_model=PermissionOut)
def get_permission(permission_id: int, current_user: dict = Depends(get_current_user)):
    try:
        return service.get_permission(permission_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("", status_code=201)
def create_permission(
    payload: PermissionCreate,
    current_user: dict = Depends(get_current_user),
):
    existing = service.dao.get_by_id(payload.permission_code)
    if existing:
        raise HTTPException(status_code=400, detail="Permission code already exists")
    return service.create_permission_minimal(
        payload.permission_code, payload.description, payload.group_id
    )


@router.put("/{permission_id}", response_model=PermissionOut)
def update_permission(
    permission_id: int,
    payload: PermissionBase,
    current_user: dict = Depends(get_current_user),
):
    try:
        return service.update_permission(
            permission_id, payload.permission_code, payload.description
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{permission_id}")
def delete_permission(permission_id: int, current_user: dict = Depends(get_current_user)):
    try:
        service.delete_permission(permission_id)
        return {"message": "Permission deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{permission_id}/group")
def update_permission_group(
    permission_id: int,
    payload: PermissionGroupUpdate,
    current_user: dict = Depends(get_current_user),
):
    try:
        service.reassign_group(permission_id, payload.group_id)
        return {"message": "Permission reassigned to new group successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", status_code=201)
def create_permission_basic(
    permission: PermissionCreateU,
    current_user: dict = Depends(get_current_user),
):
    existing = service.dao.get_by_id(permission.permission_code)
    if existing:
        raise HTTPException(status_code=400, detail="Permission code already exists")

    return service.create_permission_minimal(
        permission.permission_code, permission.description
    )
