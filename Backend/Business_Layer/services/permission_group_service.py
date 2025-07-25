from sqlalchemy.orm import Session
from ...Data_Access_Layer.dao.group_dao import PermissionGroupDAO
from ...Data_Access_Layer.utils.dependency import SessionLocal  # your SQLAlchemy session factory

class PermissionGroupService:
    def __init__(self):
        self.db: Session = SessionLocal()  # session created internally
        self.dao = PermissionGroupDAO(self.db)

    def list_groups(self):
        return self.dao.get_all_groups()

    def get_group(self, group_id: int):
        return self.dao.get_group_by_id(group_id)

    def create_group(self, group_name: str):
        existing = self.dao.get_group_by_name(group_name)
        if existing:
            raise ValueError("Group name already exists")
        return self.dao.create_group(group_name)

    def update_group(self, group_id: int, group_name: str):
        return self.dao.update_group(group_id, group_name)

    def delete_group(self, group_id: int):
        return self.dao.delete_group(group_id)

    def list_unmapped_groups(self):
        return self.dao.get_unmapped_groups()

    def list_permissions_in_group(self, group_id: int):
        return self.dao.get_permissions_by_group(group_id)
