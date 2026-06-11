# drexor-python

drexor-python 是 Drexor 的 Python 后端服务，提供用户认证 + 数据库 + Redis + WebSocket 基础设施。

纯基础设施核心后端（无 AI/Agent 运行时）。前端为独立仓库。

## 功能特性

- **用户认证**: 密码登录、钱包登录 (EVM)、JWT、HTTP-Only Cookie、TOTP 两步验证、API Key
- **数据库**: PostgreSQL 异步连接、SQLAlchemy ORM
- **缓存**: Redis 异步连接、Session 缓存、统一 Key 命名规范
- **定时任务**: APScheduler 异步调度
- **队列**: 基于 Redis Streams 的消费者框架（含重试 / DLQ）
- **WebSocket**: 基础连接、消息广播、心跳检测
- **其他**: Loguru 日志、统一异常处理、Google 风格 API 响应、CORS

## 快速开始

### 环境要求

- Python >= 3.14
- PostgreSQL
- Redis

### 安装与运行

```bash
# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入数据库 / Redis / 密钥等

# 初始化数据库
psql -U postgres -d drexor -f migrations/001_init.sql

# 运行服务
make dev

# 可选：运行后台 worker
# 默认不启用任何后台角色；按 .env 打开 SCHEDULER_ENABLED 或 QUEUE_WORKER_ENABLED 后再运行。
make worker
```

### Docker

API 和 worker 使用同一个镜像，不需要分别构建。区别只在启动命令：

```bash
# 构建镜像
make docker-build

# 运行 API
make docker-run-api

# 运行 worker
make docker-run-worker
```

也可以参考 [docker-compose.example.yml](./docker-compose.example.yml)，用同一个 `drexor-python:latest` 镜像启动 `api` 和 `worker` 两个容器。

### API 文档

- Swagger UI: http://localhost:8000/docs
- Scalar API Reference: http://localhost:8000/scalar
- ReDoc: http://localhost:8000/redoc
- 接口文档: [docs/api/README.md](./docs/api/README.md)
- 产品文档: [docs/README.md](./docs/README.md)
- 架构文档: [docs/architecture/README.md](./docs/architecture/README.md)
- 开发进度: [docs/dev-phase/README.md](./docs/dev-phase/README.md)

## 项目结构

```
app/
├── main.py                # API 应用入口
├── worker.py              # 后台 worker 入口（scheduler / queue）
├── config/                # 配置管理 (pydantic-settings)
├── core/                  # 核心模块 (异常、日志、安全、响应)
│   └── security/          # 密码、JWT、Cookie、TOTP、钱包验证、API Key
├── db/                    # 数据库连接 (PostgreSQL + Redis) + redis_keys 命名规范
├── models/                # ORM 模型 (User, ApiKey)
├── repositories/          # 数据访问层
├── schemas/               # 请求/响应 Schema
├── services/              # 业务逻辑层 (auth, api_key)
├── scheduler/             # APScheduler 定时任务
├── queue/                 # Redis Streams 消费者框架
├── api/                   # API 路由层 (auth / common / websocket)
└── utils/                 # 兼容工具入口
packages/
└── common/                # 未来多服务共享的纯基础设施工具
tests/                     # pytest 测试
```

## 文档库

| 目录 | 说明 |
| --- | --- |
| `docs/product/` | 产品 / 功能文档 |
| `docs/architecture/` | 系统架构文档 |
| `docs/api/` | API 文档 |
| `docs/dev-phase/` | 开发进度文档 |

修改代码时如果影响接口、配置、数据结构、服务边界或模块行为，需要同步更新对应文档。

## 主要 API

### Auth (`/api/auth`)

| Method | Path | 说明 |
|--------|------|------|
| POST | /api/auth/register | 注册 |
| POST | /api/auth/login | 密码登录 |
| POST | /api/auth/refresh | 刷新 token |
| POST | /api/auth/logout | 登出 |
| GET  | /api/auth/me | 当前用户 |
| POST | /api/auth/wallet/nonce | 获取钱包签名 nonce |
| POST | /api/auth/wallet/login | 钱包登录 |
| POST | /api/auth/totp/setup | TOTP 初始化 |
| POST | /api/auth/totp/verify | TOTP 校验 |
| POST | /api/auth/totp/disable | 关闭 TOTP |
| POST | /api/auth/api-keys | 创建 API Key |
| GET  | /api/auth/api-keys | 列出 API Key |
| PUT  | /api/auth/api-keys/{id}/revoke | 撤销 API Key |
| DELETE | /api/auth/api-keys/{id} | 删除 API Key |

### Common (`/api/docs`)

| Method | Path | 说明 |
|--------|------|------|
| GET | /api/docs/health | 健康检查 |
| GET | /api/docs/info | 服务信息 |

### WebSocket

| Path | 说明 |
|------|------|
| /ws | WebSocket 连接 |
| /ws/broadcast | 消息广播 |
