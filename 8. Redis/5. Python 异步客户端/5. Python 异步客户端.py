# -*- coding: utf-8 -*-
"""
5. Python 异步客户端 —— 可运行演示脚本
======================================

核心认知：

    用 redis.asyncio.Redis，把 Redis 融入 FastAPI 的 async def 路由：

        from redis.asyncio import Redis
        redis = Redis(host="localhost", port=6379, decode_responses=True)

        @app.get("/users/{user_id}")
        async def get_user(user_id: int):
            cached = await redis.get(f"user:{user_id}")
            if cached:
                return cached
            user = 查数据库...
            await redis.set(f"user:{user_id}", user, ex=3600)
            return user

    这把前面学的串起来：asyncio -> FastAPI -> Redis -> PostgreSQL。

运行：python "5. Python 异步客户端.py"（需本机已启动 Redis）
"""
import sys
import asyncio
from redis.asyncio import Redis

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


async def main():
    r = Redis(host="127.0.0.1", port=6379, db=15, decode_responses=True, protocol=2)  # protocol=2 兼容老版 Redis
    await r.flushdb()

    # 1. 异步 get/set
    section("1. 异步 get / set")

    await r.set("user:1", "Tom", ex=3600)
    name = await r.get("user:1")
    print('await r.set("user:1", "Tom", ex=3600)')
    print('await r.get("user:1") ->', name)
    print()
    print("注意：全部用 await，等待 Redis 时不阻塞事件循环。")

    # 2. 异步缓存旁路（模拟 FastAPI 路由）
    section("2. 异步缓存旁路（模拟 FastAPI 路由）")

    async def get_user(user_id):
        key = f"user:{user_id}"
        cached = await r.get(key)
        if cached:
            return cached, True          # 命中缓存
        user = f"从数据库查出的 user{user_id}"
        await r.set(key, user, ex=3600)  # 回填缓存
        return user, False

    result, hit = await get_user(1)
    print("  第 1 次：", result, "| 命中缓存：", hit)
    result, hit = await get_user(1)
    print("  第 2 次：", result, "| 命中缓存：", hit)

    await r.aclose()


asyncio.run(main())

# 3. 完整技术链
section("3. 完整技术链：把前面学的串起来")

print("Python asyncio")
print("     ↓")
print("FastAPI（async def 路由）")
print("     ↓")
print("Redis（异步客户端，缓存热点）")
print("     ↓")
print("PostgreSQL（存业务数据）")
print()
print("这才是学习 Redis 的真正目的：在异步后端里做缓存。")

section("小结")
print("1. redis.asyncio.Redis 提供异步 API，配合 await 使用。")
print("2. async def 路由里用 await redis.get/set，不阻塞事件循环。")
print("3. 技术链：asyncio -> FastAPI -> Redis -> PostgreSQL。")
