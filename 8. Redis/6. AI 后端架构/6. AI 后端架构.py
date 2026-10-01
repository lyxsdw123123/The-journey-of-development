# -*- coding: utf-8 -*-
"""
6. AI 后端架构 —— 可运行演示脚本
================================

核心认知：

    你以后可以形成这样的 AI 后端架构：

                    用户请求
                       ↓
                    FastAPI
                       ↓
                  业务逻辑层
                       ↓
                    Redis（缓存/限流/状态）
                       ↓
              ┌────────┴────────┐
              ↓                 ↓
         PostgreSQL            LLM
              ↓                 ↓
          业务数据            AI 结果

    对 GeoAI / LLM + GIS 后端，Redis 用于：LLM结果缓存、地图查询缓存、
    Session、限流、异步任务状态、Agent 状态。

运行：python "6. AI 后端架构.py"（需本机已启动 Redis）
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


# 1. 架构图
section("1. AI 后端架构图")

print("""                    用户请求
                       ↓
                    FastAPI
                       ↓
                  业务逻辑层
                       ↓
        ┌──────────────────────────┐
        │          Redis           │
        │  缓存 / 限流 / 任务状态    │
        └────────────┬─────────────┘
                     ↓
          ┌──────────┴──────────┐
          ↓                     ↓
     PostgreSQL                LLM
          ↓                     ↓
       业务数据               AI 结果""")


# 2. 综合演示：模拟 AI 后端缓存
section("2. 综合演示：模拟 AI 后端的缓存旁路")


async def main():
    r = Redis(host="127.0.0.1", port=6379, db=15, decode_responses=True, protocol=2)  # protocol=2 兼容老版 Redis
    await r.flushdb()

    async def ai_endpoint(question):
        """模拟 FastAPI 路由：先查 Redis，再决定是否调 LLM。"""
        key = f"cache:{question}"
        cached = await r.get(key)
        if cached:
            return cached, "命中缓存（不调 LLM）"
        answer = f"AI 关于「{question}」的回答..."
        await r.set(key, answer, ex=3600)
        return answer, "调 LLM 并缓存"

    for i in range(2):
        ans, src = await ai_endpoint("长沙有哪些高校")
        print(f"  第 {i+1} 次问：{src}")
        print(f"          答：{ans}")

    await r.aclose()


asyncio.run(main())

# 3. GeoAI 用途
section("3. 对 GeoAI / LLM + GIS 后端，Redis 的用途")

print("  * LLM 结果缓存      相同问题直接返回")
print("  * 地图查询缓存      热门区域查询缓存")
print("  * 用户 Session      登录态")
print("  * Token 限流        防滥用 API")
print("  * 异步任务状态      任务进行中/完成")
print("  * Agent 运行状态     多步骤 Agent 的中间状态")

section("小结")
print("1. 架构：FastAPI -> Redis -> PostgreSQL/LLM。")
print("2. Redis 在中间做缓存/限流/状态，加速 + 省钱。")
print("3. 对 GeoAI 后端：LLM 缓存、地图缓存、限流、任务状态。")
