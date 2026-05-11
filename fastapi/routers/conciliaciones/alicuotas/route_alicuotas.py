from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router_alicuotas = APIRouter(prefix='/alicuotas', tags=['alicuotas'])

templates = Jinja2Templates(directory='templates')


@router_alicuotas.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/alicuotas/tasks.html",
        context={}
    )


@router_alicuotas.get("/jurisdicciones")
def rend_jurisdicciones(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/alicuotas/jurisdicciones.html",
        context={}
    )


@router_alicuotas.get("/cargar-archivo")
def rend_jurisdicciones(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/alicuotas/cargar-archivo.html",
        context={}
    )


@router_alicuotas.get("/reporte")
def rend_jurisdicciones(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/alicuotas/reporte.html",
        context={}
    )
