from uuid import UUID

from dto.conciliaciones.alicuotas.JurisdiccionDTO import JurisdiccionCreate
from models.conciliaciones.alicuotas.Jurisdiccion import Jurisdiccion
from sqlalchemy.orm import Session
from sqlalchemy import select


def insert_nueva_jurisdiccion(jurisdiccion_data: JurisdiccionCreate, db: Session):
    nueva_jurisdiccion = Jurisdiccion(nombre=jurisdiccion_data.nombre)

    db.add(nueva_jurisdiccion)
    db.commit()

    db.refresh(nueva_jurisdiccion)

    return nueva_jurisdiccion


def read_all_jurisdicciones(db: Session):
    stmt = select(Jurisdiccion)

    return db.execute(stmt).scalars().all()


def read_jurisdiccion_by_id(id: UUID, db: Session):
    stmt = select(Jurisdiccion).where(Jurisdiccion.id == id)

    return db.execute(stmt).scalars().first()
