# -*- coding: utf-8 -*-
"""
3. 理解 APIRoute —— 可运行演示脚本
==================================

核心认知：

    一个 Python 函数，是怎么变成一个能处理 HTTP 请求的 Route 的？

    中间不是简单的 URL -> function，而是：

        URL -> Route -> 依赖解析 -> 参数解析 -> Pydantic 验证
            -> 调用 endpoint -> 序列化 -> Response

    重点看 fastapi/routing.py 里的 APIRoute。

运行：python "3. 理解 APIRoute.py"
"""
import sys
import inspect
from fastapi import FastAPI
from fastapi.routing import APIRoute

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


@app.get("/users/{user_id}")
async def get_user(user_id: int, name: str = "Tom"):
    return {"user_id": user_id, "name": name}


# 找到我刚注册的那个路由（跳过文档路由）
my_routes = [r for r in app.routes if getattr(r, "path", "").startswith("/users")]
route = my_routes[0]

# 1. 这个 route 是什么
section("1. 这个 route 是什么")

print("类型：", type(route).__name__)
print("是 APIRoute？", isinstance(route, APIRoute))
print()
print("APIRoute 源码文件：", inspect.getsourcefile(APIRoute))
print("  （就是 fastapi/routing.py）")

# 2. APIRoute 的关键属性
section("2. APIRoute 的关键属性")

print("path：    ", route.path)
print("methods： ", route.methods)
print("endpoint：", route.endpoint.__name__)
print("dependant：", type(route.dependant).__name__)
print()
print("dependant（依赖/参数）里解析出的参数：")
path_params = getattr(route.dependant, "path_params", [])
query_params = getattr(route.dependant, "query_params", [])
print("  路径参数：", [p.name for p in path_params])
print("  查询参数：", [p.name for p in query_params])
print()
print("看到没：user_id 是路径参数，name 是查询参数——")
print("APIRoute 在注册时就『解析』了函数签名，知道每个参数从哪来。")

# 3. 一个函数变成 Route 的完整过程
section("3. 函数 -> Route 的完整过程")

print("URL")
print("  ↓")
print("Route（APIRoute）")
print("  ↓")
print("依赖解析")
print("  ↓")
print("参数解析（从 path/query/body 拿参数）")
print("  ↓")
print("Pydantic 验证")
print("  ↓")
print("调用 endpoint")
print("  ↓")
print("序列化")
print("  ↓")
print("Response")
print()
print("这就是 FastAPI 真正有意思的地方：")
print("一个普通函数，被 APIRoute 包装后，就获得了完整的 HTTP 处理能力。")

section("小结")
print("1. @app.get 注册的是 APIRoute（fastapi/routing.py）。")
print("2. APIRoute 有 path/methods/endpoint/dependant 等属性。")
print("3. 注册时解析函数签名，知道每个参数从哪来。")
print("4. 请求处理 = 依赖解析 -> 参数解析 -> 验证 -> 调 endpoint -> 序列化。")
