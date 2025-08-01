from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..interfaces.permissiongroup import GroupBase, GroupOut, PermissionInGroup
from ...Business_Layer.services.permission_group_service import PermissionGroupService
from ...Business_Layer.utils.permission_check import permission_required
from ..JWT.jwt_validator.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/permission-groups/unmapped", response_model=List[GroupOut])
def get_unmapped_groups(
    service: PermissionGroupService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    return service.list_unmapped_groups()

@router.get("/", dependencies=[Depends(permission_required)])
def admin_home():
    return {"message": "Group Management Route"}

@router.get("", response_model=List[GroupOut])
def list_groups(
    service: PermissionGroupService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    return service.list_groups()

@router.get("/{group_id}", response_model=GroupOut)
def get_group(
    group_id: int,
    service: PermissionGroupService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    group = service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.post("", response_model=GroupOut, status_code=201)
def create_group(
    group: GroupBase,
    service: PermissionGroupService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    try:
        return service.create_group(group.group_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{group_id}", response_model=GroupOut)
def update_group(
    group_id: int,
    group: GroupBase,
    service: PermissionGroupService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    updated = service.update_group(group_id, group.group_name)
    if not updated:
        raise HTTPException(status_code=404, detail="Group not found")
    return updated

@router.delete("/{group_id}", status_code=204)
def delete_group(
    group_id: int,
    service: PermissionGroupService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    deleted = service.delete_group(group_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Group not found")

@router.get("/{group_id}/permissions", response_model=List[PermissionInGroup])
def get_permissions_by_group(
    group_id: int,
    service: PermissionGroupService = Depends(),
    current_user: dict = Depends(get_current_user)
):
    group = service.get_group(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Permission group not found")
    return [
        {"code": code, "description": description}
        for code, description in service.list_permissions_in_group(group_id)
    ]
