# -*- coding: utf-8 -*-
"""
2. Coroutine 协程与 await —— 可运行演示脚本
===========================================

核心认知：

    1) async def 定义的函数，调用它不会直接执行函数体，
       而是返回一个「协程对象」（Coroutine Object）。

        async def hello():
            print("hello")

        result = hello()   # -> <coroutine object ...>，并没有打印 hello

    2) await 不是简单的「等待」：
        await X 表示「当前协程暂时让出执行权，等 X 完成后再继续」。

运行：python "2. Coroutine 协程与 await.py"
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


# 1. async def 返回协程对象
section("1. async def 返回的是协程对象，不是直接执行")


async def hello():
    print("hello")


result = hello()
print("result = hello()  ->", result)
print("类型：", type(result).__name__)
print()
print("注意：上面并没有打印 hello！")
print("调用 async def 函数，只是拿到一个『协程对象』，函数体还没执行。")
result.close()   # 关闭协程，避免 "never awaited" 警告
print("（若既不 await 也不 close，Python 会警告 coroutine was never awaited）")
print()
print("对比普通函数：")
def normal():
    return "hello"
print("  normal() ->", normal(), "  （立即执行并返回）")

# 2. 怎么真正执行协程：asyncio.run
section("2. 真正执行协程：asyncio.run")


async def hello2():
    print("hello")


print("执行 asyncio.run(hello2())：")
asyncio.run(hello2())
print()
print("asyncio.run 会创建事件循环，真正驱动协程执行。")

# 3. await 的本质：让出执行权
section("3. await 的本质：暂时让出执行权")


async def main():
    print("  步骤1：开始执行")
    await asyncio.sleep(1)   # 让出执行权，事件循环去处理别的任务
    print("  步骤2：1 秒后回来继续")


print("await 不是简单『等待』，而是：")
print("  当前协程让出执行权 -> 事件循环处理其他任务 -> 条件满足 -> 回来继续")
print()
asyncio.run(main())
print()
print("所以 await database.query() 更准确的理解是：")
print("  『当前协程等数据库，同时把执行机会交还给事件循环』。")
print("  这是 asyncio 最重要的思想之一。")

section("小结")
print("1. async def 函数调用后返回协程对象，不直接执行。")
print("2. asyncio.run() 驱动协程真正执行。")
print("3. await = 让出执行权 + 等待结果，不是傻等。")
