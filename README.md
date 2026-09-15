# Hotel Backend — Role-Based Auth API

## Stack
FastAPI + PostgreSQL + SQLAlchemy + JWT

## Roles
admin, manager, receptionist, cashier

## Setup

1. Create the database:
   createdb hotel_db

2. Copy env file and fill in your values:
   cp .env.example .env

3. Install dependencies:
   pip install -r requirements.txt

4. Seed the first admin account:
   python -m app.scripts.create_admin

5. Run the server:
   uvicorn app.main:app --reload

6. Open API docs:
   http://127.0.0.1:8000/docs

## Creating more users
- Via CLI: python -m app.scripts.create_user
- Via API: POST /auth/register (requires admin JWT token)

## Auth flow
1. POST /auth/login  → returns JWT access token + role
2. Send token as: Authorization: Bearer <token>
3. Protected routes use require_role(...) to restrict by role