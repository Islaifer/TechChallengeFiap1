from app.core.config.database_settings import SessionLocal
from app.models.entities.user import User

class UserRepository:
    def find_by_id(self, user_id: int):
        with SessionLocal() as db:
            return db.query(User).filter(User.id == user_id).first()
        
    def find_by_email(self, user_email: str):
        with SessionLocal() as db:
            return db.query(User).filter(User.email == user_email).first()
        
    def find_by_name(self, user_name: str):
        with SessionLocal() as db:
            return db.query(User).filter(User.name == user_name).first()
        
    def has_name(self, user_name: str):
        return self.find_by_name(user_name) is not None
    
    def has_email(self, user_email: str):
        return self.find_by_email(user_email) is not None
    
    def save(self, user: User):
        with SessionLocal() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        
    def delete(self, user: User):
        with SessionLocal() as db:
            db.delete(user)
            db.commit()