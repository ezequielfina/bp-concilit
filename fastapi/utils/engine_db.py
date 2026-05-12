import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # <-- Cambio aquí
from sqlalchemy.pool import QueuePool

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

URI_DB = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

print(URI_DB)


# 1. Configuración del Engine con Pooling
# En producción, quieres manejar las conexiones inactivas para que no mueran
engine = create_engine(
    URI_DB,
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