# -*- coding: utf-8 -*-
"""
8. FastAPI 异步机制与完整链路 —— 可运行讲解脚本
================================================

核心认知：

    你的目标不是「我会用 asyncio」，而是：
    「我知道 FastAPI 为什么可以同时处理大量请求。」

    完整后端链路：

        浏览器 -> HTTP -> Uvicorn -> Event Loop -> FastAPI
               -> async def -> await -> 异步数据库驱动 -> PostgreSQL

    本脚本用 asyncio 模拟「一个事件循环并发处理大量请求」，
    让你直观看到 FastAPI 背后的机制。

运行：python "8. FastAPI 异步机制与完整链路.py"
"""
import sys
import time
import asyncio

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. 完整链路
section("1. 完整后端链路")

print("浏览器")
print("  ↓")
print("HTTP")
print("  ↓")
print("Uvicorn（ASGI 服务器，驱动事件循环）")
print("  ↓")
print("Event Loop")
print("  ↓")
print("FastAPI")
print("  ↓")
print("async def（你的路由处理函数）")
print("  ↓")
print("await")
print("  ↓")
print("异步数据库驱动（asyncpg 等）")
print("  ↓")
print("PostgreSQL")

# 2. 模拟：一个事件循环并发处理大量请求
section("2. 模拟：一个事件循环并发处理 5 个请求")


async def handle_request(name):
    # 这就是 FastAPI 里 async def 路由函数的简化版
    print(f"  [收到] 请求 {name}")
    await asyncio.sleep(0.1)   # 模拟 await 异步数据库查询
    print(f"  [返回] 响应 {name}")


async def server():
    t0 = time.perf_counter()
    await asyncio.gather(*(handle_request(f"req{i}") for i in range(5)))
    print(f"  （5 个请求并发处理，总耗时 {time.perf_counter() - t0:.2f} 秒）")


asyncio.run(server())
print()
print("如果同步串行处理，5 个各等 0.1 秒的请求要 0.5 秒；")
print("异步并发只要约 0.1 秒——这就是 FastAPI 高并发的秘密。")

# 3. async def 路由
section("3. FastAPI 里的 async def 路由")


print("FastAPI 代码：")
print()
print("  @app.get('/users')")
print("  async def get_users():")
print("      rows = await db.fetch('SELECT * FROM users')")
print("      return rows")
print()
print("关键：路由函数是 async def，里面的数据库查询用 await。")
print("这样等待数据库时，事件循环能去处理别的请求。")
print()
print("如果写的是普通 def 路由，FastAPI 会丢到线程池里跑；")
print("async def + await 才是真正的异步并发。")

# 4. 从「会调用」到「理解为什么」
section("4. 从『会调用库』到『理解为什么这样设计』")

print("搞懂这一层后，你之前用的 FastAPI、LangChain、异步 API 调用，")
print("都会从『会调用库』变成『理解它为什么这样设计』：")
print("  * 为什么路由要 async def？        -> 让事件循环能调度")
print("  * 为什么数据库驱动要 asyncpg？     -> await 时不阻塞事件循环")
print("  * 为什么 Uvicorn 能扛大量连接？    -> 单线程事件循环 + I/O 并发")
print("  * 为什么不能用 time.sleep？        -> 它会阻塞整个事件循环！")

section("小结")
print("1. FastAPI 高并发的秘密：事件循环 + async/await + 异步驱动。")
print("2. 链路：Uvicorn -> Event Loop -> FastAPI -> async def -> await -> 异步DB。")
print("3. async def 路由 + await 异步驱动，才能真正并发。")
print("4. 理解这一层，你就从『会用』升级到『懂原理』。")
