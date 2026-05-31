# 书阁 · 图书管理系统

中文 | [English](README.en.md)

本仓库整理了两个独立的图书管理系统课程项目。两个项目面向同一业务主题，但技术栈、运行方式和课程侧重点不同。

## 项目一览

| 项目 | 课程 | 学期与性质 | 技术栈 | 成绩 |
| --- | --- | --- | --- | --- |
| [数据库技术](database-technology/) | 数据库技术 | 2022 年秋 · 主修 | SQL Server + Python CLI | 99 |
| [软件工程](software-engineering/) | 软件工程 | 2023 年秋 · 辅修 | Flask + Vue 2 + MySQL | 92 |

## 演示视频

GitHub README 会过滤 YouTube `<iframe>`，所以下方使用可点击的 YouTube 视频封面；打开后可全屏播放高清版本。

| 数据库技术 | 软件工程 |
| --- | --- |
| [<img src="https://img.youtube.com/vi/vDb9shPoo60/hqdefault.jpg" width="420" alt="数据库技术演示视频">](https://www.youtube.com/watch?v=vDb9shPoo60)<br>[YouTube 播放](https://www.youtube.com/watch?v=vDb9shPoo60) | [<img src="https://img.youtube.com/vi/IJ76RYxe_vM/hqdefault.jpg" width="420" alt="软件工程演示视频">](https://www.youtube.com/watch?v=IJ76RYxe_vM)<br>[YouTube 播放](https://www.youtube.com/watch?v=IJ76RYxe_vM) |

## 目录结构

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
