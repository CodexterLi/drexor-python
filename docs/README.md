# docs · 文档库

> drexor-python 的统一文档入口。文档路径使用英文，正文使用中文。

文档保持精简、可读。不同类型文档放在不同分区，不要互相混杂。

## 分区

| 分区 | 职责 |
| --- | --- |
| [product](./product/README.md) | 产品 / 功能文档：用户能做什么、功能规则是什么 |
| [architecture](./architecture/README.md) | 系统架构文档：系统怎么组织、边界在哪里 |
| [api](./api/README.md) | API 文档：接口怎么调用、请求响应是什么 |
| [plan](./plan/README.md) | 计划 / 设计草图：未实现能力、待确认方案和 TODO |
| [dev-phase](./dev-phase/README.md) | 开发进度文档：做了什么、还差什么、如何验证 |

## 维护规则

- 改接口：同步 `docs/api/`。
- 改功能规则：同步 `docs/product/`。
- 改代码分层、服务边界、部署/运行方式：同步 `docs/architecture/`。
- 完成阶段任务或留下待办：同步 `docs/dev-phase/`。
- 未实现设计、备选方案和 TODO 先进入 `docs/plan/`，落地后再回填 `docs/product/` 和 `docs/api/`。
- 文档以清晰可读为主，避免把代码实现细节完整搬进文档。
