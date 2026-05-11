import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # <-- Cambio aquí
from sqlalchemy.pool import QueuePool

load_dotenv()

# 1. Configuración del Engine con Pooling
# En producción, quieres manejar las conexiones inactivas para que no mueran
engine = create_engine(
    os.getenv('URI_DB'),
    pool_size=10,            # Conexiones mantenidas abiertas
    max_overflow=20,         # Conexiones extra si hay picos de tráfico
    pool_pre_ping=True       # Verifica si la conexión sigue viva antes de usarla
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. CREAR EL OBJETO BASE (Estilo Moderno 2.0+)
class Base(DeclarativeBase):
    pass

# 3. Dependencia de FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()