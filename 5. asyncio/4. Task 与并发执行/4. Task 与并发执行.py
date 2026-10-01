# -*- coding: utf-8 -*-
"""
4. Task 与并发执行 —— 可运行演示脚本
====================================

核心认知：

    直接 await 两个协程是「顺序执行」：

        await task1()   # 等 task1 完成
        await task2()   # 才轮到 task2

    用 asyncio.create_task() 创建 Task，才能「并发执行」：

        t1 = asyncio.create_task(task1())
        t2 = asyncio.create_task(task2())
        await t1
        await t2

    Task 把协程「提交」给事件循环调度，两个任务就能同时推进。

运行：python "4. Task 与并发执行.py"
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


async def task(name):
    await asyncio.sleep(1)
    print(f"  {name} 完成")


# 1. 顺序 await：本质还是串行
section("1. 顺序 await：两个任务串行（2 秒）")


async def sequential():
    t0 = time.perf_counter()
    await task("task1")   # 等 1 秒
    await task("task2")   # 再等 1 秒
    print(f"  顺序 await 耗时：{time.perf_counter() - t0:.2f} 秒")


asyncio.run(sequential())
print()
print("await task1() 再 await task2()，本质上还是『先等 task1 完成，再跑 task2』。")

# 2. create_task：并发（1 秒）
section("2. create_task：两个任务并发（1 秒）")


async def concurrent():
    t0 = time.perf_counter()
    t1 = asyncio.create_task(task("task1"))   # 提交给事件循环
    t2 = asyncio.create_task(task("task2"))   # 提交给事件循环
    await t1
    await t2
    print(f"  create_task 并发耗时：{time.perf_counter() - t0:.2f} 秒")


asyncio.run(concurrent())
print()
print("create_task 后，两个任务同时开始等待，事件循环同时调度它们。")

# 3. 可视化对比
section("3. 对比")

print("顺序 await：")
print("  task1 ──等待1s──> 完成")
print("                       task2 ──等待1s──> 完成")
print("  总耗时 2 秒")
print()
print("create_task：")
print("  Task1 ──等待1s──────> 完成")
print("        ↘")
print("  Task2 ──等待1s──────> 完成")
print("        ↗")
print("  总耗时 1 秒（两个任务同时等）")
print()
print("从这一刻起，你才真正进入 asyncio 的世界。")

section("小结")
print("1. 顺序 await = 串行；create_task = 并发。")
print("2. Task 把协程提交给事件循环调度。")
print("3. 两个 1 秒任务：顺序 2 秒，并发 1 秒。")
