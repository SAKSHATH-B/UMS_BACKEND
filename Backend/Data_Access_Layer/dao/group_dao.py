from sqlalchemy.orm import Session
from ..models.models import Permission_Group, Permission_Group_Mapping, Permissions

class PermissionGroupDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_all_groups(self):
        return self.db.query(Permission_Group).all()

    def get_group_by_id(self, group_id: int):
        return self.db.query(Permission_Group).filter_by(group_id=group_id).first()

    def get_group_by_name(self, name: str):
        return self.db.query(Permission_Group).filter_by(group_name=name).first()

    def create_group(self, group_name: str):
        new_group = Permission_Group(group_name=group_name)
        self.db.add(new_group)
        self.db.commit()
        self.db.refresh(new_group)
        return new_group

    def update_group(self, group_id: int, group_name: str):
        group = self.get_group_by_id(group_id)
        if group:
            group.group_name = group_name
            self.db.commit()
            self.db.refresh(group)
        return group

    def delete_group(self, group_id: int):
        group = self.get_group_by_id(group_id)
        if group:
            self.db.delete(group)
            self.db.commit()
        return group

    def get_unmapped_groups(self):
        mapped_ids = self.db.query(Permission_Group_Mapping.group_id).distinct()
        return self.db.query(Permission_Group).filter(~Permission_Group.group_id.in_(mapped_ids)).all()

    def get_permissions_by_group(self, group_id: int):
        return (
            self.db.query(Permissions.permission_code, Permissions.description)
            .join(Permission_Group_Mapping, Permissions.permission_id == Permission_Group_Mapping.permission_id)
            .filter(Permission_Group_Mapping.group_id == group_id)
            .all()
        )
