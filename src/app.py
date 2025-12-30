import os
import shutil
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db import Post, User, create_db_and_tables, get_async_session
from src.schemas import UserRead, UserCreate, UserUpdate, PostResponse
from src.users import auth_backend, fastapi_users, current_active_user

# Konfiguracja katalogu na pliki statyczne
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
	"""
	Zarządza cyklem życia aplikacji.
	Inicjalizuje strukturę bazy danych przy starcie serwera.
	"""
	await create_db_and_tables()
	yield


app = FastAPI(
	title="FastAPI Gram",
	description="Backend aplikacji typu social media z obsługą plików i użytkowników.",
	version="1.0.0",
	lifespan=lifespan
)

# Udostępnianie plików z folderu uploads pod ścieżką /static
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")

# --- KONFIGURACJA ROUTERÓW UŻYTKOWNIKA ---

app.include_router(
	fastapi_users.get_auth_router(auth_backend),
	prefix="/auth/jwt",
	tags=["Auth"]
)
app.include_router(
	fastapi_users.get_register_router(UserRead, UserCreate),
	prefix="/auth",
	tags=["Auth"]
)
app.include_router(
	fastapi_users.get_users_router(UserRead, UserUpdate),
	prefix="/users",
	tags=["Users"]
)


# --- ENDPOINTY APLIKACJI ---

@app.post("/upload", response_model=PostResponse, tags=["Posts"])
async def upload_post(
		file: UploadFile = File(...),
		caption: str = Form(""),
		user: User = Depends(current_active_user),
		session: AsyncSession = Depends(get_async_session)
):
	"""
	Tworzy nowy post ze zdjęciem.
	Wymaga uwierzytelnienia użytkownika (JWT).
	"""
	try:
		# Generowanie bezpiecznej, unikalnej nazwy pliku
		file_ext = os.path.splitext(file.filename)[1]
		unique_filename = f"{uuid.uuid4()}{file_ext}"
		file_path = os.path.join(UPLOAD_DIR, unique_filename)

		# Zapis fizyczny pliku na dysku
		with open(file_path, "wb") as buffer:
			shutil.copyfileobj(file.file, buffer)

		# Konstrukcja URL do pliku (w produkcji użyj zmiennej środowiskowej dla domeny)
		file_url = f"http://127.0.0.1:8000/static/{unique_filename}"

		# Tworzenie obiektu posta powiązanego z aktualnym użytkownikiem
		new_post = Post(
			caption=caption,
			url=file_url,
			file_type=file.content_type,
			file_name=unique_filename,
			user_id=user.id
		)

		session.add(new_post)
		await session.commit()
		await session.refresh(new_post)

		return new_post

	except Exception as e:
		# W przypadku błędu warto posprzątać (usunąć plik jeśli powstał),
		# ale dla uproszczenia rzucamy tylko błąd HTTP.
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="Wystąpił błąd podczas przesyłania pliku."
		)
	finally:
		await file.close()


@app.get("/feed", tags=["Posts"])
async def get_feed(session: AsyncSession = Depends(get_async_session)):
	"""
	Pobiera listę wszystkich postów, posortowaną od najnowszych.
	Endpoint publiczny (nie wymaga logowania).
	"""
	query = select(Post).order_by(Post.created_at.desc())
	result = await session.execute(query)
	posts = result.scalars().all()

	# Konwersja obiektów SQLAlchemy na słowniki dla JSON
	return {"posts": posts}


@app.delete("/posts/{post_id}", tags=["Posts"])
async def delete_post(
		post_id: str,
		user: User = Depends(current_active_user),
		session: AsyncSession = Depends(get_async_session)
):
	"""
	Usuwa post. Wymaga bycia właścicielem posta.
	Usuwa również powiązany plik z dysku.
	"""
	try:
		post_uuid = uuid.UUID(post_id)
	except ValueError:
		raise HTTPException(status_code=400, detail="Nieprawidłowy format ID.")

	result = await session.execute(select(Post).where(Post.id == post_uuid))
	post = result.scalar_one_or_none()

	if not post:
		raise HTTPException(status_code=404, detail="Post nie został znalezion.")

	# Weryfikacja uprawnień - czy usuwający jest właścicielem?
	if post.user_id != user.id:
		raise HTTPException(status_code=403, detail="Nie masz uprawnień do usunięcia tego posta.")

	# Usunięcie pliku z systemu plików
	file_path = os.path.join(UPLOAD_DIR, post.file_name)
	if os.path.exists(file_path):
		try:
			os.remove(file_path)
		except OSError:
			pass  # Ignorujemy błędy systemu plików przy usuwaniu, by nie blokować DB

	await session.delete(post)
	await session.commit()

	return {"status": "success", "message": "Post został usunięty."}