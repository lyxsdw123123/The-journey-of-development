# -*- coding: utf-8 -*-
"""
2. 生成器（Generator）—— 可运行演示脚本
========================================

核心认知：

    用 yield 的函数是「生成器」，它不会一次算出所有结果，而是
    「要一个、算一个、给一个」，用多少算多少，省内存。

        普通函数：return [1,2,3]   -> 一次性创建整个列表
        生成器：  yield 1; yield 2 -> 逐个产出，边产边停

    大数据（如 10 亿条记录）不能一次全读进内存，必须用生成器。

运行：python "2. 生成器.py"
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


# 1. 普通函数 vs 生成器
section("1. 普通函数 vs 生成器")


def get_numbers_list():
    return [1, 2, 3, 4, 5]   # 一次性创建整个列表


def get_numbers_gen():
    yield 1
    yield 2
    yield 3
    yield 4
    yield 5


print("普通函数返回：", get_numbers_list())   # [1,2,3,4,5]
print("生成器返回：  ", get_numbers_gen())    # <generator object ...>
print()
print("生成器不会立刻算结果，而是返回一个生成器对象，等你逐个取。")

# 2. 逐个取值：for 循环与 next
section("2. 逐个取值：for 循环与 next")

gen = get_numbers_gen()
print("for x in 生成器：")
for x in gen:
    print("  ", x)
print()
print("也可以手动 next()：")
g = get_numbers_gen()
print("  next(g) ->", next(g))
print("  next(g) ->", next(g))
print("  next(g) ->", next(g))
print()
print("过程：yield 1 暂停 -> 下次 next 继续 -> yield 2 暂停 ...")

# 3. 内存对比：列表 vs 生成器
section("3. 内存对比：列表 vs 生成器")

N = 1_000_000
lst = list(range(N))
gen = (i for i in range(N))   # 生成器表达式

print(f"list(range({N})) 占内存：{sys.getsizeof(lst):,} 字节（约 {sys.getsizeof(lst)/1024/1024:.1f} MB）")
print(f"生成器占内存：          {sys.getsizeof(gen):,} 字节")
print()
print("列表把 100 万个元素全部存下；生成器只存一个『当前状态』，")
print("要一个才算一个，内存占用几乎不随数据量增长。")

# 4. 大数据：逐行读文件
section("4. 大数据场景：逐行读文件（10 亿条也不爆）")


def read_lines(file):
    for line in file:
        yield line   # 每次只产出一行


print("假设 trajectory.csv 有 10 亿行：")
print("  如果用 data = read_all()，10 亿条会占几十 GB，直接爆内存。")
print()
print("用生成器：")
print("  读取第 1 行 -> 处理 -> 释放 -> 读取第 2 行 -> ...")
print("  内存里永远只保留一条，无论文件多大都不怕。")
print()
print("代码：")
print("  for line in read_lines(open('trajectory.csv')):")
print("      process(line)   # 一次只处理一行")

# 5. FastAPI 里的流式传输
section("5. FastAPI 里也用生成器：流式传输")

print("大文件下载不能一次性读进内存，要分块（chunk）流式发送：")
print()
print("  async def file_stream():")
print("      while True:")
print("          chunk = file.read(1024)   # 每次读 1KB")
print("          if not chunk:")
print("              break")
print("          yield chunk               # 边读边发")
print()
print("实现：流式传输，内存只占一个 chunk 大小。")

section("小结")
print("1. yield 让函数变成生成器，逐个产出、暂停、继续。")
print("2. 生成器惰性求值：要一个才算一个，不一次算完。")
print("3. 内存：列表存全部，生成器只存当前状态。")
print("4. 大数据（文件、流）必须用生成器，避免内存爆炸。")
