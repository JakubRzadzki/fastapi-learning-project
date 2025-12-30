import streamlit as st
import requests

# Konfiguracja podstawowa strony
st.set_page_config(
	page_title="FastAPI Gram",
	page_icon="📸",
	layout="centered"
)

API_URL = "http://127.0.0.1:8000"

# --- ZARZĄDZANIE STANEM SESJI (Session State) ---
if "token" not in st.session_state:
	st.session_state.token = None
if "user_email" not in st.session_state:
	st.session_state.user_email = None


def login_user(email, password):
	"""Wysyła żądanie logowania i zapisuje token w sesji."""
	try:
		resp = requests.post(
			f"{API_URL}/auth/jwt/login",
			data={"username": email, "password": password}
		)
		if resp.status_code == 200:
			data = resp.json()
			st.session_state.token = data["access_token"]
			st.session_state.user_email = email
			st.success("Zalogowano pomyślnie!")
			st.rerun()
		else:
			st.error("Błąd logowania. Sprawdź login i hasło.")
	except Exception as e:
		st.error(f"Błąd połączenia z serwerem: {e}")


def register_user(email, password):
	"""Rejestruje nowego użytkownika."""
	try:
		resp = requests.post(
			f"{API_URL}/auth/register",
			json={"email": email, "password": password}
		)
		if resp.status_code == 201:
			st.success("Konto utworzone! Możesz się teraz zalogować.")
		elif resp.status_code == 400:
			st.error("Taki użytkownik już istnieje.")
		else:
			st.error(f"Wystąpił błąd: {resp.text}")
	except Exception as e:
		st.error(f"Błąd połączenia: {e}")


def logout():
	"""Wylogowuje użytkownika czyszcząc sesję."""
	st.session_state.token = None
	st.session_state.user_email = None
	st.rerun()


# --- GŁÓWNY INTERFEJS ---

st.title("📸 FastAPI Gram")

# Jeśli użytkownik NIE jest zalogowany -> Pokaż ekran logowania/rejestracji
if not st.session_state.token:
	tab1, tab2 = st.tabs(["Logowanie", "Rejestracja"])

	with tab1:
		st.header("Witaj ponownie!")
		with st.form("login_form"):
			email = st.text_input("Email")
			password = st.text_input("Hasło", type="password")
			submit = st.form_submit_button("Zaloguj się")

			if submit:
				if email and password:
					login_user(email, password)
				else:
					st.warning("Wypełnij wszystkie pola.")

	with tab2:
		st.header("Załóż konto")
		with st.form("register_form"):
			new_email = st.text_input("Email")
			new_password = st.text_input("Hasło", type="password")
			confirm_password = st.text_input("Powtórz hasło", type="password")
			submit_reg = st.form_submit_button("Zarejestruj się")

			if submit_reg:
				if new_password != confirm_password:
					st.warning("Hasła muszą być identyczne.")
				elif new_email and new_password:
					register_user(new_email, new_password)
				else:
					st.warning("Wypełnij wszystkie pola.")

# Jeśli użytkownik JEST zalogowany -> Pokaż główną aplikację
else:
	# Sidebar z informacjami o użytkowniku
	with st.sidebar:
		st.write(f"Zalogowany jako: **{st.session_state.user_email}**")
		if st.button("Wyloguj się"):
			logout()

	# Główne zakładki aplikacji
	tab_feed, tab_upload = st.tabs(["Tablica (Feed)", "Dodaj Post"])

	# --- ZAKŁADKA: DODAWANIE ---
	with tab_upload:
		st.header("Dodaj nowe zdjęcie")
		with st.form("upload_post_form", clear_on_submit=True):
			uploaded_file = st.file_uploader("Wybierz plik", type=["jpg", "png", "jpeg"])
			caption = st.text_input("Opis zdjęcia")
			submitted = st.form_submit_button("Opublikuj")

			if submitted and uploaded_file:
				# Przygotowanie nagłówków z tokenem
				headers = {"Authorization": f"Bearer {st.session_state.token}"}
				files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
				data = {"caption": caption}

				try:
					with st.spinner("Wysyłanie..."):
						resp = requests.post(f"{API_URL}/upload", files=files, data=data, headers=headers)

					if resp.status_code == 200:
						st.success("Post opublikowany!")
					elif resp.status_code == 401:
						st.error("Sesja wygasła. Zaloguj się ponownie.")
						logout()
					else:
						st.error(f"Błąd: {resp.text}")
				except Exception as e:
					st.error(f"Błąd połączenia: {e}")

	# --- ZAKŁADKA: FEED ---
	with tab_feed:
		st.subheader("Najnowsze posty")
		if st.button("Odśwież"):
			st.rerun()

		try:
			resp = requests.get(f"{API_URL}/feed")
			if resp.status_code == 200:
				posts = resp.json().get("posts", [])

				if not posts:
					st.info("Nic tu jeszcze nie ma. Dodaj pierwszy post!")

				for post in posts:
					# Wyświetlanie posta w ładnym kontenerze
					with st.container(border=True):
						col1, col2 = st.columns([2, 1])

						with col1:
							if post.get("url"):
								st.image(post["url"], use_container_width=True)

						with col2:
							st.caption(f"📅 {post.get('created_at', '')[:10]}")
							st.markdown(f"**Opis:**")
							st.write(post.get('caption', ''))

							# Przycisk usuwania (wymaga autoryzacji)
							# Uwaga: Frontend nie wie czy to "mój" post, ale backend zablokuje jeśli nie.
							if st.button("Usuń post", key=post["id"]):
								headers = {"Authorization": f"Bearer {st.session_state.token}"}
								del_resp = requests.delete(f"{API_URL}/posts/{post['id']}", headers=headers)

								if del_resp.status_code == 200:
									st.success("Usunięto!")
									st.rerun()
								elif del_resp.status_code == 403:
									st.error("To nie Twój post!")
								else:
									st.error("Błąd usuwania.")

			else:
				st.error("Nie udało się pobrać postów.")
		except Exception as e:
			st.error(f"Serwer nie odpowiada: {e}")