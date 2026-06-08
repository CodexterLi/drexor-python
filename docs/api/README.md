# api · API 文档

> 本目录记录 drexor-python 的 HTTP / WebSocket 接口契约。
> 产品功能看 `../product/`，系统架构看 `../architecture/`，开发进度看 `../dev-phase/`。

维护约定：新增、修改或删除任何 API，都要同步更新本目录。API 改动未更新文档视为未完成。

## 通用约定

- Base URL：`http://localhost:8000`
- Content-Type：`application/json`
- 时间：ISO-8601
- 浏览器认证优先使用 HttpOnly Cookie。
- 非浏览器客户端可使用 Bearer Token 或 API Key。

## 认证方式

Cookie / Bearer：

```text
Authorization: Bearer <token>
```

API Key：

```text
X-Api-Key: <key>
X-Api-Secret: <secret>
```

## 响应格式

成功响应直接返回业务对象。

列表响应：

```json
{
  "items": [],
  "totalCount": 0
}
```

统一错误响应：

```json
{
  "error": {
    "code": 400,
    "message": "Bad Request"
  }
}
```

说明：当前部分路由仍使用 FastAPI `HTTPException` 默认格式：

```json
{ "detail": "..." }
```

后续重构时应逐步统一。

## 端点索引

| 方法 | 路径 | 说明 | 认证 |
| --- | --- | --- | --- |
| POST | `/api/auth/login` | 密码登录 | 否 |
| POST | `/api/auth/refresh` | 刷新 token | refresh cookie |
| POST | `/api/auth/logout` | 登出 | 是 |
| POST | `/api/auth/register` | 创建用户 | superuser |
| GET | `/api/auth/me` | 当前用户信息 | 是 |
| POST | `/api/auth/wallet/nonce` | 获取钱包 nonce | 否 |
| POST | `/api/auth/wallet/login` | 钱包登录 | 否 |
| POST | `/api/auth/totp/setup` | 设置 TOTP | 是 |
| POST | `/api/auth/totp/verify` | 验证并启用 TOTP | 是 |
| POST | `/api/auth/totp/disable` | 禁用 TOTP | 是 |
| POST | `/api/auth/api-keys` | 创建 API Key | 是 |
| GET | `/api/auth/api-keys` | 列出 API Key | 是 |
| PUT | `/api/auth/api-keys/{id}/revoke` | 吊销 API Key | 是 |
| DELETE | `/api/auth/api-keys/{id}` | 删除 API Key | 是 |
| GET | `/api/docs/health` | 健康检查 | 否 |
| GET | `/api/docs/info` | 服务信息 | 否 |
| WS | `/ws` | 基础 WebSocket | 否 |
| WS | `/ws/broadcast` | 广播 WebSocket | 否 |

详见：

- [01-认证](./01-认证.md)
- [02-公共](./02-公共.md)
- [03-WebSocket](./03-WebSocket.md)
