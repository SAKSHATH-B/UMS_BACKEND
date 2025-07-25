from pydantic import BaseModel

# Schemas
class PermissionBase(BaseModel):
    permission_code: str
    description: str

class PermissionOut(PermissionBase):
    permission_id: int
    class Config:
        from_attributes = True

class PermissionCreate(BaseModel):
    permission_code: str
    description: str
    group_id: int

class PermissionGroupUpdate(BaseModel):
    group_id: int

class PermissionCreateU(BaseModel):
    permission_code: str
    description: str