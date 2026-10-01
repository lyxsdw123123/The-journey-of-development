# -*- coding: utf-8 -*-
"""
7. asyncio 常用工具 —— 可运行演示脚本
=====================================

核心认知：

    掌握核心概念后，还要会用这些「工具」：

        asyncio.gather()     并发跑多个任务，收集结果
        asyncio.wait()       更细粒度的等待控制
        异步上下文管理器      async with（__aenter__ / __aexit__）
        异步迭代器           async for（__aiter__ / __anext__）
        asyncio.Queue        生产-消费模型
        asyncio.Semaphore    限制并发数

运行：python "7. asyncio 常用工具.py"
"""
import sys
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


# 1. gather
section("1. asyncio.gather：并发 + 收集结果")


async def fetch(i):
    await asyncio.sleep(0.1)
    return f"结果{i}"


async def main_gather():
    results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
    print("  gather 返回：", results)


asyncio.run(main_gather())

# 2. 异步上下文管理器
section("2. 异步上下文管理器：async with")


class AsyncResource:
    async def __aenter__(self):
        print("  [打开] 异步资源")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("  [关闭] 异步资源")


async def main_cm():
    async with AsyncResource():
        print("  [使用] 资源")


asyncio.run(main_cm())
print("  对应数据库：async with db.connection() —— 异步版 with。")

# 3. 异步迭代器
section("3. 异步迭代器：async for")


class AsyncCounter:
    def __init__(self, n):
        self.n = n
        self.i = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.i >= self.n:
            raise StopAsyncIteration
        self.i += 1
        return self.i


async def main_iter():
    print("  async for 遍历：", end=" ")
    async for x in AsyncCounter(3):
        print(x, end=" ")
    print()


asyncio.run(main_iter())

# 4. Queue：生产-消费
section("4. asyncio.Queue：生产-消费模型")


async def producer(q):
    for i in range(3):
        await q.put(i)
        print(f"  生产 {i}")
        await asyncio.sleep(0.05)


async def consumer(q):
    for _ in range(3):
        item = await q.get()
        print(f"  消费 {item}")


async def main_queue():
    q = asyncio.Queue()
    await asyncio.gather(producer(q), consumer(q))


asyncio.run(main_queue())

# 5. Semaphore：限制并发数
section("5. asyncio.Semaphore：限制并发数")


sem = asyncio.Semaphore(2)   # 最多同时 2 个


async def limited(name):
    async with sem:
        print(f"  {name} 进入（当前最多 2 个并发）")
        await asyncio.sleep(0.3)
        print(f"  {name} 离开")


async def main_sem():
    await asyncio.gather(*(limited(f"任务{i}") for i in range(5)))


asyncio.run(main_sem())
print("  用途：爬虫限流、限制数据库并发连接数，避免打爆下游。")

section("小结")
print("1. gather：并发跑 + 收集结果（最常用）。")
print("2. 异步上下文管理器 async with / 异步迭代器 async for。")
print("3. Queue 做生产-消费；Semaphore 限制并发。")
print("4. 这些是异步后端（爬虫、API、流处理）的日常工具。")
