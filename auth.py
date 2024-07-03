from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

app= FastAPI()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

oauth = OAuth2PasswordBearer(tokenUrl="login") #el endpoint que me manejera la verficiacion 
crypt = CryptContext(schemes=["bcrypt"],deprecated="auto")

class User(BaseModel):
    id:int
    name:str
    lastname:str
    email:str
    diseable:bool
    

class userDB(User):
    password: str
    

user_db = {
    "sebas" : {
        "id":1,
        "name":"sebastian",
        "lastname":"coneo",
        "email":"sebas",
        "diseable":False,
        "password": "$2a$12$3IZrOW6Fh67LvETqJlFwI.GqhfR3uM/ILav/8C2hL45Piz/f8omqm"
    }
}

def searchUser (Username: str):
    if Username in user_db:
        return userDB(**user_db[Username])


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    userVerify = user_db.get(form.username)
    if not userVerify:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="el usuario no existe")
    
    user = searchUser(form.username)
    
    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="contraseña incorrecta")
    
    acces_token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc)+ acces_token_expiration
    
    token = {"sub":user.email, "exp": expire}
    
    
    return{"token jwt": jwt.encode(token,SECRET_KEY,algorithm=ALGORITHM)}
    

async def authUser(token: str = Depends(oauth)):
    excepcion = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Token invalido",
                              headers={"WWW-Authenticate": "Bearer"})
    
    print("Token recibido:", token)
    try:
     tokenVisto = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
     user = tokenVisto.get("sub")
     
     if user is None:
         print("fue invalido 1")
         raise excepcion
     

    except  InvalidTokenError:
        print("fue invalido 2")
        raise excepcion
    
    return searchUser(user)
    
    
    
async def  current(user : userDB = Depends(authUser)):
    if user.diseable:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Usuario inactivo",)
    else:
        return user
        


@app.get("/user/me")
async def me(user : userDB = Depends(current)):
    return User(id=user.id, name=user.name, lastname=user.lastname, email=user.email, diseable=user.diseable)

    

    