from sqlalchemy import select
from sqlalchemy.orm import Session
from models.conciliaciones.Cuenta import Cuenta
from uuid import UUID
from dto.conciliaciones.CuentaDTO import CuentaCreate, CuentaUpdate


def read_cuentas_by_id_empresa(empresa_id: UUID, db: Session):
    stmt = select(Cuenta).where(Cuenta.id_empresa == empresa_id)

    return db.execute(stmt).scalars().all()


def read_cuenta_by_id(id: UUID, db: Session):
    stmt = select(Cuenta).where(Cuenta.id == id)

    return db.execute(stmt).scalars().first()


def insert_nueva_cuenta(cuenta_data: CuentaCreate, db: Session):
    nueva_cuenta = Cuenta(
        nombre=cuenta_data.nombre,
        comentario=cuenta_data.comentario,
        id_empresa=cuenta_data.id_empresa
    )

    db.add(nueva_cuenta)
    db.commit()

    db.refresh(nueva_cuenta)

    return nueva_cuenta


def update_nueva_cuenta(cuenta_data: CuentaUpdate, id: UUID, db: Session):
    db_cuenta = db.query(Cuenta).where(Cuenta.id == id).first()

    if not db_cuenta:
        return None

    update_cuenta = cuenta_data.model_dump(exclude_unset=True)

    for key, value in update_cuenta.items():
        setattr(db_cuenta, key, value)

    db.commit()
    db.refresh(db_cuenta)

    return db_cuenta
