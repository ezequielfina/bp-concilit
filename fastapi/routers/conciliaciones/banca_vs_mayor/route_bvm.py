from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


from services.ser_empresas import read_empresas
from fastapi import Depends
from sqlalchemy.orm import Session
from utils.engine_db import get_db # Tu generador de sesión



router_bvm = APIRouter(prefix="/banca-vs-mayor", tags=["Conciliaciones"])

templates = Jinja2Templates(directory="templates")


@router_bvm.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/banca_vs_mayor/tasks.html",
        context={}
    )


@router_bvm.get("/saldos-bancarios")
def index(request: Request, db: Session = Depends(get_db)):
    empresas = read_empresas(db)

    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/banca_vs_mayor/saldo_bancario.html",
        context={"empresas": empresas}
    )


@router_bvm.get("/mayor")
def index(request: Request, db: Session = Depends(get_db)):
    empresas = read_empresas(db)

    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/banca_vs_mayor/mayor.html",
        context={"empresas": empresas}
    )


@router_bvm.get("/reporte")
def index(request: Request, db: Session = Depends(get_db)):
    empresas = read_empresas(db)

    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/banca_vs_mayor/descargar_reporte.html",
        context={"empresas": empresas}
    )


@router_bvm.get("/look-partidas")
def index(request: Request, db: Session = Depends(get_db)):
    empresas = read_empresas(db)

    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/banca_vs_mayor/look_partidas.html",
        context={"empresas": empresas}
    )


@router_bvm.get("/modify-partidas")
def index(request: Request, db: Session = Depends(get_db)):
    empresas = read_empresas(db)

    return templates.TemplateResponse(
        request=request,
        name="/conciliaciones/banca_vs_mayor/modify_partidas.html",
        context={"empresas": empresas}
    )



