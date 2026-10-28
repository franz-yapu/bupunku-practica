# Flask Biblioteca (3 capas + PostgreSQL)

1. `docker run --name pg-biblioteca -e POSTGRES_USER=biblio -e POSTGRES_PASSWORD=biblio123 -e POSTGRES_DB=biblioteca -p 5432:5432 -d postgres:16`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env`
5. `flask --app wsgi db upgrade`
6. `pytest -q`  → 16 passed
7. `flask --app wsgi run --debug`
