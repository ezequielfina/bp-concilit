from uuid import UUID

from sqlalchemy.orm import Session
from models.Empresa import Empresa # Tu modelo de SQLAlchemy
from sqlalchemy import select
from dto.EmpresaDTO import EmpresaCreate, EmpresaUpdate


def read_empresas(db: Session):
    stmt = select(Empresa)

    return db.execute(stmt).scalars().all()


def read_empresa_by_id(id: UUID, db: Session):
    stmt = select(Empresa).where(Empresa.id == id)

    return db.execute(stmt).scalars().all()


def insert_empresa(empresa_data: EmpresaCreate, db: Session):
    nueva_empresa = Empresa(
        razon_social=empresa_data.razon_social,
        cuit=empresa_data.cuit
    )

    db.add(nueva_empresa)
    db.commit()

    db.refresh(nueva_empresa)

    return nueva_empresa


def update_empresa(empresa_data: EmpresaUpdate, id: UUID, db: Session):
    db_saldo = db.query(Empresa).where(Empresa.id == id).first()

    if not db_saldo:
        return None

    update_data = empresa_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_saldo, key, value)

    db.commit()
    db.refresh(db_saldo)

    return db_saldo
