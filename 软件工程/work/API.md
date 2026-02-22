# 图书管理系统 · 后端 API 说明

后端基地址默认：`http://127.0.0.1:8080`。除登录/注册及部分查询外，需在请求头携带 JWT：`Authorization: Bearer <token>`。

统一响应格式：`{ "code": 200|400, "message": "...", ... }`，业务数据在对应字段中。

---

## 认证

| 方法 | 路径 | 说明 | 请求体/参数 | 响应 |
|------|------|------|-------------|------|
| POST | `/api/user/login` | 登录（读者或管理员，`user_id` 即读者编号或管理员账号） | `user_id`, `password` | `token` |
| POST | `/api/user/register` | 读者注册 | 用户信息字段 | — |
| POST | `/api/user/getInfo` | 获取当前用户信息（JWT） | 可选 `user_id`（管理员必填） | 用户信息 |

---

## 用户（读者）

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | `/api/user/update` | 更新个人信息 | JWT |
| POST | `/api/user/update_password` | 修改密码 | JWT |

---

## 图书

| 方法 | 路径 | 说明 | 参数/请求体 |
|------|------|------|-------------|
| GET | `/api/book/category` | 所有图书分类 | — |
| GET | `/api/book/page` | 分页模糊查询 | `keyword`, `page`, `pageSize` |
| GET | `/api/book/getById` | 按 ID 查单本 | query `book_id`（必填） |
| GET | `/api/book/top` | 借阅排行（可选 query `n`） | — |
| POST | `/api/book/add` | 添加图书 | 管理员，body: 分类/ISBN/书名/作者等 |
| PUT | `/api/book/update` | 更新图书 | 管理员，body: 含 `book_id` 等 |
| DELETE | `/api/book/delete` | 下架图书（改状态为下架，body: `book_id`） | 管理员 |

---

## 借阅

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | `/api/borrow/count` | 当前在借数量（可选 `user_id`，管理员可查指定读者） | 读者/管理员 |
| POST | `/api/borrow/borrow` | 借书（参数：`book_id`, `user_id`） | 管理员 |
| POST | `/api/borrow/renew` | 续借（参数：`book_id`，可选 `days`） | 管理员 |
| POST | `/api/borrow/return` | 还书（参数：`book_id`） | 管理员 |
| GET | `/api/borrow/page` | 当前借阅分页（可选 `user_id`, `keyword`, `page`, `pageSize`） | 读者/管理员 |
| GET | `/api/borrow/HistoricalPage` | 历史借阅分页（可选 `user_id`, `keyword`, `page`, `pageSize`） | 读者/管理员 |
| GET | `/api/borrow/expire` | 临期图书（可选 `due_days`, `user_id`, `page`, `pageSize`） | 读者/管理员 |

---

## 充值

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | `/api/recharge/page` | 充值/扣款记录分页（可选 `user_id`，管理员可查全部或指定读者） | 读者/管理员 |
| POST | `/api/recharge/add` | 充值/扣款（body: `user_id`, `value`，可选 `reason`） | 管理员 |

---

## 管理员

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/admin/user_page` | 读者分页查询 |
| DELETE | `/api/admin/user_delete` | 删除读者 |
| POST | `/api/admin/admin_add` | 添加管理员 |
| DELETE | `/api/admin/admin_delete` | 删除管理员 |
| GET | `/api/admin/admin_page` | 管理员列表分页 |
| POST | `/api/admin/admin_update` | 更新管理员 |
| POST | `/api/admin/password_update` | 修改管理员密码 |

---

## 操作记录

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | `/api/operation/admin_record` | 管理员重要操作记录 | 管理员 |
| GET | `/api/operation/user_record` | 用户相关操作记录（读者查自己，管理员可选 `user_id` 查指定读者或全部） | 读者/管理员 |

---

详细请求体字段以各接口实际代码为准；错误时 `code=400`，`message` 为错误说明。
