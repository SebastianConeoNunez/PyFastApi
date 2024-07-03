from fastapi import APIRouter,HTTPException #nuevo
from pydantic import BaseModel

router = APIRouter(prefix="/user",tags=["usuarios"]) #Nuevo

class User(BaseModel):
    id:int
    name:str
    lastname:str
    age:int
    email:str

users=[User(id=1,name="sebastian",lastname="coneo",age=12,email="sebastiancone@gmail.com"),
      User(id=2,name="yulissa",lastname="turizo",age=15,email="sebastiancone@gmail.com")]

@router.get("/todos")
async def root():
    return users

#path, se utiliza cuando es un parametro obligatorio
@router.get("/{id}")
async def ObtenerUsuarioEsp(id:int):
    user = filter(lambda user:user.id == id,users)
    try:
        usuario = list(user)[0]
        return usuario
    except:
        return f"Error el usuario con el id {id} no existe"
  
#Querey  , parametros que no sulen ser necesarios para hacer la peticion, cosas dinamicas puede que vaya en query
@router.get("/usersquery")
async def porquery(id:int):
        return funcion(id)
    
@router.post("/crear",response_model=str, status_code=201) #Nuevo
async def crearusuario(usuarioo:User):
    if type(funcion(usuarioo.id)) == User :
        raise HTTPException(status_code=404,detail="El usuario ya existe") #nuevo
       
    else:
        users.append(usuarioo)
        return "Usuario agregado"
   
#Actualizar en este caso todo el usuario , bueno una sola cosa pero creo que actualiza todo
@router.put("/actualizar")
async def actualizar(usuario: User):
    found = False
    for index,user in enumerate(users):
        if usuario.id == user.id:
            users[index]=usuario
            found= True
    if not found:
        return "usuario no encontrado"
    else:
        return "Usuario actualizado"


#Eliminar un usuario

@router.delete("/eliminar/{id}")
async def eliminar(id : int):
    found= False
    for usuario in users:
        if usuario.id == id:
            users.remove(usuario)
            found = True
    
    if not found:
        return "Uusuario no encontrado"
    else:
        return "Uusario elimnado correctamente"
        

def funcion(id):
    user = filter(lambda user:user.id == id,users)
    try:
        usuario = list(user)[0]
        return usuario
    except:
        return f"Error el usuario con el id {id} no existe"