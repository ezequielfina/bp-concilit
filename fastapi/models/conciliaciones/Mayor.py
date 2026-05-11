from utils.engine_db import Base
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import DATE, UUID, NUMERIC
import uuid
from sqlalchemy.orm import relationship


class Mayor(Base):
    __tablename__ = 'mayor'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    sociedad = Column(String(32))
    cuenta = Column(String(32))
    asignacion = Column(String(64), index=True, nullable=False)
    documento = Column(String(32))
    ejercicio_mes = Column(DATE, nullable=False)
    clase_doc = Column(String(32))
    fecha_doc = Column(DATE, nullable=False)
    fecha_contabilizacion = Column(DATE, nullable=False)
    clave_contabilizacion = Column(String(32))
    importe_moneda_doc = Column(NUMERIC(12, 2))
    moneda_doc = Column(String(16))
    importe_moneda_local = Column(NUMERIC(12, 2))
    moneda_local = Column(String(16))
    texto_cab_doc = Column(String(512))
    texto = Column(String(512))
    cuenta_contrapartida = Column(String(32))
    referencia = Column(String(512))
    importe_valorado_ml2 = Column(NUMERIC(12, 2), nullable=False)
    anterior = Column(Boolean, nullable=False)

    id_cuenta = Column(UUID(as_uuid=True), ForeignKey("cuentas.id", ondelete="CASCADE"), nullable=False)

    rel_cuenta = relationship('Cuenta', back_populates='partidas')

    id_carga_mayor = Column(UUID(as_uuid=True), ForeignKey("cargas_mayor.id", ondelete="CASCADE"))

    carga_mayor = relationship('CargaMayor', back_populates='partidas')
