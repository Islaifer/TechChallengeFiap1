from app.services.security_service import SecurityService
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

user_repository = UserRepository()

security_service = SecurityService(user_repository)
user_service = UserService(user_repository)

def get_security_service():
    return security_service

def get_user_service():
    return user_service

def get_none():
    return None