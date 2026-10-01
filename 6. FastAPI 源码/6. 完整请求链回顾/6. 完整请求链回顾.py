# -*- coding: utf-8 -*-
"""
6. 完整请求链回顾 —— 可运行演示脚本（收尾综合）
================================================

核心认知：

    学完这一主题，你应该能不看源码，解释一次完整请求的每一站。

    本脚本用一个「综合路由」（Depends + Pydantic response_model）真实跑一次，
    把前面几节的机制串起来。

运行：python "6. 完整请求链回顾.py"
"""
import sys
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.testclient import TestClient

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


class User(BaseModel):
    name: str
    age: int


def get_db():
    return "数据库连接"


app = FastAPI()


@app.get("/users", response_model=User)
async def get_user(db=Depends(get_db)):
    return User(name="Tom", age=20)


# 1. 一个综合路由
section("1. 一个综合路由（Depends + response_model）")

print("这个路由同时用了：")
print("  * Depends(get_db)    依赖注入")
print("  * response_model=User  Pydantic 响应序列化")
print("  * 返回 User 对象       会被序列化成 JSON")

# 2. 真实跑一次完整请求
section("2. 真实跑一次完整请求")

client = TestClient(app)
resp = client.get("/users")
print("GET /users：")
print("  状态码：", resp.status_code)
print("  响应体：", resp.json())
print("  Content-Type：", resp.headers.get("content-type"))

# 3. 脑子里应该有的完整图景
section("3. 脑子里应该有的完整图景")

print("浏览器发送请求")
print("  ↓")
print("Uvicorn")
print("  ↓")
print("ASGI")
print("  ↓")
print("FastAPI")
print("  ↓")
print("Middleware")
print("  ↓")
print("Router（找到 APIRoute）")
print("  ↓")
print("解析 Depends（依赖图）")
print("  ↓")
print("解析请求参数")
print("  ↓")
print("Pydantic Validation")
print("  ↓")
print("调用 Endpoint")
print("  ↓")
print("Response Model")
print("  ↓")
print("Serialization")
print("  ↓")
print("ASGI Response")
print("  ↓")
print("客户端")

# 4. 最终状态
section("4. 你到达的状态")

print("看到 @app.get('/users', response_model=User) 时，")
print("你脑子里不再是『这是 FastAPI 的语法』，而是：")
print()
print("  『这里注册了一个 APIRoute，它有 endpoint、response model")
print("    和 dependency graph。请求进来后，FastAPI 会先解析依赖和参数，")
print("    验证完成后调用 endpoint，最后进行响应序列化。』")
print()
print("这就是从『会用框架』到『理解框架』的关键转折点。")

section("小结")
print("1. 一次请求 = 完整链路：Uvicorn -> ASGI -> FastAPI -> Router -> DI -> Endpoint -> 序列化。")
print("2. APIRoute 管路由，Depends 管依赖，Pydantic 管数据转换。")
print("3. 你能解释全链路，就是真正『理解』了 FastAPI。")
