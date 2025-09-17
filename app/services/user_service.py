import bcrypt
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.models.entities.user import User
from app.models.dtos.user_dto import UserDto

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def get_user_by_id(self, id: int):
        user: User = self.user_repository.find_by_id(id)
        
        user_dto = UserDto()
        user_dto.from_entity(user)
        return user_dto
    
    def update_user(self, user_id: int, user_updated: UserDto):
        user: User = self.user_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(
            status_code=status.HTTP_404_BAD_REQUEST,
            detail="User not found",
        )
            
        if user_updated.name is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name must exist",
        )
        
        if user_updated.email is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must exist",
        )
            
        if user_updated.password is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must exist",
        )
        
        user.name = user_updated.name
        user.email = user_updated.email
        user.password = self.hash_password(user_updated.password)
        
        user = self.user_repository.save(user)
        user_updated.from_entity(user)
        
        user_updated.password = "********"
        return user_updated
    
    def hash_password(self, password: str):
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_pass.decode("utf-8")
        