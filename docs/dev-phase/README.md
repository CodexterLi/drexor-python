# dev-phase · 开发进度

> 本目录记录 drexor-python 的开发进度：做了什么、做到哪、如何验证、还差什么。
> 产品文档看 `../product/`，系统架构看 `../architecture/`，API 文档看 `../api/`。

## 与 docs/ 的分工

- `docs/product/`：产品 / 功能文档，回答“用户能做什么”。
- `docs/architecture/`：系统架构文档，回答“系统怎么组织”。
- `docs/api/`：API 文档，回答“接口怎么调用”。
- `docs/dev-phase/`：开发进度文档，回答“做了什么，还差什么”。

开发时：

1. 先看 `docs/product/` 对齐产品功能。
2. 再看 `docs/architecture/` 对齐系统边界。
3. 完成代码后回填进度和验证结果。
4. 同步更新受影响的 `docs/product/`、`docs/architecture/` 和 `docs/api/`。

## 命名约定

```text
docs/dev-phase/
  README.md
  00-路线图.md
  01-基础设施与架构整理.md
  02-认证与API文档.md
  03-多服务演进.md
```

## 进度符号

| 符号 | 含义 |
| --- | --- |
| ✅ | 已完成且已验证 |
| 🔄 | 进行中 |
| ⬜ | 待办 |
| ⚠️ | 有风险或待确认 |
