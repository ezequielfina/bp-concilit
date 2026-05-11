from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from dto.conciliaciones.SaldoBancarioDTO import SaldoBancarioCreate, SaldoBancarioUpdate

from models.conciliaciones.SaldoBancario import SaldoBancario


def nuevo_saldo_bancario(saldo_data: SaldoBancarioCreate, db: Session):
    nuevo_saldo = SaldoBancario(
        fecha=saldo_data.fecha,
        saldo_ars=saldo_data.saldo_ars,
        saldo_usd=saldo_data.saldo_usd,
        id_cuenta=saldo_data.id_cuenta
    )

    db.add(nuevo_saldo)
    db.commit()

    db.refresh(nuevo_saldo)

    return nuevo_saldo


def get_saldos_bancarios_by_id_cuenta_json(id_cuenta: UUID, db: Session):
    stmt = select(SaldoBancario).where(SaldoBancario.id_cuenta == id_cuenta)

    return db.execute(stmt).scalars().all()


def get_saldo_bancario_by_id_json(id: UUID, db: Session):
    stmt = select(SaldoBancario).where(SaldoBancario.id == id)

    return db.execute(stmt).scalars().first()


def update_saldo(db: Session, id: UUID, saldo_data: SaldoBancarioUpdate):
    # 1. Lógica de búsqueda
    db_saldo = db.query(SaldoBancario).filter(SaldoBancario.id == id).first()

    if not db_saldo:
        return None  # El service retorna None, el route decide qué error lanzar

    # 2. Lógica de transformación
    update_data = saldo_data.model_dump(exclude_unset=True)

    # 3. Persistencia
    for key, value in update_data.items():
        setattr(db_saldo, key, value)

    db.commit()
    db.refresh(db_saldo)
    return db_saldo
