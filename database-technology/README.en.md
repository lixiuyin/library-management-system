# Library Management System · Database Technology

[中文](README.md) | English

This is the Fall 2022 Database Technology course project, graded 99. It is built with Microsoft SQL Server and a Python command-line client, focusing on schema design, constraints, triggers, stored procedures, views, indexes, backup, and restore.

## Features

- Admin: book management, reader management, borrowing management, admin management, backup/restore, and important operation audit records.
- Reader: book search, active loans, borrowing history, recharge/deduction records, and password changes.
- Database: primary/foreign keys, CHECK constraints, unique constraints, triggers, views, stored procedures, and non-clustered indexes.

## Stack

| Layer | Technology |
| --- | --- |
| Database | Microsoft SQL Server / Azure SQL Edge |
| SQL | T-SQL, triggers, stored procedures, views, indexes |
| App | Python 3.8+, pymssql, pandas |
| Tooling | uv, Docker |

## Layout

```text
database-technology/
├── README.md
├── README.en.md
├── start-sql-edge.sh     # Starts an Azure SQL Edge container
├── init.py               # Initializes the database, objects, and sample data
├── main.py               # Command-line client
├── schema.sql            # Full T-SQL script
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

## Quick Start

```bash
cd database-technology
./start-sql-edge.sh
uv sync
uv run python init.py
uv run python main.py
```

After initialization, the default admin account is `admin` with password `admin`.

## Runtime Notes

1. `start-sql-edge.sh` starts a local Azure SQL Edge container:

| Item | Value |
| --- | --- |
| Container | sqledge |
| Address | localhost:1433 |
| User | sa |
| Password | `SA_PASSWORD` in the script |

2. `init.py` creates the `BOOKS` database, tables, constraints, indexes, triggers, views, stored procedures, and sample data. Re-running it rebuilds the database, which is useful for demos and testing.

3. `main.py` starts the command-line client. Windows can use `keyboard` for paging; macOS uses Enter, `n`, and `q` to avoid system permission issues.

If you do not use Docker, install SQL Server manually and run `schema.sql` in SSMS or Azure Data Studio.

## Database Design Highlights

| Object | Description |
| --- | --- |
| Tables | Book categories, books, readers, active loans, historical loans, admins, recharge/deduction records, important admin operations, backup/restore records |
| Constraints | ISBN length, reader ID length, reader type, non-negative balance, book status enum, unique admin account |
| Triggers | Generate borrowing limits, enforce loan count limits, fill due dates, deduct overdue fines, protect history and audit records |
| Views | Current loan counts, total borrowing TOP10, and other reporting views |
| Stored procedures | Book listing/removal, borrowing/returning, reader/admin CRUD, password reset, recharge, backup/restore |
| Indexes | ISBN, loan join fields, historical loan join fields, recharge/deduction reader field |

The original coursework required an E-R diagram, but that file is missing. This repository keeps the implemented SQL, command-line client, and runtime documentation.

## Backup And Restore

Backup and restore are available in the admin menu. The default paths are defined in `Backup()` / `Restore()` in `main.py`; adjust them to readable/writable local paths before running on another machine.

## Notes

This is a coursework project for learning and portfolio display. The scripts target a local development database. For production or shared environments, change the password, backup paths, and connection settings first.
