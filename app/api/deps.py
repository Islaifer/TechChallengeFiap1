from app.services.security_service import SecurityService
from app.repositories.user_repository import UserRepository

user_repository = UserRepository()

security_service = SecurityService(user_repository)

def get_security_service():
    return security_service