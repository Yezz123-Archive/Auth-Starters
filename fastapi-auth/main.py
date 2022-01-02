from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models
from app.db import SessionLocal, engine

app = FastAPI(
    title="FastAPI Auth",
    description="A Simple Demo for showing how to use FastAPI with JWT",
    version="0.0.1",
)

# Creating the database tables
models.Base.metadata.create_all(bind=engine)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )


# Handling Session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/api/register/")
def register(username: str, role: str, password: str, db: Session = Depends(get_db)):
    user = models.User(username=username, role=role)
    user.hash_password(password)
    user.create_access_token(data={"sub": username})
    print(user.jwt_token)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered successfully"} 


@app.post("/api/login/")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user.verify_password(password):
        return {"message": "Login Successfull", "status": 200, "token": user.jwt_token}
    else:
        return {"message": "Invalid Credentials", "status": 503}


@app.post("/api/valid/")
def check(token: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.jwt_token == token).first()
    if user:
        return {"message" : "Yes", "role": user.role}
    return {"message" : "No"}
