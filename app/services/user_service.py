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