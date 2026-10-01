# -*- coding: utf-8 -*-
"""
2. app.get 路由注册 —— 可运行演示脚本
=====================================

核心认知：

    @app.get("/users") 不只是「装饰器」三个字，它真正做了：

        @app.get("/users")
            ↓
        app.get()
            ↓
        路由注册
            ↓
        APIRoute 对象
            ↓
        app.routes（路由表）

    关键实验：打印 app.routes，你会看到 /users、{'GET'}、endpoint 函数。

    从这一刻起，你从「会使用 FastAPI」进入「知道它怎么管理路由」。

运行：python "2. app.get 路由注册.py"
"""
import sys
from fastapi import FastAPI
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


app = FastAPI()


@app.get("/users")
async def get_users():
    return {"message": "hello"}


@app.post("/users")
async def create_user():
    return {"message": "created"}


# 1. 关键实验：打印 app.routes
section("1. 关键实验：@app.get 到底把什么放进了 app")

print("for route in app.routes: print(route)")
print()
for route in app.routes:
    print("  route 对象：", route)
    print("    类型：    ", type(route).__name__)
    print("    path：    ", getattr(route, "path", "?"))
    print("    methods： ", getattr(route, "methods", None))
    print("    endpoint：", getattr(route, "endpoint", None))
    print()

# 2. 看到 /users 和 endpoint
section("2. 你看到了什么")

print("你会看到：")
print("  /users  {'GET'}  <function get_users>")
print("  /users  {'POST'} <function create_user>")
print("  （还有 FastAPI 自动加的 /docs、/openapi.json 等文档路由）")
print()
print("说明 @app.get('/users') 把『路径 + 方法 + endpoint 函数』")
print("注册成 APIRoute，存进了 app.routes 这个路由表。")

# 3. 请求到来时，如何找到 route
section("3. 请求到来时：按路径匹配路由")


@app.get("/users")
async def get_users():
    return {"message": "hello"}


client = TestClient(app)
resp = client.get("/users")
print("TestClient 发 GET /users：")
print("  状态码：", resp.status_code)
print("  响应体：", resp.json())
print()
print("请求 -> 匹配 app.routes 里的 route -> 调用 route.endpoint -> 返回结果。")

section("小结")
print("1. @app.get 是装饰器，把函数注册成 APIRoute 存入 app.routes。")
print("2. app.routes 里有 path、methods、endpoint 三个关键字段。")
print("3. 请求来了 -> 匹配路由 -> 调用 endpoint。")
