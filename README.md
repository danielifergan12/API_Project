# Media Library API

Backend web API for managing a personal media library (movies, series, books, etc.) built with FastAPI and SQLite, for the COMP3011 coursework.

## Setup

1. Create and activate virtual environment:

```bash
cd /Users/danielifergan/API_Project
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the development server:

```bash
uvicorn app.main:app --reload
```

4. Open the automatic API docs:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc


