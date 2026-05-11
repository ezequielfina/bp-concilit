from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from .banca_vs_mayor.route_bvm import router_bvm
from .alicuotas.route_alicuotas import router_alicuotas


router_conciliaciones = APIRouter(prefix="/conciliaciones", tags=["Conciliaciones"])
router_conciliaciones.include_router(router_bvm)
router_conciliaciones.include_router(router_alicuotas)


templates = Jinja2Templates(directory="templates")

@router_conciliaciones.get("/")
def root(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/index.html",
        context={}
        )
