from fastapi import FastAPI, HTTPException, Depends
from passlib.context import CryptContext
from app.schemas import UserCreate, UserResponse
from app.database import users_collection
from app.auth import create_access_token, verify_token

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    hashed_password = get_password_hash(user.password)
    new_user = {"username": user.username, "password": hashed_password, "role": "user"}
    users_collection.insert_one(new_user)
    
    return {"username": user.username, "role": "user"}


@app.post("/login")
async def login(user: UserCreate):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/verify_token")
async def verify_user(token: str):
    return verify_token(token, HTTPException(status_code=401, detail="Invalid token"))
