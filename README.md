# Module 14 – BREAD Calculator (FastAPI)

This project is the **Module 14** assignment for implementing full BREAD (Browse, Read, Edit, Add, Delete) operations for a calculations service.

The app exposes a secured REST API using **FastAPI**, a small HTML/JS front-end for interacting with the API, automated **unit/integration tests** with `pytest`, **end-to-end tests** with **Playwright**, and a **Docker** image published to Docker Hub with a **GitHub Actions** CI/CD pipeline.

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, Pydantic v2, SQLite  
- **Auth:** JWT bearer tokens (OAuth2 password flow)  
- **Frontend:** Vanilla HTML/CSS/JavaScript in `app/static/index.html`  
- **Testing:** `pytest` (unit + integration), Playwright E2E  
- **DevOps:** Docker, Docker Hub, GitHub Actions CI  

---

## Project Structure (high level)

```text
app/
  ├── main.py                 # FastAPI app, router registration
  ├── models.py               # SQLAlchemy models (User, Calculation)
  ├── schemas.py              # Pydantic models for requests/responses
  ├── database.py             # DB engine + SessionLocal
  ├── oauth2.py               # JWT creation & get_current_user dependency
  ├── routers/
  │     ├── auth.py           # /users/register, /users/login
  │     └── calculations.py   # /calculations BREAD endpoints
  └── static/
        └── index.html        # BREAD UI (form + table)

tests/
  ├── test_calculation_unit.py
  ├── test_calculation_integration.py
  ├── test_calculations_integration.py
  ├── test_users_integration.py
  └── e2e_calculations.spec.ts   # Playwright tests

.github/
  └── workflows/
        └── ci.yml           # CI pipeline (pytest + Docker build/push)
