# FastAPI Calculator with BREAD + Usage Summary Report

This project is a full-stack calculator web application built with **FastAPI** and **SQLAlchemy**.  
It supports full **BREAD** operations on calculations (Browse, Read, Edit, Add, Delete), secure
**JWT-based authentication**, and a new **Usage Summary / Report** feature implemented for the final
project.

The app is fully tested with **pytest** (unit + integration) and **Playwright** (end-to-end UI tests),
containerized with **Docker**, and deployed via a **GitHub Actions** CI pipeline that runs tests and
pushes an image to Docker Hub.

---

## Final Project Feature – Usage Summary Report

For the final project requirement, I implemented a **Usage Summary / Report** feature on top of the
existing calculator.

### API

- **Endpoint:** `GET /reports/summary`
- **Response model:** `UsageSummary`
  - `total_calculations` – total number of calculation records in the database  
  - `per_operation` – list of `{ operator, count }` objects summarizing how often each operator is used  
  - `last_calculation_at` – timestamp of the most recent calculation (or `null` if none)

### UI

- **Page:** `static/report.html`
- **How it works:**
  - Simple HTML + JavaScript page
  - “Load Stats” button calls `GET /reports/summary`
  - Displays:
    - total calculations
    - last calculation timestamp
    - per-operator counts (e.g. `+: 3`, `-: 1`, etc.)

This feature demonstrates:

- Adding new Pydantic schemas (`UsageSummary`, `OperationCount`)
- Writing reusable business logic (`build_usage_summary` in `app/services/report_service.py`)
- Exposing a new FastAPI router (`app/routers/report.py`)
- Integrating backend output into a front-end page
- Covering feature with **unit tests**, **integration tests**, and a **Playwright E2E test**

---

## Main Features

- User registration and login with **JWT** authentication
- BREAD operations on calculation records:
  - Create a calculation
  - List all calculations
  - View single calculation
  - Edit / update a calculation
  - Delete a calculation
- Validation and serialization using **Pydantic**
- Persistence with **SQLAlchemy** and a relational database
- New **Usage Summary** reporting endpoint and UI
- Automated tests:
  - `pytest` unit + integration tests
  - Playwright end-to-end tests for the UI and auth flows
- Dockerized app and CI pipeline that runs tests and builds/pushes an image to Docker Hub

---

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Auth & Security:** OAuth2 with JWT, password hashing
- **Validation:** Pydantic models
- **Database:** SQL database (via SQLAlchemy engine)
- **Frontend:** HTML + vanilla JavaScript served as static files
- **Testing:**
  - `pytest` (unit + integration)
  - `Playwright` (UI / E2E)
- **DevOps:**
  - Docker
  - GitHub Actions CI (tests + Docker build + push)

---

## Project Structure (high level)

```text
app/
  main.py                 # FastAPI app, router includes, static mount
  models.py               # SQLAlchemy models
  schemas.py              # Pydantic schemas
  database.py             # DB session and engine
  oauth2.py               # JWT auth helpers
  routers/
    auth.py               # Auth routes (register/login)
    calculations.py       # BREAD routes for calculations
    report.py             # NEW usage summary report route
  services/
    report_service.py     # NEW summary-building logic
  static/
    index.html            # Main calculator UI
    report.html           # NEW usage summary UI

tests/
  test_calculation_unit.py        # existing unit tests
  test_calculation_integration.py # existing integration tests
  test_report_unit.py             # NEW unit test for summary logic
  test_report_integration.py      # NEW integration test for /reports/summary
  report.e2e.spec.ts              # NEW E2E test for summary UI (Playwright)
  ... (other existing E2E tests)


