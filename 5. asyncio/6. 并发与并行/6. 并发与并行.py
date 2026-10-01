# -*- coding: utf-8 -*-
"""
6. 并发与并行 —— 可运行演示脚本
================================

核心认知：

    asyncio 是「并发」（Concurrency），不是「并行」（Parallelism）。

        并发：一个线程，事件循环在多个任务间切换（交替推进）
        并行：多个 CPU 核心同时执行（真正同时）

    asyncio：一个线程 + Event Loop，所以 I/O 密集加速，CPU 密集不加速。

运行：python "6. 并发与并行.py"
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


# 1. 概念
section("1. 并发 vs 并行")

print("并发（Concurrency）：一个线程，事件循环在多个任务间『交替』推进。")
print("  一个线程 -> Event Loop -> T1 T2 T3 轮流跑")
print()
print("并行（Parallelism）：多个 CPU 核心『同时』执行。")
print("  多进程/多核 -> 真正同时跑")
print()
print("asyncio 属于前者：单线程 + 事件循环。")

# 2. I/O 密集：asyncio 有效
section("2. I/O 密集：asyncio 加速（并发）")


async def io_task(name):
    print(f"  {name} 开始")
    await asyncio.sleep(1)   # 等待时让出
    print(f"  {name} 完成")


async def io_main():
    t0 = time.perf_counter()
    await asyncio.gather(io_task("a"), io_task("b"))
    print(f"  I/O 并发耗时：{time.perf_counter() - t0:.2f} 秒（串行要 2 秒）")


asyncio.run(io_main())

# 3. CPU 密集：asyncio 不加速
section("3. CPU 密集：asyncio 不加速（单线程）")


async def cpu_task(n):
    s = 0
    for i in range(n):
        s += i
    return s


async def cpu_main():
    N = 10_000_000
    t0 = time.perf_counter()
    await asyncio.gather(cpu_task(N), cpu_task(N))
    dt = time.perf_counter() - t0
    print(f"  两个 CPU 任务 gather 耗时：{dt:.2f} 秒")
    print("  （几乎等于串行两倍——因为它们不会在计算中途让出，")
    print("    单线程只能一个接一个算，异步帮不上忙。）")


asyncio.run(cpu_main())

# 4. 总结
section("4. 总结")

print("asyncio 的优势来自『I/O 并发』，不是 CPU 计算。")
print()
print("  CPU 密集 -> 用 multiprocessing / C 扩展 / NumPy（多核并行）")
print("  I/O 密集 -> 用 asyncio / 多线程（并发）")

section("小结")
print("1. 并发：单线程交替推进；并行：多核同时执行。")
print("2. asyncio 是并发，不是并行。")
print("3. I/O 密集加速，CPU 密集不加速。")
