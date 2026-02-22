# 书阁 · 图书管理系统

**book-management-system** — 图书馆与图书借阅管理（课程项目合集）

本仓库包含两个彼此独立的课程项目，技术栈与运行方式不同，详见下表。

---

## 项目一览

| 项目           | 课程       | 学期与性质     | 技术栈                         | 成绩   |
| -------------- | ---------- | -------------- | ------------------------------ | ------ |
| [数据库技术](数据库技术/) | 数据库技术 | 2022 年秋 · 主修 | SQL Server + Python 命令行     | 99 分  |
| [软件工程](软件工程/)   | 软件工程   | 2023 年秋 · 辅修 | Flask + Vue 2 双前端 + MySQL   | 92 分  |

---

## 演示视频 (Demo)

<table>
  <tr>
    <td><strong>数据库技术</strong><br><video src="数据库技术_Demo.mp4" controls width="100%"></video></td>
    <td><strong>软件工程</strong><br><video src="软件工程_Demo.mp4" controls width="100%"></video></td>
  </tr>
</table>

---

## 仓库结构

```
图书管理系统/
├── README.md           # 本文件
├── 数据库技术/         # 命令行端，SQL Server
│   ├── README.md
│   ├── main.py         # 入口
│   ├── init.py         # 数据库初始化（Python）
│   └── schema.sql      # T-SQL 建库脚本（推荐）
└── 软件工程/           # 前后端分离，MySQL
    ├── README.md
    ├── work/           # Flask 后端（端口 8080）
    └── system/         # Vue 2 双前端（读者端 8081、管理端 8083）
```

---

## 数据库技术

基于 **SQL Server** 与 **Python** 的图书借阅系统，命令行端，涵盖建库、约束、触发器、存储过程、视图、索引及备份恢复等。

**运行**：进入 `数据库技术/`，使用 **schema.sql**（在 SSMS 中执行）或 **init.py**（`python init.py`）建库并初始化后，运行 `python main.py`，默认 **admin / admin** 登录。详见 [数据库技术/README.md](数据库技术/README.md)。

---

## 软件工程

前后端分离：**Flask** 后端（RESTful、JWT）+ **Vue 2** 双前端（读者端 / 管理端），**MySQL** 数据库。

**运行**：配置 MySQL 与 `work/.env` 后，在 `软件工程/work/` 下执行 `python run.py`（默认 8080），再在 `system/book-management-system`、`system/book-manager-system` 下分别执行 `npm run serve`（读者端 8081、管理端 8083）。详见 [软件工程/README.md](软件工程/README.md)。

---

## 说明与许可证

环境与运行方式以各自子目录下的 README 为准。本项目为课程作业合集，仅供学习与展示。
