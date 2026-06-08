# AGENTS.md

本文件用于指导 Codex（Codex.ai/code）在本仓库中工作。

## 项目概览

drexor-python 是 Drexor 的 Python 后端服务，基于 FastAPI 构建，定位为 **基础设施核心后端**，包含 Web3 认证能力。

当前仓库提供：

- 用户认证：JWT、钱包登录、TOTP
- API Key 管理
- PostgreSQL + Redis 基础设施
- APScheduler 定时任务
- Redis Streams 队列框架
- WebSocket 实时通信

本仓库 **不包含 AI/Agent 运行时**。相关能力已在前后端拆分过程中移除；前端位于独立仓库。

技术栈：Python 3.14、FastAPI、SQLAlchemy 2.0 async、asyncpg、Redis、APScheduler、uv。

## 常用命令

| 命令 | 用途 |
| --- | --- |
| `make install` | 使用 `uv sync` 安装依赖 |
| `make dev` | 启动热重载开发服务（http://localhost:8000） |
| `make lint` | Ruff 检查 + 格式检查 |
| `make format` | Ruff 自动修复 + 格式化 |
| `make test` | 运行 pytest |
| `make upgrade` | 升级依赖 |

Lint 和格式化使用 `uvx ruff`，不是 `uv run ruff`；ruff 不是项目运行依赖。

## 架构

```text
Client ──▶ FastAPI (uvicorn :8000)
               ├── Auth (JWT / Wallet / TOTP / API Key)
               ├── Scheduler (APScheduler cron/interval jobs)
               ├── Queue (Redis Streams consumers)
               └── WebSocket (broadcast / personal)
```

当前主应用采用模块化单体架构：业务代码位于 `app/`，导入前缀为 `app.*`。

仓库已经预留轻量共享包：

- `packages/common`：跨未来服务复用的纯基础设施工具，例如 Snowflake ID、时间工具。
- 未来如需拆独立服务，可新增 `services/<service_name>`，并通过 HTTP/Redis Streams 通信。
- 跨服务契约可放在 `contracts/`，只放 schema、事件 payload、错误码和常量，不放业务逻辑。

## 目录结构

### 主应用：`app/`

- `main.py`：FastAPI 入口。生命周期中初始化/关闭 DB 与 Redis，注册 CORS 和异常处理器。
- `api/`：HTTP/WebSocket 路由。
  - `router.py`：主路由聚合入口。
  - `api.py`：兼容旧导入的 wrapper，保留 `api_router`。
  - `auth/`：登录、注册、钱包登录、TOTP、API Key、用户资料。
  - `websocket/`：WebSocket 路由和连接管理。
  - `common/`：健康检查、文档等公共路由。
- `config/`：基于 Pydantic Settings 的配置加载，读取根目录 `.env`。
- `core/`：横切基础能力。
  - `security/`：JWT、bcrypt、TOTP 加密、钱包签名验证、API Key 校验。
  - `responses.py`：Google JSON 风格响应。
  - `exceptions.py`：统一异常层级和异常处理器。
  - `logging.py`：Loguru 日志配置、标准库 logging 桥接、日志轮转。
- `db/`：数据库层。
  - `postgres.py`：异步 SQLAlchemy engine、session factory、`get_db()` 依赖。
  - `redis.py`：异步 Redis 客户端，支持连接池、SSL、ACL。
  - `redis_keys/`：Redis key 命名空间约定。
- `models/`：SQLAlchemy ORM 模型，例如 `User`、`ApiKey`。
- `repositories/`：数据库查询封装。
- `services/`：业务逻辑，例如 `AuthService`、`ApiKeyService`。
- `schemas/`：Pydantic 请求/响应模型。
- `scheduler/`：APScheduler 集成，`BaseJob` 支持 cron/interval trigger。
- `queue/`：Redis Streams 消费框架，支持 XREADGROUP、自动重试、死信队列。
- `utils/`：兼容层。新共享工具应优先放到 `packages/common`。

### 共享包：`packages/`

- `packages/common/snowflake.py`：Snowflake ID 生成器。
- `packages/common/time.py`：UTC 和 UTC+8 时间工具。

`packages/common` 只能放无 FastAPI、无数据库 session、无业务状态的纯工具。不要把业务 service、repository、model 放进去。

### 测试：`tests/`

测试目录统一使用 `tests/`，不要再新增 `test/`。

### 迁移：`migrations/`

当前使用 raw SQL migration 文件，例如 `001_init.sql`。

## 关键模式

- **异步优先**：数据库、Redis、HTTP 等 I/O 均使用 async。
- **依赖注入**：FastAPI `Depends()` 用于 DB session、认证和 service 注入。
- **分层边界**：API 层处理 HTTP；Service 层编排业务；Repository 层处理查询。
- **响应风格**：成功直接返回数据；错误返回 `{ "error": { "code", "message" } }`。
- **认证方式**：路由可通过 JWT cookie 或 API key header 获取当前用户。
- **用户隔离**：当前模型主要通过 `user_id` 进行数据归属。

