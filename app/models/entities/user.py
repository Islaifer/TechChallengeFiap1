from sqlalchemy import Column, BigInteger, String
from app.core.config.database_settings import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(255), nullable=False)