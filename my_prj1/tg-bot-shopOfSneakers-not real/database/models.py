from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

import os
from dotenv import load_dotenv

# Создаем БД
load_dotenv()
engine = create_async_engine(url=os.getenv("SQLALCHEMY_URL"))
# Подкючаемся к БД
async_session = async_sessionmaker(engine)
# Таблица БД
class Base(AsyncAttrs, DeclarativeBase):
    pass
# Таблица пользователей, хранит id юзеров в тг
class User(Base):
    __tablename__ = 'users' # Название таблицы

    id: Mapped[int] = mapped_column(primary_key=True) # Поле таблицы
    tg_id = mapped_column(BigInteger)
# Таблица категорий товара
class Category(Base):
    __tablename__ = 'categories'
     
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
# Таблица с самими товарами 
class Item(Base):
    __tablename__ = 'items'
     
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    describtion: Mapped[str] = mapped_column(String(125))
    price: Mapped[int] = mapped_column()
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))

# Начало сессии
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)