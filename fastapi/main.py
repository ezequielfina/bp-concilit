from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routers.conciliaciones.route_conciliaciones import router_conciliaciones
from routers.api.api_main import api_main

app = FastAPI()

app.include_router(router_conciliaciones)
app.include_router(api_main)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def main_menu(request: Request):
    # En versiones nuevas, 'request' se pasa PRIMERO y fuera del diccionario
    return templates.TemplateResponse(
        request=request,
        name="main_menu.html",
        context={}  # Aquí irían otros datos, como 'empresas': lista_empresas
    )
