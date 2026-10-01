# -*- coding: utf-8 -*-
"""
4. 上下文管理器（Context Manager）—— 可运行演示脚本
====================================================

核心认知：

    上下文管理器负责「自动管理资源」，配合 with 使用：

        with open("a.txt") as f:
            data = f.read()

    等价于：

        f = open("a.txt")
        try:
            data = f.read()
        finally:
            f.close()      # 无论是否异常，都会关闭

    数据库、文件、锁等「用完必须释放」的资源，都用它保证安全释放。

运行：python "4. 上下文管理器.py"
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


# 1. with 与 try/finally 等价
section("1. with 与 try/finally 等价")

print("with 写法：")
print('  with open("a.txt") as f:')
print('      data = f.read()')
print()
print("完全等价于：")
print('  f = open("a.txt")')
print('  try:')
print('      data = f.read()')
print('  finally:')
print('      f.close()   # 无论是否异常，都会执行')
print()
print("上下文管理器的作用：自动管理资源，保证『打开 -> 执行 -> 关闭』。")

# 2. 自己实现上下文管理器
section("2. 自己实现一个上下文管理器")


class MyContext:
    def __enter__(self):
        print("    进入")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("    退出")


print("执行 with MyContext():")
with MyContext():
    print("    运行")
print()
print("顺序：__enter__（进入）-> 块内代码 -> __exit__（退出）。")

# 3. 为什么后端重要：数据库连接
section("3. 为什么后端重要：数据库连接")


class Database:
    def __enter__(self):
        print("    获取数据库连接")
        return self

    def query(self):
        print("    执行 SQL")

    def __exit__(self, exc_type, exc, tb):
        print("    提交事务、释放连接")


print("执行 with Database() as db:")
with Database() as db:
    db.query()
print()
print("流程：获取连接 -> 执行 SQL -> 提交事务、释放连接。")
print("即使 SQL 抛异常，__exit__ 也会执行，连接不会泄漏。")

# 4. 异常也保证释放
section("4. 即使异常，也保证释放")


class SafeResource:
    def __enter__(self):
        print("    打开资源")
        return self

    def __exit__(self, exc_type, exc, tb):
        print("    关闭资源（异常也执行）")
        return False   # 不吞异常


try:
    with SafeResource():
        raise ValueError("出错了")
except ValueError as e:
    print(f"    外层捕获到：{e}")

section("小结")
print("1. with 等价于 try/finally，自动管理资源。")
print("2. __enter__ 进入时准备资源，__exit__ 退出时释放。")
print("3. 数据库：获取连接 -> 执行 SQL -> 提交事务、释放连接。")
print("4. 即使异常，资源也保证释放，不会泄漏。")
