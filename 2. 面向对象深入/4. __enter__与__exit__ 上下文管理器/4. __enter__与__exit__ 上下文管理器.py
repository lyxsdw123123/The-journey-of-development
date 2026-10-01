# -*- coding: utf-8 -*-
"""
4. __enter__ 与 __exit__ 上下文管理器 —— 可运行演示脚本
========================================================

核心认知：

    __enter__ / __exit__ 是「上下文管理器」协议，对应 with 语句。

        with open("test.txt") as f:
            data = f.read()

    Python 内部其实是：
        f = open("test.txt")
        f.__enter__()      # 进入 with：打开资源
        data = f.read()    # 使用资源
        f.__exit__()       # 退出 with：关闭资源（即使异常也会执行）

    数据库、网络连接、文件、锁等「用完必须释放」的资源，都用它管理。

运行：python "4. __enter__与__exit__ 上下文管理器.py"
"""
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. with 背后的秘密
section("1. with 背后：__enter__ 与 __exit__")

print("代码：")
print('  with open("test.txt") as f:')
print("      data = f.read()")
print()
print("Python 内部等价于：")
print("  f = open('test.txt')")
print("  f.__enter__()     # 进入 with：打开文件")
print("  data = f.read()   # 使用")
print("  f.__exit__()      # 退出 with：关闭文件")
print()
print("__enter__ 负责「进入时准备资源」，__exit__ 负责「退出时释放资源」。")

# 2. 自己实现上下文管理器
section("2. 自己实现一个上下文管理器")


class MyFile:
    def __enter__(self):
        print("    打开资源")
        return self          # 返回值会赋给 with ... as 后面的变量

    def __exit__(self, exc_type, exc_value, traceback):
        print("    关闭资源")
        # 返回 False（或 None）表示：块内若有异常，继续向外抛


print("执行 with MyFile() as f:")
with MyFile() as f:
    print("    使用资源")
print()
print("顺序：__enter__（打开）-> 块内代码 -> __exit__（关闭）。")

# 3. __exit__ 的三个参数：异常信息
section("3. __exit__ 的三个参数与异常处理")


class SafeFile:
    def __enter__(self):
        print("    进入")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print("    正常退出：无异常")
        else:
            print(f"    异常退出：{exc_type.__name__}: {exc_value}")
        print("    释放资源")
        return False   # False：不吞掉异常；True：吞掉异常


print("正常情况：")
with SafeFile():
    print("    做一些正常的事")
print()
print("异常情况（资源仍被释放）：")
try:
    with SafeFile():
        raise ValueError("出错了")
except ValueError as e:
    print(f"    外层捕获到异常：{e}")
print()
print("关键：即使块内抛异常，__exit__ 依然会执行，资源依然被释放。")

# 4. 数据库连接：为什么后端大量用 with
section("4. 实战：数据库连接（FastAPI 里大量类似）")

print("数据库操作最怕『连接忘了关』，用 with 就稳了：")
print()
print('  with database.connection():')
print('      查询数据')
print()
print("进入 with：连接数据库；退出 with：关闭连接。")
print("FastAPI 里：")
print('  with Session(engine) as session:')
print('      session.query(...)')
print()
print("本质就是：__enter__ 建会话 + __exit__ 关会话。")
print("这样即使查询抛异常，连接也会被安全关闭，不会泄漏。")

section("小结")
print("1. __enter__ / __exit__ 是上下文管理器协议，对应 with。")
print("2. __enter__ 进入时准备资源，返回值赋给 as 变量。")
print("3. __exit__ 退出时释放资源，即使异常也执行。")
print("4. 文件、数据库连接、锁等「用完必须释放」的资源，一律用 with。")
