from fastapi import APIRouter, Depends, HTTPException
from ..interfaces.role_mangement import RoleBase, RoleOut, RolePermissionGroupUpdate
from ..JWT.jwt_validator.auth.dependencies import get_current_user,admin_required
from ...Business_Layer.services.role_service import role_service_singleton  # singleton used here

router = APIRouter()

@router.get("/")
def admin_home(current_user: dict = Depends(admin_required)):
    return {"message": "Role Management Route"}

@router.get("", response_model=list[RoleOut])
def list_roles(current_user: dict = Depends(admin_required)):
    return role_service_singleton.list_roles()

@router.get("/{role_id}", response_model=RoleOut)
def get_role(role_id: int, current_user: dict = Depends(admin_required)):
    return role_service_singleton.get_role_by_id(role_id)

@router.post("", response_model=RoleOut)
def create_role(role: RoleBase, current_user: dict = Depends(admin_required)):
    return role_service_singleton.create_role(role)

@router.put("/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role: RoleBase, current_user: dict = Depends(admin_required)):
    return role_service_singleton.update_role(role_id, role)

@router.delete("/{role_id}")
def delete_role(role_id: int, current_user: dict = Depends(admin_required)):
    return role_service_singleton.delete_role(role_id)

@router.put("/{role_id}/groups")
def update_role_permission_groups(
    role_id: int,
    payload: RolePermissionGroupUpdate,
    current_user: dict = Depends(admin_required)
):
    return role_service_singleton.update_role_permission_groups(role_id, payload)

@router.get("/{role_id}/permissions")
def get_permissions_by_role(role_id: int, current_user: dict = Depends(admin_required)):
    return role_service_singleton.get_permissions_by_role(role_id)
