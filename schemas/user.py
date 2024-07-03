def user_schema(user) :
    return{
        "id":str(user["_id"]), #lo volvemos str pq esto viene de base de datos en otro formagto
        "name":user["name"],
        "lastname":user["lastname"],
        "age":user["age"],
        "email":user["email"]
    }
    
    
def users_schemas(listaMongo):
    lista=[]
    for i in listaMongo:
        lista.append(user_schema(i))
    return  lista


    
    
    #esto lo que hace es que pasa de un json a un diccionario, para buscar tendro del json un atributo lo ponemos entre []