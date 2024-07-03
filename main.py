from fastapi import FastAPI
from routers import user,userDb #Importar
from fastapi.staticfiles import StaticFiles




app = FastAPI()
app.include_router(user.router) #Importar
app.include_router(userDb.router)
app.mount("/static",StaticFiles(directory="static"),name="static")


@app.get("/")
async def root():
    return "Hello World"

@app.get("/perfil")
async def url():
    return { "url":"sapo"}