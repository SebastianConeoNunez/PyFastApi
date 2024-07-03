
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None  #Como el mongo me lo pone le pongo none que diga que no es necesario el id, en mongo el id es un str
    name:str
    lastname:str
    age:int
    email:str
