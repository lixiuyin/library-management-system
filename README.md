# 书阁 · 图书管理系统

**book-management-system** — 图书馆与图书借阅管理（课程项目合集）

本仓库包含两个彼此独立的课程项目，技术栈与运行方式不同。

## 项目一览

| 项目 | 课程 | 学期与性质 | 技术栈 | 成绩 |
| --- | --- | --- | --- | --- |
| [数据库技术](数据库技术/) | 数据库技术 | 2022 年秋 · 主修 | SQL Server + Python 命令行 | 99 分 |
| [软件工程](软件工程/) | 软件工程 | 2023 年秋 · 辅修 | Flask + Vue 2 双前端 + MySQL | 92 分 |

## 演示视频 (Demo)

| 数据库技术 | 软件工程 |
| --- | --- |
| [视频](https://github.com/user-attachments/assets/eaf44d76-58c6-49df-b970-8ff1cc900e78) | [视频](https://github.com/user-attachments/assets/b6597875-4284-4093-9ad5-6bc1be8a1e28) |

## 仓库结构

```
图书管理系统/
├── README.md           # 本文件
├── 数据库技术/         # 命令行端，SQL Server（Azure SQL Edge）
├── 软件工程/           # 前后端分离，MySQL
│   ├── work/           # Flask 后端（端口 8088）
│   ├── system/         # Vue 2 双前端（读者端 8081、管理端 8083）
│   ├── docker.sh       # MySQL 容器
│   └── start.sh        # 一键启动（MySQL → 后端 → 双前端）
```

## 项目说明

**数据库技术** — 基于 SQL Server 与 Python 的图书借阅系统，命令行端，涵盖建库、约束、触发器、存储过程、视图、索引及备份恢复等。  
**运行**：① `docker.sh` 启动数据库（Azure SQL Edge）；② `init.py` 初始化库表并执行部分测试（可用 `uv run python init.py`）；③ `main.py` 启动命令行界面进行交互（默认管理员 admin / admin）。推荐使用 uv 管理依赖：`uv sync` 后使用 `uv run python`。详见 [数据库技术/README.md](数据库技术/README.md)。

**软件工程** — 前后端分离：Flask 后端（RESTful、JWT）+ Vue 2 双前端（读者端 / 管理端），MySQL 数据库。  
**运行**：① `docker.sh` 启动 MySQL；② 在 `work/` 下执行 `uv run python run.py`（或 `python run.py`）启动后端；③ 在 `system/` 下两个前端目录分别 `npm run serve`。也可直接执行 **`start.sh`** 一键启动 MySQL、后端与双前端。后端推荐使用 uv：`cd work && uv sync`。详见 [软件工程/README.md](软件工程/README.md)。

环境与运行以各自子目录 README 为准。本项目为课程作业合集，仅供学习与展示。
