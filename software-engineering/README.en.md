# Library Management System · Software Engineering

[中文](README.md) | English

This is the Fall 2023 Software Engineering course project, graded 92. It uses a separated frontend/backend architecture with a Flask API, two Vue 2 frontends, and a MySQL database.

## Features

- Reader app: login, book search, active loans, borrowing history, recharge records, important operation records, and password changes.
- Admin app: book and category management, reader management, borrowing workflows, admin management, audit records, and borrowing rankings.
- Backend: RESTful APIs, JWT authentication, SQLAlchemy models, CORS configuration, and seed data initialization.

## Stack

| Layer | Technology |
| --- | --- |
| Database | MySQL 5.7+ / MariaDB |
| Backend | Python 3.7+, Flask, SQLAlchemy, Flask-JWT-Extended |
| Frontend | Vue 2, Vue Router, Element UI, Axios |
| Tooling | uv, npm, Docker |

## Layout

```text
软件工程/
├── README.md
├── README.en.md
├── backend/                 # Flask backend, default port 8088
│   ├── app/
│   │   ├── controllers/     # Business functions, snake_case file names
│   │   ├── models/
│   │   └── views/
│   ├── api.md               # API reference
│   ├── run.py
│   ├── seed.py
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── reader-app/          # Reader app, default port 8081
│   └── admin-app/           # Admin app, default port 8083
└── scripts/
    ├── start-all.sh         # Starts MySQL, backend, and both frontends
    └── start-mysql.sh       # Starts a local MySQL container
```

## Quick Start

```bash
cd 软件工程
cp backend/.env.example backend/.env
./scripts/start-all.sh
```

`start-all.sh` starts MySQL, imports seed data, then launches the Flask backend and both frontend apps.

| Service | URL |
| --- | --- |
| Backend API | http://127.0.0.1:8088 |
| Reader app | http://localhost:8081 |
| Admin app | http://localhost:8083 |
| MySQL | 127.0.0.1:3306 |

## Manual Startup

1. Start the database:

```bash
cd 软件工程
./scripts/start-mysql.sh
```

2. Start the backend:

```bash
cd 软件工程/backend
uv sync
uv run python seed.py
uv run python run.py
```

3. Start the reader app:

```bash
cd 软件工程/frontend/reader-app
npm install
npm run serve
```

4. Start the admin app:

```bash
cd 软件工程/frontend/admin-app
npm install
npm run serve
```

## Configuration

Backend configuration is loaded from `backend/.env`. Copy `backend/.env.example` and fill in the database credentials and JWT secret.

| Variable | Required | Description | Example |
| --- | --- | --- | --- |
| `DB_USERNAME` | Yes | Database user | root |
| `DB_PASSWORD` | Yes | Database password | `ROOT_PASSWORD` in `start-mysql.sh` |
| `DB_HOST` | Yes | Database host and port | 127.0.0.1:3306 |
| `DB_NAME` | Yes | Database name | book_system |
| `JWT_SECRET_KEY` | Yes | JWT signing secret | long random string |
| `FLASK_PORT` | No | Backend port | 8088 |
| `CORS_ORIGINS` | No | Allowed frontend origins | `http://localhost:8081,http://localhost:8083` |

The frontend API base URL is configured in each app's `.env.development`, and defaults to `http://127.0.0.1:8088`.

## Documentation

- [Backend API reference](backend/api.md)
- [Repository README](../README.en.md)

## Notes

This is a coursework project for learning and portfolio display. Before production deployment, replace default secrets and database passwords, then adjust CORS and API URLs for the target environment.
