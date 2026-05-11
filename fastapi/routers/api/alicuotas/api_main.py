from fastapi import APIRouter
from .api_jurisdicciones import api_jurisdicciones


api_alicuotas = APIRouter(prefix='/alicuotas')

api_alicuotas.include_router(api_jurisdicciones)
