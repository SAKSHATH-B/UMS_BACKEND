from sqlalchemy.orm import Session
from ..models import models

class PermissionDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models.Permissions).all()

    def get_by_id(self, permission_id: int):
        return self.db.query(models.Permissions).filter_by(permission_id=permission_id).first()

    def get_unmapped(self):
        return self.db.query(models.Permissions).filter(
            ~models.Permissions.permission_id.in_(
                self.db.query(models.Permission_Group_Mapping.permission_id)
            )
        ).all()

    def create(self, permission_code: str, description: str):
        permission = models.Permissions(permission_code=permission_code, description=description)
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)
        return permission


        # Fetch the default group ID for 'newly_created_permissions_group'
        default_group = (
            self.db.query(models.Permission_Group)
            .filter(models.Permission_Group.group_name == "newly_created_permissions_group")
            .first()
        )
        if default_group:
            # Map permission to the default group
            mapping = models.Permission_Group_Mapping(
                permission_code=permission.permission_code,
                group_id=default_group.group_id
            )
            self.db.add(mapping)
            self.db.commit()

        return permission


    def delete(self, permission):
        self.db.delete(permission)
        self.db.commit()

    def update(self, permission, code: str, desc: str):
        permission.permission_code = code
        permission.description = desc
        self.db.commit()
        self.db.refresh(permission)
        return permission

    def update_group_mapping(self, permission_id: int, group_id: int):
        self.db.query(models.Permission_Group_Mapping).filter_by(permission_id=permission_id).delete()
        self.db.add(models.Permission_Group_Mapping(permission_id=permission_id, group_id=group_id))
        self.db.commit()

    def map_to_group(self, permission_id: int, group_id: int):
        mapping = models.Permission_Group_Mapping(
            permission_id=permission_id,
            group_id=group_id
        )
        self.db.add(mapping)
        self.db.commit()

    

