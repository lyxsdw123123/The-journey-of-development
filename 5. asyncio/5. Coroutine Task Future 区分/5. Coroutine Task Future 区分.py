# -*- coding: utf-8 -*-
"""
5. Coroutine / Task / Future 区分 —— 可运行演示脚本
====================================================

核心认知：

    这是后面看 FastAPI、aiohttp、数据库驱动源码时非常重要的一组概念：

        Coroutine   要执行的异步函数（async def）
        Task        被 Event Loop 调度的协程
        Future      一个未来会产生结果的容器/状态对象

    关系：
        async def -> Coroutine -> Task -> Event Loop 调度 -> Future/I/O 结果 -> 完成

运行：python "5. Coroutine Task Future 区分.py"
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


async def foo():
    await asyncio.sleep(0)
    return 42


# 1. 三者类型
section("1. 看三个对象的类型")


async def main():
    # Coroutine：调用 async def 得到
    coro = foo()
    print("  coro 类型：", type(coro).__name__)

    # Task：create_task 包装 coroutine
    task = asyncio.create_task(coro)
    print("  task 类型：", type(task).__name__)

    # Task 是 Future 的子类
    print("  Task 是 Future 的子类？", issubclass(asyncio.Task, asyncio.Future))

    # Future：底层的结果容器
    fut = asyncio.get_running_loop().create_future()
    print("  fut 类型：", type(fut).__name__)

    await task


asyncio.run(main())

# 2. 概念对照
section("2. 概念对照")

print("Coroutine = 要执行的异步函数（还没被调度）")
print("Task      = 被事件循环调度的协程（已经排上队）")
print("Future    = 一个『未来会产生结果』的容器/状态对象")
print()
print("Task 本质上是一个『驱动协程前进的 Future』。")

# 3. 关系图
section("3. 关系图")

print("async def")
print("   ↓")
print("Coroutine（协程对象）")
print("   ↓ create_task")
print("Task（交给事件循环）")
print("   ↓")
print("Event Loop 调度")
print("   ↓")
print("Future / I/O 结果")
print("   ↓")
print("完成")
print()
print("注意：这只是第一阶段的理解模型。读源码时会发现三者关系更细致。")

# 4. ensure_future
section("4. asyncio.ensure_future 也能创建 Task")


async def demo():
    task = asyncio.ensure_future(foo())
    print("  ensure_future 返回：", type(task).__name__)
    result = await task
    print("  结果：", result)


asyncio.run(demo())
print()
print("ensure_future：协程 -> Task；Future -> 原样返回。create_task 更推荐。")

section("小结")
print("1. Coroutine：async def 定义的异步函数。")
print("2. Task：被事件循环调度的协程（是 Future 子类）。")
print("3. Future：未来产生结果的容器。")
print("4. 关系：async def -> Coroutine -> Task -> 调度 -> 完成。")
