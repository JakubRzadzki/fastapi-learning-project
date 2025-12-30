import uuid
import os
from sqlalchemy import Column, Text, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends

# Konfiguracja ścieżki do bazy danych (SQLite)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "test.db")
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"


class Base(DeclarativeBase):
	"""Główna klasa bazowa dla wszystkich modeli SQLAlchemy."""
	pass


class User(SQLAlchemyBaseUserTableUUID, Base):
	"""
	Model użytkownika rozszerzający standardowy model fastapi-users.
	Zawiera relację do postów.
	"""
	posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
	"""
	Model posta zawierającego zdjęcie/plik.
	"""
	__tablename__ = "posts"

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	# Klucz obcy łączący post z użytkownikiem
	user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

	caption = Column(Text, nullable=True)
	url = Column(String, nullable=False)  # URL do pliku (lokalny)
	file_type = Column(String, nullable=False)  # np. image/png
	file_name = Column(String, nullable=False)  # oryginalna nazwa pliku
	created_at = Column(DateTime, default=func.now())

	# Relacja zwrotna do użytkownika
	user = relationship("User", back_populates="posts")


# Konfiguracja silnika bazy danych
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
	"""Tworzy tabele w bazie danych przy starcie aplikacji."""
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)


async def get_async_session():
	"""Generator sesji asynchronicznej dla Dependency Injection."""
	async with async_session_maker() as session:
		yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
	"""Dostarcza adapter bazy danych użytkowników dla fastapi-users."""
	yield SQLAlchemyUserDatabase(session, User)