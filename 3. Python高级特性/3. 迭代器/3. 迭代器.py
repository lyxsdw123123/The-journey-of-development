# -*- coding: utf-8 -*-
"""
3. 迭代器（Iterator）—— 可运行演示脚本
========================================

核心认知：

    for 循环背后其实是「迭代器协议」：

        for item in data:
            等价于
        it = iter(data)          # 得到迭代器
        while True:
            try:
                item = next(it)  # 不断取下一个
            except StopIteration:
                break            # 取完就停

    生成器其实就是一种迭代器。

运行：python "3. 迭代器.py"
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


# 1. iter 与 next
section("1. iter() 与 next()")

nums = [1, 2, 3]
it = iter(nums)          # 从列表拿到「迭代器」
print("it = iter(nums) ->", it)
print()
print("next(it) ->", next(it))   # 1
print("next(it) ->", next(it))   # 2
print("next(it) ->", next(it))   # 3
print()
print("再 next 就会抛 StopIteration，表示取完了。")

# 2. for 循环的本质
section("2. for 循环的本质")

nums = [1, 2, 3]
print("for 循环写法：")
for item in nums:
    print("  ", item)
print()
print("等价的手写版本：")
it = iter(nums)
while True:
    try:
        item = next(it)
    except StopIteration:
        break
    print("  ", item)
print()
print("for -> iterator -> next()，这就是迭代器协议。")

# 3. 可迭代对象 vs 迭代器
section("3. 可迭代对象 vs 迭代器")

nums = [1, 2, 3]
print("列表是可迭代对象（iterable），但不是迭代器：")
print("  iter(nums) 存在 ->", hasattr(nums, "__iter__"))
print("  next(nums) 会报错 -> 列表不能直接 next")
print()
print("iter(nums) 返回的才是迭代器（iterator）：")
it = iter(nums)
print("  hasattr(it, '__next__') ->", hasattr(it, "__next__"))
print()
print("可迭代对象：能被 iter() 处理（有 __iter__）。")
print("迭代器：能不断 next()（有 __next__），取完抛 StopIteration。")

# 4. 自己实现一个迭代器
section("4. 自己实现一个迭代器（__iter__ + __next__）")


class CountDown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self            # 迭代器返回自己

    def __next__(self):
        if self.current < 0:
            raise StopIteration  # 取完，停止
        value = self.current
        self.current -= 1
        return value


print("for x in CountDown(3)：")
for x in CountDown(3):
    print("  ", x)

# 5. 生成器是迭代器
section("5. 生成器其实就是一种迭代器")


def gen():
    yield 1
    yield 2


g = gen()
print("生成器有 __iter__ ->", hasattr(g, "__iter__"))
print("生成器有 __next__ ->", hasattr(g, "__next__"))
print("next(g) ->", next(g))
print("next(g) ->", next(g))
print()
print("生成器自动实现了迭代器协议，所以能直接用 for 循环遍历。")

section("小结")
print("1. for 循环本质：iter() -> next() -> StopIteration。")
print("2. 可迭代对象：能被 iter() 处理；迭代器：能不断 next()。")
print("3. 自定义迭代器：实现 __iter__ 和 __next__。")
print("4. 生成器是一种迭代器（自动实现迭代器协议）。")
