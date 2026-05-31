# Shuge · Library Management Systems

[中文](README.md) | English

This repository contains two independent course projects for library management. They share the same domain but use different technology stacks and focus on different coursework requirements.

## Projects

| Project | Course | Term | Stack | Grade |
| --- | --- | --- | --- | --- |
| [Database Technology](数据库技术/) | Database Technology | Fall 2022 · Major | SQL Server + Python CLI | 99 |
| [Software Engineering](软件工程/) | Software Engineering | Fall 2023 · Minor | Flask + Vue 2 + MySQL | 92 |

## Demo Videos

| Database Technology | Software Engineering |
| --- | --- |
| <video src="./media/videos/database-technology-demo.mp4" controls width="100%"></video><br>[Open video](media/videos/database-technology-demo.mp4) | <video src="./media/videos/software-engineering-demo.mp4" controls width="100%"></video><br>[Open video](media/videos/software-engineering-demo.mp4) |

## Repository Layout

```text
library-management-system/
├── README.md
├── README.en.md
├── media/
│   └── videos/
│       ├── database-technology-demo.mp4
│       └── software-engineering-demo.mp4
├── 数据库技术/
│   ├── README.md
│   ├── README.en.md
│   ├── start-sql-edge.sh
│   ├── init.py
│   ├── main.py
│   └── schema.sql
└── 软件工程/
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
cd 数据库技术
./start-sql-edge.sh
uv sync
uv run python init.py
uv run python main.py
```

**Software Engineering project**

```bash
cd 软件工程
cp backend/.env.example backend/.env
./scripts/start-all.sh
```

See each subproject README for environment variables, default accounts, and step-by-step startup instructions.

## Notes

This repository is kept for coursework archiving, learning, and portfolio display. The database settings, dependencies, and scripts target local development. Production deployment requires new secrets, database credentials, and frontend API configuration.
