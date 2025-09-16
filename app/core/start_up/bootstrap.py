from app.core.config.database_settings import engine, Base
from app.models.entities.user import User

def init():
    Base.metadata.create_all(bind=engine)