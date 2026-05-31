# Shuge · Library Management Systems

[中文](README.md) | English

This repository contains two independent course projects for library management. They share the same domain but use different technology stacks and focus on different coursework requirements.

## Projects

| Project | Course | Term | Stack | Grade |
| --- | --- | --- | --- | --- |
| [Database Technology](database-technology/) | Database Technology | Fall 2022 · Major | SQL Server + Python CLI | 99 |
| [Software Engineering](software-engineering/) | Software Engineering | Fall 2023 · Minor | Flask + Vue 2 + MySQL | 92 |

## Demo Videos

The README player loads HD videos from the `main` branch, and the browser video controls include fullscreen playback. The original HD files remain in `media/videos/`; the Software Engineering demo also includes an H.264 HD playback copy to avoid HEVC compatibility issues in some browsers.

| Database Technology | Software Engineering |
| --- | --- |
| <video src="https://raw.githubusercontent.com/lixiuyin/library-management-system/refs/heads/main/media/videos/database-technology-demo.mp4" poster="./media/videos/database-technology-demo-poster.jpg" controls preload="metadata" width="420"></video><br>[Open HD video](https://raw.githubusercontent.com/lixiuyin/library-management-system/refs/heads/main/media/videos/database-technology-demo.mp4) | <video src="https://raw.githubusercontent.com/lixiuyin/library-management-system/refs/heads/main/media/videos/software-engineering-demo-web-hd.mp4" poster="./media/videos/software-engineering-demo-poster.jpg" controls preload="metadata" width="420"></video><br>[Open HD video](https://raw.githubusercontent.com/lixiuyin/library-management-system/refs/heads/main/media/videos/software-engineering-demo-web-hd.mp4) |

## Repository Layout

```text
library-management-system/
├── README.md
├── README.en.md
├── media/
│   └── videos/
│       ├── database-technology-demo.mp4
│       ├── database-technology-demo-poster.jpg
│       ├── software-engineering-demo.mp4
│       ├── software-engineering-demo-web-hd.mp4
│       └── software-engineering-demo-poster.jpg
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
