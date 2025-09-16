import bcrypt
from fastapi import HTTPException, status
from app.security.jwt_provider import create_access_token, verify_token
from app.repositories.user_repository import UserRepository
from app.models.dtos.user_dto import UserDto
from app.models.entities.user import User

class SecurityService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def login(self, user: UserDto):
        user_entity: User = self.user_repository.find_by_name(user.name)
        if user_entity is None:
            user_entity = self.user_repository.find_by_email(user.email)
            if user_entity is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User or email with password combination does not exists"
                    )
        
        if user.password is None or not bcrypt.checkpw(user.password.encode("utf-8"), user_entity.password.encode("utf-8")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User or email with password combination does not exists"
                )
        
        return create_access_token(user)
    
    def register(self, user: UserDto):
        self.valid_user(user)
        new_user: User = user.to_entity()
        new_user.password = self.hash_password(user.password)
        
        new_user = self.user_repository.save(new_user)
        user.from_entity(new_user)
        user.password = "********"
        
        return user
    
    def hash_password(self, password: str):
        salt = bcrypt.gensalt()
        hashed_pass = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_pass.decode("utf-8")
    
    def validate_token(self, token: str):
        id = verify_token(token)
        user: User = self.user_repository.find_by_id(id)
        
        user_dto = UserDto()
        user_dto.from_entity(user)
        user_dto.password = "********"
        
        return user_dto
        
    def valid_user(self, user: UserDto):
        if user.name is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Name must exist",
        )
        
        if user.email is None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must exist",
        )
            
        if self.user_repository.has_name(user.name):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already exist a user with this name",
        )
            
        if self.user_repository.has_email(user.email):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already exist a user with this email",
        )
        
        return