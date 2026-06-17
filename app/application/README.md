# application · UseCase 编排层

`app/application/` 用于放置跨 service、跨资源或多步骤业务流程的 UseCase。

它不是 `services/` 的子层，而是 API 与领域 service 之间的编排层：

```text
API / Router
    ↓
Application / UseCase
    ↓
Service
    ↓
Repository
    ↓
Model / Infrastructure
```

## 什么时候放在这里

- 需要 2 个以上 service 协作。
- 需要明确事务边界、补偿、幂等或状态流转。
- 需要同时调用 DB、Redis、外部 HTTP 或未来内部 service。
- 需要发布领域事件、Redis Stream 消息或协调后台任务。
- 需要把一个完整业务动作组织成可测试、可复用的流程。

## 什么时候不要放在这里

- 单个 service 能完成的简单业务，继续保持 `API -> Service -> Repository`。
- 纯领域规则放在对应 service 或领域 helper，不放在 UseCase。
- SQLAlchemy 查询放在 repository，不放在 UseCase。
- HTTP 请求解析、Response/Cookie 处理放在 API 层，不放在 UseCase。

## 组织方式

按业务域创建子目录，UseCase 文件使用动词或业务动作命名：

```text
app/application/
├── auth/
│   └── login_usecase.py
├── api_key/
│   └── create_api_key_usecase.py
└── README.md
```

UseCase 类名建议使用 `<Business>UseCase`，方法名使用动词开头，表达完整业务动作，例如：

```python
class LoginUseCase:
    async def login_with_password(self, command: LoginCommand) -> LoginResult:
        ...
```

UseCase 只负责编排流程；具体校验、状态判断和领域规则仍由对应 service 承担。
