from fastapi import APIRouter
from .api_empresas import api_empresas
from .api_cuentas import api_cuentas
from .api_saldos_bancarios import api_saldos_bancarios
from .api_mayor import api_mayor
from .api_reporte import api_reporte
from .alicuotas.api_main import api_alicuotas


api_main = APIRouter(prefix="/api_v1", tags=["API_V1"])

api_main.include_router(api_empresas)
api_main.include_router(api_cuentas)
api_main.include_router(api_saldos_bancarios)
api_main.include_router(api_mayor)
api_main.include_router(api_reporte)


api_main.include_router(api_alicuotas)