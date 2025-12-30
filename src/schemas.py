import uuid
from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel

class UserRead(schemas.BaseUser[uuid.UUID]):
    """Schemat do odczytu danych użytkownika (publiczny)."""
    pass

class UserCreate(schemas.BaseUserCreate):
    """Schemat do rejestracji nowego użytkownika."""
    pass

class UserUpdate(schemas.BaseUserUpdate):
    """Schemat do aktualizacji danych użytkownika."""
    pass

class PostCreate(BaseModel):
    """Schemat tworzenia posta (walidacja danych wejściowych)."""
    caption: str

class PostResponse(BaseModel):
    """Schemat zwracany przez API z danymi posta."""
    id: uuid.UUID
    caption: Optional[str]
    url: str
    file_type: str
    file_name: str
    created_at: str

    class Config:
        from_attributes = True