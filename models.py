import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "swapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRS_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRS_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str]
    eye_color: Mapped[str]
    films: Mapped[list]
    gender: Mapped[str]
    hair_color: Mapped[str]
    height: Mapped[str]
    homeworld: Mapped[str]
    mass: Mapped[str]
    name: Mapped[str]
    skin_color: Mapped[int]
    species: Mapped[list]
    starships: Mapped[list]
    vehicles: Mapped[list]


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
