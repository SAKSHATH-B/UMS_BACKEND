from fastapi import APIRouter, Depends, HTTPException
from ..interfaces.user_management import UserBase, UserOut, UserRoleUpdate, UserWithRoleNames
from ..JWT.jwt_validator.auth.dependencies import get_current_user, admin_required
from ...Business_Layer.services.user_management_service import get_user_service_singleton

router = APIRouter()

@router.get("/")
def admin_home(current_user: dict = Depends(admin_required)):
    return {"message": "User Management Route"}

@router.get("", response_model=list[UserOut])
def list_users(current_user: dict = Depends(admin_required)):
    return get_user_service_singleton().list_users()

@router.get("/roles", response_model=list[UserWithRoleNames])
def get_users_with_roles(current_user: dict = Depends(admin_required)):
    return get_user_service_singleton().get_users_with_roles()

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, current_user: dict = Depends(admin_required)):
    user = get_user_service_singleton().get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=UserOut)
def create_user(user: UserBase, current_user: dict = Depends(admin_required)):
    try:
        return get_user_service_singleton().create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserBase, current_user: dict = Depends(admin_required)):
    try:
        return get_user_service_singleton().update_user(user_id, user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}")
def deactivate_user(user_id: int, current_user: dict = Depends(admin_required)):
    try:
        get_user_service_singleton().deactivate_user(user_id)
        return {"message": "User deactivated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{user_id}/role")
def update_user_roles(user_id: int, payload: UserRoleUpdate, current_user: dict = Depends(admin_required)):
    try:
        message = get_user_service_singleton().update_user_roles(user_id, payload.role_ids)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/roles")
def get_user_roles(user_id: int, current_user: dict = Depends(admin_required)):
    try:
        return {"roles": get_user_service_singleton().get_user_roles(user_id)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
