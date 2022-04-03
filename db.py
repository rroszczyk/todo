from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# konfiguracja adresu i danych do logowania do bazy danych (dane logowania należy przekazać w sposób bezpieczny)
SQLALCHEMY_DB_URL = "postgresql://pgadmin:password@dione:5432/todo"

# tworzymy silnik bazy danych ORM
engine = create_engine(
    SQLALCHEMY_DB_URL,
    pool_pre_ping = True,
)

# sesja wykorzystywana podczas połączeń
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# naza baza danych
Base = declarative_base()

def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()