# 图书管理系统 · 数据库技术

[English](README.md) | **中文**

> 2022 年秋季「数据库技术」课程大作业，成绩 99。项目基于 Microsoft SQL Server 和 Python 命令行端，重点展示数据库建模、约束、触发器、存储过程、视图、索引、备份与恢复。

## 目录

- [功能](#功能)
- [技术栈](#技术栈)
- [目录结构](#目录结构)
- [快速开始](#快速开始)
- [运行说明](#运行说明)
- [数据库设计要点](#数据库设计要点)
- [备份与恢复](#备份与恢复)
- [说明](#说明)

## 功能

- **管理员** —— 图书管理、读者管理、借阅管理、管理员管理、备份恢复和重要操作审计。
- **读者** —— 图书检索、当前借阅、历史借阅、充值扣款记录和密码修改。
- **数据库** —— 主外键、CHECK 约束、唯一约束、触发器、视图、存储过程和非聚集索引。

## 技术栈

| 层次 | 技术 |
| --- | --- |
| 数据库 | Microsoft SQL Server / Azure SQL Edge |
| SQL | T-SQL、触发器、存储过程、视图、索引 |
| 应用层 | Python 3.8+、pymssql、pandas |
| 工具 | uv、Docker |

## 目录结构

```text
database-technology/
├── README.md             # English（默认）
├── README.zh-CN.md       # 中文
├── start-sql-edge.sh     # 启动 Azure SQL Edge 容器
├── init.py               # 初始化数据库、对象和示例数据
├── main.py               # 命令行交互端
├── schema.sql            # 完整 T-SQL 脚本
├── pyproject.toml
├── requirements.txt
└── uv.lock
```

## 快速开始

```bash
cd database-technology
./start-sql-edge.sh
uv sync
uv run python init.py
uv run python main.py
```

初始化后默认管理员账号为 `admin`，密码为 `admin`。

## 运行说明

1. `start-sql-edge.sh` 会启动本地 Azure SQL Edge 容器：

   | 项 | 值 |
   | --- | --- |
   | 容器名 | sqledge |
   | 地址 | localhost:1433 |
   | 用户 | sa |
   | 密码 | 脚本中的 `SA_PASSWORD` |

2. `init.py` 会创建 `BOOKS` 数据库、表、约束、索引、触发器、视图、存储过程和示例数据。重复执行会重建数据库，适合演示和测试。

3. `main.py` 启动命令行界面。Windows 下支持 `keyboard` 翻页；macOS 下使用回车、`n`、`q` 翻页，避免系统权限问题。

如果不使用 Docker，可以自行安装 SQL Server，并在 SSMS/Azure Data Studio 中执行 `schema.sql`。

## 数据库设计要点

| 对象 | 说明 |
| --- | --- |
| 表 | 图书分类、图书信息、读者信息、借阅信息、历史借阅信息、管理员信息、充值扣款记录、管理员重要操作记录、备份恢复记录 |
| 约束 | ISBN 长度、读者编号长度、读者类型、余额非负、图书状态枚举、管理员账号唯一 |
| 触发器 | 自动生成借阅权限、校验借阅数量上限、填充应还日期、逾期扣款、保护历史借阅和审计记录 |
| 视图 | 当前借阅数量、总借阅量 TOP10 等统计视图 |
| 存储过程 | 图书上下架、借还书、读者与管理员增删改查、密码重置、充值、备份恢复 |
| 索引 | ISBN、借阅关联字段、历史借阅关联字段、充值扣款读者字段 |

原作业要求包含 E-R 图，但该文件已丢失。本仓库保留了实现后的 SQL、命令行端和运行说明。

## 备份与恢复

管理员菜单中包含备份和恢复功能。默认路径写在 `main.py` 的 `Backup()` / `Restore()` 中，不同机器上运行前需要改成可写、可读的本机路径。

## 说明

本项目为课程作业，仅供学习与展示。脚本默认使用本地开发数据库，生产环境或共享环境请先调整密码、备份路径和连接信息。