## 代码风格

- Ruff 配置位于 `ruff.toml`，行宽 120。
- Python 运行版本为 3.14；Ruff `target-version` 固定为 `py313`，避免 PEP 649 相关误判影响 FastAPI 运行时注解。
- 启用规则：E、W、F、I、B、C4、UP、SIM、TCH、RUF。
- 忽略 `B008`，用于兼容 FastAPI `Depends()`。
- isort first-party 包含 `app` 和 `packages`。
- SQLAlchemy 模型中的 `Mapped[]` 需要运行时类型导入，`app/models/` 对 `TC003` 有例外。

## 编码约束

- 每次修改代码后必须运行 `make format` 和 `make lint`；通常先 `make format`，再 `make lint`。如果因为环境问题无法运行，需要在回复中明确说明原因。
- 涉及业务逻辑、接口行为、数据模型、队列、调度或安全认证的改动，必须运行 `make test`；如果测试覆盖不足，应补充针对性测试。
- 单个函数/方法尽量控制在 50 行以内。超过 50 行时，应优先拆分为私有 helper、service 方法或独立对象；只有在事务流程必须连续表达时才允许例外，并保持清晰注释。
- 单个模块不应混合多个层级职责。API 文件不要写数据库查询；repository 不要写 HTTP/Redis 副作用；schema 不要包含业务流程。
- API 层只负责参数解析、依赖注入和响应返回；业务规则放在 service；SQLAlchemy 查询放在 repository。
- 新增公共逻辑前先查现有实现，优先复用本仓库已有模式，不要引入重复工具函数。
- 不为了“未来可能需要”提前创建抽象。只有出现实际复用、边界隔离或复杂度下降时才抽象。
- 复杂业务涉及多个 service、外部系统、状态流转或多步骤事务时，可以引入合适的设计模式提升健壮性，例如 Facade、Strategy、Factory、State Machine、Unit of Work、Domain Event、Saga/Process Manager。
- 使用设计模式必须服务当前复杂度：需要能说明它解决了什么问题，例如隔离变化、减少分支、统一事务边界、降低耦合或提升可测试性。不要为了“看起来架构化”而套模式。
- 跨多个 service 的业务流程应有明确编排层；不要让 API 路由直接串联多个 repository 或外部调用。
- 不要在代码中硬编码环境相关配置、密钥、token、服务地址、数据库/Redis 地址、链 RPC、外部 API endpoint、管理员账号或业务可调参数；应放入 `app/config/settings.py` 并通过 `.env` 注入。
- 对固定协议值、错误码、Redis key 前缀、权限名等确实稳定的常量，应集中定义在对应模块，不要散落在业务流程中。
- 异步代码中不要调用阻塞 I/O；需要外部 HTTP 调用时使用 `httpx.AsyncClient`。
- 错误处理优先使用 `app.core.exceptions` 中的统一异常，不要在业务层随意返回裸 dict 表示错误。
- 日志不得包含密码、JWT、API secret、TOTP secret、私钥、完整 API key 等敏感信息。
- 代码风格要服务可读性：命名清晰、分支扁平、避免深层嵌套，优先早返回；不要为了压行数牺牲语义。

## 测试要求

- 测试统一放在 `tests/`，文件命名为 `test_*.py`。
- 对 service 和 repository 的核心分支补测试；API 行为变化至少覆盖成功路径和关键失败路径。
- 修复 bug 时，优先先补一个能复现问题的测试，再修复实现。
- 不要依赖测试执行顺序；涉及时间、ID、Redis、数据库的测试应显式隔离状态。

## 环境变量

`.env` 位于仓库根目录，参考 `.env.example`。

关键配置：

```text
SECRET_KEY      — JWT 签名密钥
DB_*            — PostgreSQL asyncpg 连接配置
REDIS_*         — Redis 连接配置
TOTP_*          — TOTP 加密配置
CORS_ORIGINS    — 允许的跨域来源
```

要求 Python 3.14+ 和 uv。

## 开发约定

- 新增共享工具时优先放入 `packages/common`，并视情况在 `app/utils` 保留兼容 wrapper。
- 新增测试放入 `tests/`。
- 不要把未来独立 service 的代码直接 import 到 `app` 中；服务间同步调用优先 HTTP，异步事件优先 Redis Streams。
- 不要使用共享数据库作为服务间通信方式；独立服务应有明确表权限和边界。
- 修改架构说明、命令、目录或服务边界时，同步更新 `AGENTS.md` 和 `CLAUDE.md`。
