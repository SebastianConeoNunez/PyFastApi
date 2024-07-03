from fastapi import APIRouter,HTTPException,status #nuevo
from MongoBase.models.user import User # Importar una clase  para poder trabajar con ella
from schemas.user import user_schema, users_schemas
from MongoBase.client import db_client
from bson import ObjectId


router = APIRouter(prefix="/userDB",tags=["usuariosDB"]) #Nuevo



users=[]

@router.get("/todos",response_model=list[User])
async def root():
    return users_schemas(db_client.local.users.find())


@router.get("/{id}")
async def ObtenerUsuarioEsp(id:str):
    try:
        usuario = funcion("_id",ObjectId(id))
        return usuario
    except:
        return f"Error el usuario con el id {id} no existe"
  

@router.get("/usersquery")
async def porquery(id:str):
        return funcion("_id",ObjectId(id))
    
@router.post("/crear",response_model=User, status_code=201) 
async def crearusuario(usuarioo:User):
    if type(funcion("email",usuarioo.email)) == User :
        raise HTTPException(status_code=404,detail="El usuario ya existe") 
       
    else:
        user_dict = dict(usuarioo) #es necesario coger lo que venga del body en un diccionario
        del user_dict["id"] #como puede que el usuario venga vacio yo quiero que entonces siempre se me borre el campo id antes de subir a la base de datos
        id = db_client.local.users.insert_one(user_dict).inserted_id #Con el insterted id podemos ver el id con el que fue insertado el objeto
        usuario = user_schema(db_client.local.users.find_one({"_id":id}))#obtener un objeto desde mogno buscando por el id, mongo crea el id pero lo llama _id. {criterio de busquedad:LoqueBusco}. Esto retorna un json
        return User(**usuario) #Puedo crear un objeto usuario a partir del diccioario 
    

@router.put("/actualizar")
async def actualizar(usuario: User):
   
    diccionario = dict(usuario)
    del diccionario["id"]
    
    try:
        db_client.local.users.find_one_and_replace({"_id":ObjectId(usuario.id)},
        diccionario)
        return funcion("_id",ObjectId(usuario.id))
    
    except:
        return "Error al intentar actualizar el usuario"
    
    
    



@router.delete("/eliminar/{id}", status_code= status.HTTP_204_NO_CONTENT)
async def eliminar(id : str):
    
    try:
         db_client.local.users.find_one_and_delete({"_id":ObjectId(id)})
    
    except:
        return "usuario no encontrado"
    
        

def funcion(key:str, value):
    try:
        user = user_schema(db_client.local.users.find_one({key:value}))
        return User(**user)
   
    except:
        return "Error el usuario no existe"