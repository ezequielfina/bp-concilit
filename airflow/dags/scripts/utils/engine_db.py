from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import os



def get_engine() -> Engine:
    uri: str = os.getenv('URI_DB')

    engine: Engine = create_engine(uri)

    return engine
