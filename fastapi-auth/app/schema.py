from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    jwt_token: str

    class Config:
        orm_mode = True