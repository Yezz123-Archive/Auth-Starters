from sqlalchemy import Column, Integer, String
from db import Base
from passlib.apps import custom_app_context as pwd_context
from jose import jwt
from starlette.config import Config

config = Config(".env")

SECRET_KEY = config("SECRET_KEY", default="secret")
ALGORITHM = config("ALGORITHM", default="HS256")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(122), unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String(20), index=True)
    jwt_token = Column(String(1024))

    def hash_password(self, password):
        self.hashed_password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)

    def create_access_token(self, data):
        to_encode = data.copy()
        self.jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)