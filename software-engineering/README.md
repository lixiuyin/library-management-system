# 图书管理系统 · 软件工程

中文 | [English](README.en.md)

2023 年秋季「软件工程」课程项目，成绩 92。项目采用前后端分离架构：Flask 后端 API、Vue 2 读者端、Vue 2 管理端，以及 MySQL 数据库。

## 功能

- 读者端：登录、图书检索、当前借阅、历史借阅、充值记录、重要操作记录和密码修改。
- 管理端：图书与分类管理、读者管理、借书/续借/还书、管理员管理、重要操作审计和借阅排行。
- 后端：RESTful API、JWT 鉴权、SQLAlchemy 数据模型、CORS 配置和初始化种子数据。

## 技术栈

| 层次 | 技术 |
| --- | --- |
| 数据库 | MySQL 5.7+ / MariaDB |
| 后端 | Python 3.7+、Flask、SQLAlchemy、Flask-JWT-Extended |
| 前端 | Vue 2、Vue Router、Element UI、Axios |
| 工具 | uv、npm、Docker |

## 目录结构

```text
software-engineering/
├── README.md
├── README.en.md
├── backend/                 # Flask 后端，默认端口 8088
│   ├── app/
│   │   ├── controllers/     # 业务函数，文件采用 snake_case 命名
│   │   ├── models/
│   │   └── views/
│   ├── api.md               # API 说明
│   ├── run.py
│   ├── seed.py
│   ├── pyproject.toml
│   └── .env.example
├── frontend/
│   ├── reader-app/          # 读者端，默认端口 8081
│   └── admin-app/           # 管理端，默认端口 8083
└── scripts/
    ├── start-all.sh         # 一键启动 MySQL、后端和双前端
    └── start-mysql.sh       # 启动本地 MySQL 容器
```

## 快速开始

```bash
cd software-engineering
cp backend/.env.example backend/.env
./scripts/start-all.sh
```

`start-all.sh` 会依次启动 MySQL、导入种子数据、启动 Flask 后端和两个前端。

| 服务 | 地址 |
| --- | --- |
| 后端 API | http://127.0.0.1:8088 |
| 读者端 | http://localhost:8081 |
| 管理端 | http://localhost:8083 |
| MySQL | 127.0.0.1:3306 |

## 分步运行

1. 启动数据库：

```bash
cd software-engineering
./scripts/start-mysql.sh
```

2. 启动后端：

```bash
cd software-engineering/backend
uv sync
uv run python seed.py
uv run python run.py
```

3. 启动读者端：

```bash
cd software-engineering/frontend/reader-app
npm install
npm run serve
```

4. 启动管理端：

```bash
cd software-engineering/frontend/admin-app
npm install
npm run serve
```

## 配置

后端配置从 `backend/.env` 读取。复制 `backend/.env.example` 后填写实际数据库账号和 JWT 密钥。

| 变量 | 必填 | 说明 | 示例 |
| --- | --- | --- | --- |
| `DB_USERNAME` | 是 | 数据库用户 | root |
| `DB_PASSWORD` | 是 | 数据库密码 | `start-mysql.sh` 中的 `ROOT_PASSWORD` |
| `DB_HOST` | 是 | 数据库主机和端口 | 127.0.0.1:3306 |
| `DB_NAME` | 是 | 数据库名 | book_system |
| `JWT_SECRET_KEY` | 是 | JWT 签名密钥 | 随机长字符串 |
| `FLASK_PORT` | 否 | 后端端口 | 8088 |
| `CORS_ORIGINS` | 否 | 允许的前端来源 | `http://localhost:8081,http://localhost:8083` |

前端开发环境的 API 地址在两个应用的 `.env.development` 中配置，默认指向 `http://127.0.0.1:8088`。

## 文档

- [后端 API 文档](backend/api.md)
- [根目录 README](../README.md)

## 说明

本项目为课程作业，仅供学习与展示。生产部署前需要替换默认密钥、数据库密码，并根据部署环境调整 CORS 和 API 地址。
