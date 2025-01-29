from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

engine = create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db-postgres/{POSTGRES_DB}", echo=True)


Session = sessionmaker(bind=engine)


def get_session():
    return Session()

