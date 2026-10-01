# -*- coding: utf-8 -*-
"""
9. asyncio 源码导读 —— 可运行讲解脚本
=====================================

核心认知：

    想真正吃透 asyncio，最终要读它的源码（Lib/asyncio/）。

    但不要一上来就从头读，推荐分三阶段：

        第一阶段：理解 async / await / Coroutine / Task / Future / Event Loop
        第二阶段：自己写 asyncio.run / create_task / gather / sleep
        第三阶段：读源码，重点追 asyncio.run -> Event Loop -> create_task
                  -> Task -> Future -> I/O

    本脚本打印 asyncio 源码位置和目录结构，帮你定位要读的文件。

运行：python "9. asyncio 源码导读.py"
"""
import sys
import asyncio
import os

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. asyncio 源码在哪
section("1. asyncio 源码在哪里")

print("asyncio 模块文件：", asyncio.__file__)
asyncio_dir = os.path.dirname(asyncio.__file__)
print("asyncio 目录：", asyncio_dir)
print()
print("目录里核心文件：")
print("  events.py       事件循环、Future、Task 的接口")
print("  base_events.py  事件循环的基础实现")
print("  tasks.py        Task、gather、sleep、create_task")
print("  futures.py      Future 实现")
print("  runners.py      asyncio.run 实现")

# 2. 三阶段学习路线
section("2. 三阶段学习路线")

print("第一阶段（先理解概念）：")
print("  async / await / Coroutine / Task / Future / Event Loop")
print("  <- 前面 8 节就是这个阶段")
print()
print("第二阶段（自己写）：")
print("  asyncio.run()")
print("  asyncio.create_task()")
print("  asyncio.gather()")
print("  asyncio.sleep()")
print("  <- 用熟了再读源码，否则看不懂")
print()
print("第三阶段（读源码）：")
print("  asyncio/")
print("  ├── events.py")
print("  ├── tasks.py")
print("  ├── futures.py")
print("  └── base_events.py")

# 3. 重点追什么
section("3. 读源码时重点追什么")

print("推荐追踪路径：")
print("  asyncio.run()")
print("     ↓")
print("  Event Loop（events.py / base_events.py）")
print("     ↓")
print("  create_task()（tasks.py）")
print("     ↓")
print("  Task（tasks.py，是 Future 子类）")
print("     ↓")
print("  Future（futures.py）")
print("     ↓")
print("  _event_loop 调度 I/O")
print()
print("不要逐行读，带着问题追：")
print("  * asyncio.run 里到底做了什么？")
print("  * create_task 如何把协程变成 Task？")
print("  * await 一个 Future 时，事件循环怎么『暂停/恢复』？")

section("小结")
print("1. 先懂概念，再自己写，最后读源码。")
print("2. 重点文件：events.py / tasks.py / futures.py / base_events.py。")
print("3. 追踪路径：asyncio.run -> Event Loop -> create_task -> Task -> Future -> I/O。")
print("4. 带着问题读，不要逐行硬啃。")
