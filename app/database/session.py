### Configure SQLAlchemy    -- Create app/database/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import DATABASE_URL


class Base(DeclarativeBase):
    pass


engine_options = {}

if DATABASE_URL.startswith("sqlite"):
    engine_options["connect_args"] = {
        "check_same_thread": False   # allows multiple threads to access the same SQLite database connection simultaneously. Setting this option to False disables that safety check.
    }

'''
By default, SQLite in Python (via the built-in sqlite3 module) restricts database operations to the specific thread that created the connection. If another thread tries to use that connection, Python raises a ProgrammingError.
'''
engine = create_engine(
    DATABASE_URL,
    **engine_options,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


