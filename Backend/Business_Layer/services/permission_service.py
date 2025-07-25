from fastapi import HTTPException
from ...Data_Access_Layer.dao.permission_dao import PermissionDAO
from ...Data_Access_Layer.dao.group_dao import PermissionGroupDAO
from ...Data_Access_Layer.dao.access_point_dao import AccessPointDAO
from ...Data_Access_Layer.utils.dependency import SessionLocal


class PermissionService:
    def __init__(self):
        self.db = SessionLocal()
        self.dao = PermissionDAO(self.db)
        self.group_dao = PermissionGroupDAO(self.db)
        self.access_point_dao = AccessPointDAO(self.db)

    def create_permission_minimal(self, permission_code: str, description: str, group_id: int = None):
        permission = self.dao.create(permission_code=permission_code, description=description)

        if not group_id:
            default_group = self.group_dao.get_group_by_name("newly_created_permissions_group")
            if not default_group:
                raise HTTPException(status_code=500, detail="Default group not found")
            group_id = default_group.group_id
        else:
            group = self.group_dao.get_group_by_id(group_id)
            if not group:
                raise HTTPException(status_code=404, detail="Group not found")

        self.dao.map_to_group(permission.permission_id, group_id)

        return {
            "message": "Permission created and assigned to group",
            "permission_id": permission.permission_id,
            "group_id": group_id
        }

    def list_permissions(self):
        return self.dao.get_all()

    def get_permission(self, permission_id):
        permission = self.dao.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")
        return permission

    def update_permission(self, permission_id, code, desc):
        permission = self.dao.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")
        return self.dao.update(permission, code, desc)

    def delete_permission(self, permission_id):
        permission = self.dao.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")
        self.dao.delete(permission)

    def reassign_group(self, permission_id, group_id):
        permission = self.dao.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")
        self.dao.update_group_mapping(permission_id, group_id)

    def list_unmapped_permissions(self):
        return self.dao.get_unmapped()
