# -*- coding: utf-8 -*-
"""
1. 为什么需要 asyncio —— 可运行演示脚本
========================================

核心认知：

    传统同步代码在「等待 I/O（数据库/网络/文件）」时，CPU 其实在傻等，
    没做有意义的工作。大量请求就会产生大量「等待」。

    asyncio 的核心思想：等待 I/O 的时候不要傻等，把执行机会让给其他任务。

    所以 asyncio 最适合 I/O 密集（HTTP/数据库/Redis/文件/网络），
    而不是纯 CPU 密集计算。

运行：python "1. 为什么需要 asyncio.py"
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


# 1. 同步代码的问题
section("1. 同步代码：等待时 CPU 傻等")


def sync_task(name):
    print(f"  {name} 开始")
    time.sleep(1)          # 模拟「等待数据库返回」，整个线程被卡住
    print(f"  {name} 完成")


print("同步串行处理 3 个请求（每个等 1 秒）：")
t0 = time.perf_counter()
for name in ["请求1", "请求2", "请求3"]:
    sync_task(name)
print(f"  同步总耗时：{time.perf_counter() - t0:.2f} 秒")
print()
print("问题：等待数据库时，CPU 没做任何有意义的事，时间全浪费在『等』上。")

# 2. 异步：等待时让出执行权
section("2. 异步：等待时把机会让给别的任务")


async def async_task(name):
    print(f"  {name} 开始")
    await asyncio.sleep(1)   # 模拟等待 I/O，此时让出执行权
    print(f"  {name} 完成")


async def main():
    await asyncio.gather(
        async_task("请求1"),
        async_task("请求2"),
        async_task("请求3"),
    )


print("异步并发处理 3 个请求（每个等 1 秒）：")
t0 = time.perf_counter()
asyncio.run(main())
print(f"  异步总耗时：{time.perf_counter() - t0:.2f} 秒")
print()
print(f"对比：同步 3 秒 -> 异步 1 秒。因为等待时 CPU 去处理别的请求了。")

# 3. asyncio 适合什么
section("3. asyncio 适合什么、不适合什么")

print("适合（I/O 密集）：")
print("  HTTP 请求、数据库、Redis、文件 I/O、网络通信、WebSocket、API 调用")
print()
print("不适合（CPU 密集）：")
print("  纯计算任务（矩阵运算、大量循环）——异步不会让它变快，")
print("  因为 asyncio 是单线程，不是多核并行（见第 6 节）。")

section("小结")
print("1. 同步：等待 I/O 时 CPU 傻等，大量请求 = 大量等待。")
print("2. asyncio：等待 I/O 时让出执行权，去做别的任务。")
print("3. 适合 I/O 密集，不适合纯 CPU 计算。")
