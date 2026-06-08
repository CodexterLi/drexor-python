# WebSocket

## WS `/ws`

基础 WebSocket 连接。

连接成功后服务端发送：

```json
{
  "type": "welcome",
  "message": "欢迎连接 WebSocket 服务！",
  "connectionCount": 1
}
```

客户端 ping：

```json
{
  "type": "ping"
}
```

服务端响应：

```json
{
  "type": "pong"
}
```

客户端 message：

```json
{
  "type": "message",
  "content": "hello"
}
```

服务端响应：

```json
{
  "type": "echo",
  "content": "hello"
}
```

未知类型响应：

```json
{
  "type": "error",
  "message": "未知的消息类型: xxx"
}
```

## WS `/ws/broadcast`

广播频道。

连接成功后服务端发送 welcome，并向所有连接广播在线人数。

客户端发送：

```json
{
  "type": "message",
  "content": "hello everyone"
}
```

服务端向所有连接广播：

```json
{
  "type": "broadcast",
  "content": "hello everyone"
}
```

断开连接后服务端广播当前在线人数。
