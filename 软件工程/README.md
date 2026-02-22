# 图书管理系统 · 软件工程课程项目

**软件工程 · 课程项目** | 2023 年秋 · **辅修**项目 · **课程成绩 92 分**

2023 年秋季学期「软件工程」课程的辅修项目。前后端分离的图书借阅管理系统：**Flask 后端 API** + **Vue 2 双前端**（读者端 / 管理端），使用 MySQL 数据库。

## 项目概述

| 项目属性   | 说明                     |
| ---------- | ------------------------ |
| 课程       | 软件工程                 |
| 学期与性质 | 2023 年秋 · 辅修项目     |
| 课程成绩   | 92 分                    |
| 数据库     | MySQL                    |
| 应用层     | Flask 后端 + Vue 2 双前端 |

## 技术栈

| 层次     | 技术                                   |
| -------- | -------------------------------------- |
| 数据库   | MySQL 5.7+（或 MariaDB、云数据库）     |
| 后端     | Python 3.7+、Flask、SQLAlchemy、JWT    |
| 前端     | Vue 2、Node.js 14+、npm               |

## 项目结构

```
软件工程/
├── README.md                    # 本文件
├── docker.sh                    # MySQL 容器（可选，用于本地数据库）
├── start.sh                     # 一键启动：MySQL → 后端 → 双前端
├── work/                        # 后端（Flask，默认端口 8088）
│   ├── run.py                   # 启动入口
│   ├── pyproject.toml / requirements.txt  # 依赖（推荐 uv，见下方）
│   ├── .env.example             # 环境变量示例（复制为 .env 后填写）
│   ├── API.md                   # 后端接口说明（路由、鉴权、请求/响应）
│   └── app/
│       ├── config.py            # 配置（从环境变量读取）
│       ├── models/               # 数据模型
│       ├── controllers/         # 业务逻辑
│       └── views/               # API 路由
└── system/
    ├── book-management-system   # 前端：读者端，端口 8081
    └── book-manager-system      # 前端：管理端，端口 8083
```

## 功能概览

- **读者端**：登录、图书检索、当前/历史借阅、充值记录、重要操作查看、修改密码等。
- **管理端**：图书与分类、读者、借阅（借书/续借/还书）、管理员管理，重要操作记录，借阅排行等。
- **后端**：RESTful API，JWT 鉴权，MySQL + SQLAlchemy，CORS 支持前后端分离。

接口文档：后端路由、方法、鉴权及主要请求/响应说明见 `work/API.md`。

## 环境与运行

### 环境要求

- **Python** 3.7+（后端）
- **Node.js** 14+、npm（前端）
- **MySQL** 5.7+ 或兼容（如 MariaDB）。可使用本目录 `docker.sh` 启动 MySQL 容器。

### 快速开始

**方式一：一键启动（推荐）**

```bash
cd 软件工程
chmod +x start.sh && ./start.sh
```

`start.sh` 会依次启动 MySQL 容器、后端（端口 8088）与双前端（读者端 8081、管理端 8083）。首次使用前需在 `work/` 下配置 `.env`（见下方配置说明），并与 `docker.sh` 中的数据库账号、库名一致。

**方式二：分步运行**

1. **数据库** — 执行 `docker.sh` 启动 MySQL 容器，或自行创建数据库（如 `book_system`）并保证可连接。
2. **后端** — 在 `work/` 下安装依赖并启动：
   - 推荐使用 **uv**：`cd work && uv sync`，然后 `uv run python run.py`。
   - 或使用 pip：`pip install -r requirements.txt`，然后 `python run.py`。
   - 首次运行会执行 `db.create_all()` 建表。后端默认监听 **http://127.0.0.1:8088**（可在 `work/.env` 中设置 `FLASK_PORT`）。
3. **前端** — 在两个前端目录分别安装并启动：
   - 读者端：`cd system/book-management-system && npm install && npm run serve`（http://localhost:8081）
   - 管理端：`cd system/book-manager-system && npm install && npm run serve`（http://localhost:8083）

两个前端的 API 基地址在 `.env.development` 中配置为 `http://127.0.0.1:8088`，与 `start.sh` 及后端默认端口一致。`npm run serve` / `npm run build` 已使用 `cross-env`，Windows / macOS / Linux 下均可直接运行。

### 配置说明

#### 后端（work/.env）

配置从环境变量读取，`work/.env` 在应用启动时自动加载。

| 变量                 | 必填 | 说明                             | 默认/示例     |
| -------------------- | ---- | -------------------------------- | ------------- |
| `DB_USERNAME`        | 是   | 数据库用户名                     | test1         |
| `DB_PASSWORD`        | 是   | 数据库密码                       | —             |
| `DB_HOST`            | 是   | 主机:端口                        | localhost:3306 |
| `DB_NAME`            | 是   | 数据库名                         | book_system   |
| `JWT_SECRET_KEY`     | 是   | JWT 签名密钥（生产请用随机长串） | —             |
| `JWT_EXPIRATION_DAYS`| 否   | Token 有效天数                   | 1             |
| `FLASK_HOST`         | 否   | 监听地址                         | 127.0.0.1     |
| `FLASK_PORT`         | 否   | 监听端口                         | 8088          |
| `FLASK_DEBUG`        | 否   | 是否调试模式（1/0 或 true/false）| 1             |
| `FLASK_ENV`          | 否   | 环境名                           | development   |
| `CORS_ORIGINS`       | 否   | 允许的前端来源（多个逗号分隔；`*` 表示全部） | * |

复制 `work/.env.example` 为 `work/.env` 后按需修改。使用 `docker.sh` 时，账号、库名需与脚本内一致。

#### 前端 API 地址

- **开发**：`system/*/` 下 `.env.development` 中 `VUE_APP_API_BASE_URL`（已默认 `http://127.0.0.1:8088`）。
- **生产**：构建前设置 `VUE_APP_API_BASE_URL` 为实际后端地址，再执行 `npm run build`。

## 许可证

本项目为课程作业，仅供学习与展示。
