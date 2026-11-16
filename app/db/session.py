from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator para inyección de sesión de base de datos en endpoints FastAPI.
    Asegura el cierre de la conexión al finalizar cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
