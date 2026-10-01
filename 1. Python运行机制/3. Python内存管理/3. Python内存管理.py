# -*- coding: utf-8 -*-
"""
3. Python 内存管理 —— 可运行演示脚本
=====================================

核心认知：

    Python 的内存主要是一块「私有堆」（Python Private Heap），
    里面存放着所有 Python 对象。

        变量表（命名空间）            私有堆
        ----------------              ---------------
        x  ────────────────────→      Integer 对象 100
                                       （值 + 类型 + 引用计数）

    变量本身很小（只是一个名字 + 一个指针），真正占内存的是「对象」。
    每个对象除了数据，还带「对象头」（类型信息 + 引用计数）。

运行：python "3. Python内存管理.py"
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


# 1. 变量很小，对象占内存
section("1. 变量 vs 对象：谁真正占内存")

print("sys.getsizeof 可以看一个对象占多少字节：")
print()

x = 100
big = 10 ** 100

print("int 对象 x = 100     占：", sys.getsizeof(x), "字节")
print("int 对象 10**100     占：", sys.getsizeof(big), "字节")
print()
print("注意：int 越大占内存越多（大整数按位数存储），")
print("      而变量名 x 只是命名空间里的『名字 + 指针』，开销极小。")
print("      真正占内存的是对象，不是变量。")

# 2. 容器对象：对象头 + 指针数组
section("2. 列表的真相：对象头 + 一堆指针")

empty = []
one = [1]
three = [1, 2, 3]

print("空列表 []         占：", sys.getsizeof(empty), "字节  <- 这就是『对象头』的固定开销")
print("列表 [1]          占：", sys.getsizeof(one), "字节")
print("列表 [1,2,3]      占：", sys.getsizeof(three), "字节")
print()
print("规律：列表本身不存数据，只存『指向每个元素的指针』（64 位系统每指针 8 字节）。")
print("      空列表对象头 56 字节，每个指针槽 8 字节。")
print("      注意 [1,2,3] 是 88 而非 56+3×8=80：列表会『预分配多余容量』")
print("      （overallocation），为后续 append 预留空间，避免频繁扩容。")
print()
print("关键：getsizeof 只算『容器自身』，不算元素引用的对象。")
lst = [1000, 2000, 3000]
print("列表 [1000,2000,3000] 自身占：", sys.getsizeof(lst), "字节")
print("但 3 个大 int 还各自占：", sys.getsizeof(1000), "字节（没有算进上面那个数）")

# 3. 小整数缓存
section("3. 小整数缓存（-5 ~ 256 被预先创建并复用）")

# 用 int("...") 动态生成，避开编译期常量折叠，结果才可靠
a = int("100")
b = int("100")
c = int("1000")
d = int("1000")

print("a = int('100');  b = int('100')")
print("  a is b ?", a is b, "  # True：100 在 -5~256 缓存内，复用同一对象")
print()
print("c = int('1000'); d = int('1000')")
print("  c is d ?", c is d, "  # False：1000 超出缓存，各建新对象")
print()
print("意义：频繁使用的小整数不重复分配内存，省时省空间。")

# 4. 内存分配器：分层管理
section("4. CPython 的内存分配器（pymalloc）")

print("CPython 不从操作系统逐字节申请内存，而是分层管理：")
print()
print("  Arena（大块，如 256KB）")
print("      └── Pool（中块，如 4KB）")
print("            └── Block（小块，按对象大小分类）")
print()
print("好处：")
print("  * 小对象分配 / 释放极快（几乎只是移动指针）")
print("  * 减少与操作系统 malloc/free 的交互次数")
print("  * 同类大小的对象集中存放，缓存友好")
print()
print("这解释了为什么 Python 创建大量小对象很快，但内存未必立刻还给操作系统。")

section("小结")
print("1. 变量是「名字 + 指针」，对象才真正占内存。")
print("2. 每个对象都带对象头（类型、引用计数），有固定开销。")
print("3. 容器（list 等）存的是指针数组，不是数据本身。")
print("4. 小整数 -5~256 被缓存复用。")
print("5. pymalloc 分层管理内存，小对象分配极快。")
