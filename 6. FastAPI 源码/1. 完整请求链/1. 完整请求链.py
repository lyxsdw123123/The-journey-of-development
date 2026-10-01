# -*- coding: utf-8 -*-
"""
1. 完整请求链：FastAPI 不是 Web 服务器 —— 可运行演示脚本
========================================================

核心认知：

    FastAPI 本身不是 Web 服务器。执行 uvicorn main:app 时：

        Uvicorn（负责监听 HTTP，把请求转成 ASGI 调用）
            ↓
        FastAPI app（一个 ASGI 应用）

    完整请求链：

        客户端 -> HTTP -> Uvicorn -> ASGI -> FastAPI
               -> Middleware -> Router -> DI -> Endpoint
               -> Pydantic Validation -> Response -> ASGI -> 客户端

运行：python "1. 完整请求链.py"
"""
import sys
from fastapi import FastAPI

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. FastAPI 不是 Web 服务器
section("1. FastAPI 不是 Web 服务器")

app = FastAPI()
print("app = FastAPI() 的类型：", type(app).__name__)
print()
print("关键认知：FastAPI app 是「ASGI 应用」，不是 Web 服务器。")
print()
print("uvicorn main:app 实际上：")
print("  Uvicorn  -> 负责监听 HTTP 端口、解析请求")
print("             -> 把请求转换成 ASGI 调用")
print("  app      -> 你的 FastAPI 应用（ASGI 应用），处理请求")

# 2. 完整请求链
section("2. 完整请求链")

chain = [
    "客户端",
    "HTTP Request",
    "Uvicorn",
    "ASGI",
    "FastAPI",
    "Middleware",
    "Router",
    "Dependency Injection",
    "Endpoint",
    "Pydantic Validation",
    "Response",
    "ASGI",
    "客户端",
]
print("请求走过的每一站：")
for i, step in enumerate(chain, 1):
    arrow = "  ↓" if i < len(chain) else ""
    print(f"  {step}{arrow}")

# 3. ASGI 是什么
section("3. ASGI 接口")

print("ASGI 应用就是一个 callable，签名是：")
print("  async def app(scope, receive, send): ...")
print()
print("  scope    请求的元信息（类型、路径、headers 等）")
print("  receive  接收请求体的异步函数")
print("  send     发送响应的异步函数")
print()
print("FastAPI app 实现了这个接口，所以 Uvicorn 能调用它。")
print("这套『服务器 Uvicorn + 应用 FastAPI』通过 ASGI 解耦。")

# 4. 你之前学的完整技术链
section("4. 你之前学的技术链，串起来了")

print("Python")
print("  ↓")
print("asyncio（事件循环、并发）")
print("  ↓")
print("ASGI（异步服务器接口）")
print("  ↓")
print("FastAPI（Web 框架）")
print("  ↓")
print("PostgreSQL（数据持久化）")
print()
print("这其实是一条非常完整的后端技术链。")

section("小结")
print("1. FastAPI 是 ASGI 应用，不是 Web 服务器；Uvicorn 才是服务器。")
print("2. 请求链：客户端 -> Uvicorn -> ASGI -> FastAPI -> ... -> 客户端。")
print("3. ASGI = 服务器与应用之间的标准接口（scope/receive/send）。")
