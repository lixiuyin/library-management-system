# 书阁 · 图书管理系统

[English](README.en.md) | **中文**

> 本仓库整理了两个独立的图书管理系统课程项目，用于课程归档、学习与作品集展示。两个项目面向同一业务主题，但技术栈、运行方式和课程侧重点不同。

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![Vue 2](https://img.shields.io/badge/Vue%202-4FC08D?logo=vuedotjs&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?logo=microsoftsqlserver&logoColor=white)

## 目录

- [项目一览](#项目一览)
- [演示视频](#演示视频)
- [目录结构](#目录结构)
- [快速运行](#快速运行)
- [说明](#说明)

## 项目一览

| 项目 | 课程 | 学期与性质 | 技术栈 | 成绩 |
| --- | --- | --- | --- | --- |
| [数据库技术](database-technology/) | 数据库技术 | 2022 年秋 · 主修 | SQL Server + Python CLI | 99 |
| [软件工程](software-engineering/) | 软件工程 | 2023 年秋 · 辅修 | Flask + Vue 2 + MySQL | 92 |

## 演示视频

项目演示视频已发布到 YouTube：

[![Watch on YouTube](https://img.shields.io/badge/Watch%20on-YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@lixiuyin)

> GitHub README 会过滤 YouTube `<iframe>`，请点击缩略图到 YouTube 播放，可全屏观看高清版本。

| 数据库技术 | 软件工程 |
| :---: | :---: |
| [![数据库技术演示视频](https://img.youtube.com/vi/vDb9shPoo60/maxresdefault.jpg)](https://youtu.be/vDb9shPoo60) | [![软件工程演示视频](https://img.youtube.com/vi/IJ76RYxe_vM/maxresdefault.jpg)](https://youtu.be/IJ76RYxe_vM) |
| SQL Server + Python 命令行端，展示建库、初始化、业务操作和数据库对象实践 | Flask + Vue 2 + MySQL 前后端分离系统，展示读者端、管理端和核心借阅流程 |

## 目录结构

```text
library-management-system/
├── README.md              # English（默认）
├── README.zh-CN.md        # 中文
├── database-technology/   # SQL Server + Python 命令行项目
│   ├── README.md
│   ├── README.zh-CN.md
│   ├── start-sql-edge.sh
│   ├── init.py
│   ├── main.py
│   └── schema.sql
└── software-engineering/  # Flask + Vue 2 + MySQL 项目
    ├── README.md
    ├── README.zh-CN.md
    ├── backend/
    ├── frontend/
    │   ├── reader-app/
    │   └── admin-app/
    └── scripts/
        ├── start-all.sh
        └── start-mysql.sh
```

## 快速运行

**数据库技术项目**

```bash
cd database-technology
./start-sql-edge.sh
uv sync
uv run python init.py
uv run python main.py
```

**软件工程项目**

```bash
cd software-engineering
cp backend/.env.example backend/.env
./scripts/start-all.sh
```

更多环境变量、默认账号和分步运行方式见各子项目 README。

## 说明

本仓库用于课程作业归档、学习和作品集展示。数据库、依赖和启动脚本均以本地开发环境为目标，生产环境部署需要重新配置密钥、数据库账号和前端 API 地址。
