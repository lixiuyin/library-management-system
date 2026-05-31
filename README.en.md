# Shuge · Library Management Systems

[中文](README.md) | English

This repository contains two independent course projects for library management. They share the same domain but use different technology stacks and focus on different coursework requirements.

## Projects


| Project                                       | Course               | Term              | Stack                   | Grade |
| --------------------------------------------- | -------------------- | ----------------- | ----------------------- | ----- |
| [Database Technology](database-technology/)   | Database Technology  | Fall 2022 · Major | SQL Server + Python CLI | 99    |
| [Software Engineering](software-engineering/) | Software Engineering | Fall 2023 · Minor | Flask + Vue 2 + MySQL   | 92    |


## Demo Videos

Walk-throughs and feature demos are on the project's YouTube channel:

[![Watch on YouTube](https://img.shields.io/badge/Watch%20on-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@lixiuyin)

> Click a thumbnail to play on YouTube. GitHub-flavored Markdown does not embed live YouTube players inline.

| Database Technology | Software Engineering |
|:---:|:---:|
| [![Database Technology demo video](https://img.youtube.com/vi/vDb9shPoo60/maxresdefault.jpg)](https://youtu.be/vDb9shPoo60) | [![Software Engineering demo video](https://img.youtube.com/vi/IJ76RYxe_vM/maxresdefault.jpg)](https://youtu.be/IJ76RYxe_vM) |
| SQL Server + Python CLI demo covering database setup, initialization, workflows, and database objects | Flask + Vue 2 + MySQL full-stack demo covering the reader app, admin app, and core borrowing workflows |


## Repository Layout

```text
library-management-system/
├── README.md
├── README.en.md
├── database-technology/
│   ├── README.md
│   ├── README.en.md
│   ├── start-sql-edge.sh
│   ├── init.py
│   ├── main.py
│   └── schema.sql
└── software-engineering/
    ├── README.md
    ├── README.en.md
    ├── backend/
    ├── frontend/
    │   ├── reader-app/
    │   └── admin-app/
    └── scripts/
        ├── start-all.sh
        └── start-mysql.sh
```

## Quick Start

**Database Technology project**

```bash
cd database-technology
./start-sql-edge.sh
uv sync
uv run python init.py
uv run python main.py
```

**Software Engineering project**

```bash
cd software-engineering
cp backend/.env.example backend/.env
./scripts/start-all.sh
```

See each subproject README for environment variables, default accounts, and step-by-step startup instructions.

## Notes

This repository is kept for coursework archiving, learning, and portfolio display. The database settings, dependencies, and scripts target local development. Production deployment requires new secrets, database credentials, and frontend API configuration.
