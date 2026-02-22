# 图书管理系统 · 软件工程课程项目

**软件工程 · 课程项目** | 2023 年秋 · **辅修**项目 · **课程成绩 92 分**

2023 年秋季学期「软件工程」课程的辅修项目。前后端分离的图书借阅管理系统：**Flask 后端 API** + **Vue 2 双前端**（读者端 / 管理端），使用 MySQL 数据库。

---

## 项目概述

| 项目属性   | 说明                     |
| ---------- | ------------------------ |
| 课程       | 软件工程                 |
| 学期与性质 | 2023 年秋 · 辅修项目     |
| 课程成绩   | 92 分                    |
| 数据库     | MySQL                    |
| 应用层     | Flask 后端 + Vue 2 双前端 |

---

## 技术栈

| 层次     | 技术                                   |
| -------- | -------------------------------------- |
| 数据库   | MySQL 5.7+（或 MariaDB、云数据库）     |
| 后端     | Python 3.7+、Flask、SQLAlchemy、JWT    |
| 前端     | Vue 2、Node.js 14+、npm               |

---

## 项目结构

```
软件工程/
├── README.md                    # 本文件
├── work/                        # 后端（Flask）
│   ├── run.py                   # 启动入口
│   ├── requirements.txt        # Python 依赖
│   ├── .env.example             # 环境变量示例（复制为 .env 后填写）
│   ├── API.md                   # 后端接口说明（路由、鉴权、请求/响应）
│   └── app/
│       ├── config.py            # 配置（从环境变量读取）
│       ├── models/              # 数据模型
│       ├── controllers/         # 业务逻辑
│       └── views/               # API 路由
└── system/
    ├── book-management-system   # 前端：读者端（借阅、充值、个人记录等），端口 8081
    └── book-manager-system      # 前端：管理端（图书/读者/借阅/管理员管理、操作记录等），端口 8083
```

---

## 功能概览

- **读者端**：登录、图书检索、当前/历史借阅、充值记录、重要操作查看、修改密码等。
- **管理端**：图书与分类、读者、借阅（借书/续借/还书）、管理员管理，重要操作记录，借阅排行等。
- **后端**：RESTful API，JWT 鉴权，MySQL + SQLAlchemy，CORS 支持前后端分离。

接口文档：后端路由、方法、鉴权及主要请求/响应说明见 `work/API.md`。

---

## 环境与运行

### 环境要求

- **Python** 3.7+（后端）
- **Node.js** 14+、npm（前端）
- **MySQL** 5.7+ 或兼容（如 MariaDB、云数据库）

### 快速开始

#### 1. 数据库

创建数据库（如 `book_system`），并保证本机或远程可连接。

#### 2. 后端

**前提**：先创建好 MySQL 数据库，并配置 `work/.env`（见下方配置说明）。未配置或数据库不可连接时，启动会在 `db.create_all()` 处报错。

```bash
cd work
python -m venv venv          # 可选：虚拟环境
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env         # 复制后编辑 .env，填写数据库与 JWT 配置
python run.py                # 默认 http://127.0.0.1:8080
```

首次运行会执行 `db.create_all()` 建表（无迁移时）。若使用 Flask-Migrate，可先执行 `flask db upgrade`。

#### 3. 前端（读者端）

```bash
cd system/book-management-system
npm install
npm run serve    # 开发：http://localhost:8081，API 默认请求 http://127.0.0.1:8080
```

#### 4. 前端（管理端）

```bash
cd system/book-manager-system
npm install
npm run serve    # 开发：http://localhost:8083，API 默认请求 http://127.0.0.1:8080
```

本地开发时，两个前端的 `request.js` 会优先使用 `.env.development` 中的 `VUE_APP_API_BASE_URL`（默认 `http://127.0.0.1:8080`），无需改代码。`npm run serve` / `npm run build` 已使用 `cross-env`，Windows / macOS / Linux 下均可直接运行。

### 配置说明

#### 后端（work/.env）

配置统一从环境变量读取，`work/.env` 会在应用启动时自动加载（与当前工作目录无关）。

| 变量                 | 必填 | 说明                             | 默认/示例     |
| -------------------- | ---- | -------------------------------- | ------------- |
| `DB_USERNAME`         | 是 | 数据库用户名                     | test1         |
| `DB_PASSWORD`         | 是 | 数据库密码                       | —             |
| `DB_HOST`             | 是 | 主机:端口                        | localhost:3306 |
| `DB_NAME`             | 是 | 数据库名                         | book_system   |
| `JWT_SECRET_KEY`      | 是 | JWT 签名密钥（生产请用随机长串） | —             |
| `JWT_EXPIRATION_DAYS` | 否 | Token 有效天数                   | 1             |
| `FLASK_HOST`          | 否 | 监听地址                         | 127.0.0.1     |
| `FLASK_PORT`          | 否 | 监听端口                         | 8080          |
| `FLASK_DEBUG`         | 否 | 是否调试模式（1/0 或 true/false）| 1             |
| `FLASK_ENV`           | 否 | 环境名                           | development   |
| `CORS_ORIGINS`        | 否 | 允许的前端来源（多个逗号分隔；`*` 表示全部） | * |

复制 `work/.env.example` 为 `work/.env` 后按需修改即可。

#### 前端 API 地址

- **开发**：`system/*/` 下 `.env.development` 中 `VUE_APP_API_BASE_URL`（已默认 `http://127.0.0.1:8080`）。
- **生产**：构建前设置 `VUE_APP_API_BASE_URL` 为实际后端地址，再执行 `npm run build`。

---

## 许可证

本项目为课程作业，仅供学习与展示。
