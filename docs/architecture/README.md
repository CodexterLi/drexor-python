# architecture · 系统架构

> 本目录记录 drexor-python 的系统架构：代码分层、运行组件、服务边界和未来演进。
> 产品功能看 `../product/`，API 文档看 `../api/`，开发进度看 `../dev-phase/`。

## 一句话架构

drexor-python 当前是 **FastAPI 模块化单体**：主服务承载认证、数据库、Redis、队列、调度和 WebSocket；未来只有在出现明确隔离或独立部署需求时才拆独立 service。

## 运行视图

```text
Client / SDK
    │
    ▼
FastAPI app
    ├── Auth: JWT / Cookie / Wallet / TOTP / API Key
    ├── DB: PostgreSQL + SQLAlchemy async
    ├── Cache: Redis
    ├── Queue: Redis Streams
    ├── Scheduler: APScheduler
    └── Realtime: WebSocket
```

## 代码分层

```text
API / Router
    ↓
Application / UseCase   # 复杂流程才需要
    ↓
Service
    ↓
Repository
    ↓
Model / Infrastructure
```

当前简单业务保持：

```text
API -> Service -> Repository
```

出现以下情况再加 UseCase：

- 需要 2 个以上 service 协作
- 需要事务边界、补偿、幂等或状态流转
- 需要同时调用 DB、Redis、外部 HTTP 或未来内部 service
- 需要发布领域事件或 Redis Stream 消息

## 目录边界

| 目录 | 职责 |
| --- | --- |
| `app/` | 主 FastAPI backend |
| `packages/common/` | 纯共享工具，不放业务逻辑 |
| `contracts/` | 未来跨服务 schema / event / error code |
| `services/<name>/` | 未来独立部署服务 |
| `app/clients/` | 未来内部服务 HTTP client |

## 服务间通信

| 场景 | 方式 |
| --- | --- |
| 同步命令 / 查询 | HTTP REST + `httpx.AsyncClient` |
| 异步事件 / 副作用 | Redis Streams |
| 本地发现 | `.env` 中配置 URL |
| 容器 / K8s | service name / Service DNS |

当前不需要注册中心。

## 拆 service 的条件

只有满足以下条件之一才拆：

- 独立部署或独立扩缩容
- 独立数据库权限或安全边界
- 资金、链上操作、密钥等高风险隔离
- 长任务 worker 与 API 生命周期明显不同
- 拆分后能明显降低主 backend 复杂度

## 设计原则

- 简单业务保持直接，不提前套模式。
- 复杂跨 service 流程允许使用 Facade、Strategy、State Machine、Unit of Work、Domain Event、Saga 等模式。
- API 层不写 SQL，不串联多个 repository。
- Repository 不做 HTTP、Redis Streams、WebSocket 副作用。
- 配置、密钥、服务地址不硬编码，统一走 `Settings` + `.env`。
