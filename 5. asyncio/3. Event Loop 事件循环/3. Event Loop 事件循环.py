# -*- coding: utf-8 -*-
"""
3. Event Loop 事件循环 —— 可运行演示脚本
========================================

核心认知：

    Event Loop（事件循环）是 asyncio 的核心。

             Event Loop
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
     Task 1     Task 2     Task 3
       │          │          │
       ↓          ↓          ↓
     await      await       CPU
       │          │          │
       └──────┬───┘          │
              ↓
        Event Loop
              │
              ↓
       谁可以继续执行？

    它不断循环：检查任务 -> 谁能继续 -> 执行 -> 遇到 await 切换 -> 再循环。

运行：python "3. Event Loop 事件循环.py"
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


# 1. 看当前事件循环
section("1. asyncio.run 会创建事件循环")


async def show_loop():
    loop = asyncio.get_running_loop()
    print("  当前事件循环对象：", loop)
    print("  类型：", type(loop).__name__)


asyncio.run(show_loop())
print()
print("asyncio.run() 内部：创建 Event Loop -> 运行协程 -> 关闭 Loop。")

# 2. 事件循环如何调度多个任务
section("2. 事件循环调度多个任务")


async def task(name, delay):
    print(f"  {name} 开始")
    await asyncio.sleep(delay)   # 在这里让出，事件循环去跑别的任务
    print(f"  {name} 完成（等了 {delay}s）")


async def main():
    # 三个任务交给事件循环并发调度
    await asyncio.gather(
        task("A", 3),
        task("B", 1),
        task("C", 2),
    )


print("三个任务 A(3s)、B(1s)、C(2s) 并发执行：")
asyncio.run(main())
print()
print("注意完成顺序：B 先完（1s），然后 C（2s），最后 A（3s）。")
print("事件循环在 B 等待时去跑 C，在 C 等待时去跑 A——不浪费等待时间。")

# 3. 事件循环的循环逻辑
section("3. 事件循环的循环逻辑")

print("Event Loop 不断做同一件事：")
print("  检查任务")
print("    ↓")
print("  哪个任务可以继续？")
print("    ↓")
print("  执行它")
print("    ↓")
print("  遇到 await / I/O 等待")
print("    ↓")
print("  切换到其他任务")
print("    ↓")
print("  循环")
print()
print("一句话：事件循环就是一个『大 while 循环』，不断把 CPU 时间片分给")
print("那些『不再等待』的任务。")

section("小结")
print("1. Event Loop 是 asyncio 的核心调度器。")
print("2. asyncio.run() 创建并运行事件循环。")
print("3. 事件循环：检查 -> 执行 -> 遇 await 切换 -> 循环。")
print("4. 等待中的任务不占 CPU，事件循环去跑别的任务。")
