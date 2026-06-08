# 认证与 API 文档

## 目标

补齐认证相关设计文档和 API 契约文档，让后续接口改动有明确维护位置。

## 进度

| 任务 | 状态 |
| --- | --- |
| `docs/product/02-认证与用户.md` | ✅ |
| `docs/api/01-认证.md` | ✅ |
| `docs/api/02-公共.md` | ✅ |
| `docs/api/03-WebSocket.md` | ✅ |
| API 文档迁入 `docs/api/` | ✅ |
| 钱包 nonce Redis 化 | ⬜ |
| 统一认证错误响应 | ⬜ |
| API Key 边界清理 | ⬜ |

## 关键事实

- 浏览器优先使用 HttpOnly Cookie。
- 非浏览器可使用 Bearer 或 API Key。
- API Secret 只在创建时返回一次。
- TOTP secret 加密存储。
- 钱包登录当前需要补 nonce 服务端存储和一次性消费。

## 验证

本阶段主要是文档库建设。后续认证改动需要补测试并运行：

```text
make format
make lint
make test
```
