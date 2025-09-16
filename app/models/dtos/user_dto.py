from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.entities.user import User

class UserDto(BaseModel):
    id: int = Field(0)
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = Field(None, min_length=3, max_length=80)
    password: str = Field(..., min_length=8, max_length=16)
    
    def to_entity(self):
        user = User()
        user.name = self.name
        user.email = self.email
        user.password = self.password
        
        return user
        
    def from_entity(self, user: User):
        self.id = user.id
        self.name = user.name
        self.email = user.email
        self.password = user.password