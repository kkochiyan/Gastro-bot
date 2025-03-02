from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, TIMESTAMP, func, String, ForeignKey, Text

from bot import SQLALCHEMY_URL

engine =  create_async_engine(url=SQLALCHEMY_URL)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    tg_id = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    created_at = mapped_column(TIMESTAMP, server_default=func.now())

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)

class Recipe(Base):
    __tablename__ = 'recipes'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger, ForeignKey('users.tg_id', ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description = mapped_column(Text)
    ingredients = mapped_column(Text, nullable=False)
    creates_at = mapped_column(TIMESTAMP, server_default=func.now())


class Step(Base):
    __tablename__ = 'steps'

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey('recipes.id', ondelete="CASCADE"))
    step_number: Mapped[int] = mapped_column(nullable=False)
    description = mapped_column(Text, nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)




