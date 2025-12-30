# 📸 FastAPI Gram

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)

Prosta aplikacja typu social media (klon Instagrama) stworzona w celu nauki frameworka **FastAPI**. Projekt obsługuje pełny proces rejestracji i logowania użytkowników (JWT), przesyłanie plików (zdjęć) oraz ich wyświetlanie w formie feedu.

## 🚀 Funkcjonalności

### Dla Użytkownika:
* 🔐 **Rejestracja i Logowanie:** Bezpieczne uwierzytelnianie przy użyciu JWT.
* 📤 **Upload Zdjęć:** Przesyłanie plików graficznych z opisem.
* 🖼️ **Feed:** Przeglądanie najnowszych postów od wszystkich użytkowników.
* 🗑️ **Zarządzanie:** Możliwość usuwania własnych postów.

### Technologia:
* **Backend:** FastAPI (Asynchroniczne endpointy)
* **Baza danych:** SQLite (dla prostoty) + SQLAlchemy (Async)
* **Frontend:** Streamlit (Interfejs w Pythonie)
* **Auth:** FastAPI Users (Bearear Token + JWT Strategy)
* **Pliki:** Lokalne przechowywanie w folderze `uploads/`

---

## 🛠️ Instalacja i Uruchomienie

### 1. Klonowanie i środowisko
Zaleca się użycie wirtualnego środowiska (`venv`), aby nie zaśmiecać systemu.

```bash
# Sklonuj repozytorium (jeśli pobierasz z GH) lub wejdź do folderu
cd nazwa-twojego-folderu

# Stwórz środowisko wirtualne
python -m venv .venv

# Aktywuj środowisko:
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
2. Instalacja zależności
Bash

# Zainstaluj wszystkie biblioteki zdefiniowane w pyproject.toml
pip install .
3. Uruchomienie Backendu (Serwer)
Serwer wystartuje na porcie 8000. Przy pierwszym uruchomieniu automatycznie utworzy plik bazy danych test.db oraz folder uploads.

Bash

uvicorn src.app:app --reload
📄 Dokumentacja API (Swagger): http://127.0.0.1:8000/docs

4. Uruchomienie Frontendu
W nowym oknie terminala (pamiętaj o aktywacji .venv) uruchom interfejs:

Bash

streamlit run frontend.py
📂 Struktura Projektu
Plaintext

├── src/
│   ├── app.py       # Główny plik aplikacji, konfiguracja FastAPI i endpointy
│   ├── db.py        # Modele bazy danych i konfiguracja SQLAlchemy
│   ├── schemas.py   # Schematy Pydantic (walidacja danych wejścia/wyjścia)
│   └── users.py     # Logika autentykacji i menedżer użytkowników
├── uploads/         # Folder na przesłane zdjęcia (tworzony automatycznie)
├── frontend.py      # Interfejs użytkownika w Streamlit
├── pyproject.toml   # Lista zależności projektu
└── test.db          # Plik bazy danych SQLite (tworzony automatycznie)

📝 Licencja
Projekt stworzony w celach edukacyjnych.