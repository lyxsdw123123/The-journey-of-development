# -*- coding: utf-8 -*-
"""
4. Depends 依赖注入 —— 可运行演示脚本
====================================

核心认知：

    Depends(get_db) 表面上只是「调用一下 get_db」，
    但源码层面远不止这么简单：

        Depends()
          ↓
        Dependant（依赖对象）
          ↓
        依赖关系解析
          ↓
        solve_dependencies()
          ↓
        执行依赖
          ↓
        得到结果
          ↓
        注入 endpoint

    依赖可以嵌套（get_current_user 依赖 get_db），形成依赖图。

运行：python "4. Depends 依赖注入.py"
"""
import sys
from fastapi import FastAPI, Depends
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


# 1. 定义依赖
section("1. 定义两个依赖（含嵌套）")


def get_db():
    return {"db": "数据库连接"}


def get_current_user(db=Depends(get_db)):
    # 这个依赖又依赖 get_db —— 嵌套依赖
    return {"user": "Tom", **db}


app = FastAPI()


@app.get("/users")
async def get_users(user=Depends(get_current_user)):
    return user


print("get_db:          最底层依赖，返回数据库连接")
print("get_current_user: 依赖 get_db，返回当前用户")
print("get_users:       endpoint，依赖 get_current_user")

# 2. 实际请求：依赖被自动注入
section("2. 实际请求：依赖被自动解析并注入")

client = TestClient(app)
resp = client.get("/users")
print("GET /users 响应：", resp.json())
print()
print("注意：endpoint 参数 user 我们没传，是 FastAPI 自动注入的。")
print("它先执行 get_db，再执行 get_current_user（拿到 db），最后注入 endpoint。")

# 3. 依赖图
section("3. 依赖图")

print("Request")
print("  │")
print("  ↓")
print("Route（/users）")
print("  │")
print("  ↓")
print("Dependency Graph")
print("  │")
print("  ├── get_current_user()")
print("  │      └── get_db()")
print("  ↓")
print("Endpoint（get_users）")
print()
print("solve_dependencies() 会先按依赖图，从最底层(get_db)往上解析，")
print("把结果一层层注入。这就是 FastAPI 的依赖注入系统。")

# 4. Depends 不止于此
section("4. Depends 能做什么")

print("1. 复用逻辑：数据库连接、当前用户、权限校验。")
print("2. 嵌套依赖：get_current_user 依赖 get_db。")
print("3. 缓存：同一请求里，同一个依赖只执行一次。")
print("4. 覆盖：测试时用 app.dependency_overrides 替换依赖。")
print()
print("理解了 Depends，就真正理解了 FastAPI 的依赖注入系统。")

section("小结")
print("1. Depends(get_db) 表面是调用函数，实际是声明依赖关系。")
print("2. Dependant + solve_dependencies() 解析依赖图。")
print("3. 依赖可嵌套，从底层往上解析，结果注入 endpoint。")
print("4. 这是 FastAPI 最核心的机制之一。")
