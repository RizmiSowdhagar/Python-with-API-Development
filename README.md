# Module 14 – FastAPI Calculator (BREAD + Frontend + Tests)

This project is a calculator service built with **FastAPI** that implements full **BREAD** operations:

- **Browse** all calculations for the current user  
- **Read** a single calculation by ID  
- **Edit** an existing calculation  
- **Add** a new calculation  
- **Delete** a calculation  

It also includes:

- A small **HTML + JavaScript frontend** for interacting with the API  
- **Pytest** unit/integration tests  
- **Playwright** end-to-end tests for the UI  
- **Dockerfile** and **GitHub Actions** workflow for CI/CD

---

## Tech Stack

- Python 3.11+ / FastAPI
- SQLAlchemy + SQLite
- Pydantic v2
- HTML + CSS + vanilla JavaScript
- Pytest
- Playwright
- Docker
- GitHub Actions

---

## Project Layout

```text
app/
  main.py                # FastAPI application entrypoint
  models.py              # SQLAlchemy models
  database.py            # DB engine & SessionLocal
  oauth2.py              # Auth helpers / get_current_user
  schemas.py             # Pydantic models (Users, Calculations)
  routers/
    users.py             # /users/register, /users/login
    auth.py              # token routes (if needed)
    calculations.py      # /calculations BREAD endpoints
  static/
    index.html           # Frontend UI
    app.js               # Frontend JS logic (calls API)
tests/
  test_calculation_unit.py
  test_calculation_integration.py
  test_calculations_integration.py
  test_users_integration.py
  e2e_calculations.spec.ts   # Playwright end-to-end tests
Dockerfile
requirements.txt
