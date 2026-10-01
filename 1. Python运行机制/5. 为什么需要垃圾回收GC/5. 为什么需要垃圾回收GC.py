# -*- coding: utf-8 -*-
"""
5. 为什么需要垃圾回收 GC —— 可运行演示脚本
===========================================

核心认知：

    引用计数有个致命盲区：循环引用（cyclic reference）。

        a.next = b
        b.next = a

        a ──→ b
        ↑     │
        └─────┘

    del a、del b 之后，两个对象仍互相引用，引用计数永远不为 0，
    于是「无法释放」——这就是循环引用。

    所以 CPython 除了引用计数，还有「垃圾回收器 GC」，
    专门找出这些「不可达」的循环引用并释放。

运行：python "5. 为什么需要垃圾回收GC.py"
"""
import gc
import sys
import weakref

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. 构造循环引用
section("1. 构造循环引用：两个对象互相引用")


class Node:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Node {self.name}>"


a = Node("A")
b = Node("B")
a.next = b
b.next = a

# 弱引用：观察对象生死，不增加引用计数
ra = weakref.ref(a)
rb = weakref.ref(b)

print("a.next = b；b.next = a（互相引用）")
print("删除前：ra() =", ra(), " rb() =", rb())
print()

# 2. 关键：del 之后对象还活着
section("2. del a、del b 之后：对象仍无法释放")

del a
del b

print("执行 del a、del b 之后：")
print("  ra() =", ra())   # 仍然不是 None！
print("  rb() =", rb())   # 仍然不是 None！
print()
print("原因：两个对象互相引用，引用计数都是 1（对方指着自己），")
print("      永远到不了 0，引用计数机制「看不见」它们该被回收。")
print()

# 3. GC 出手：找到不可达的循环并回收
section("3. 垃圾回收器 GC 出手")

collected = gc.collect()
print("gc.collect() 返回回收的不可达对象数：", collected)
print()
print("GC 之后：")
print("  ra() =", ra())   # 现在是 None
print("  rb() =", rb())   # 现在是 None
print()
print("GC 找到这两个「互相引用但外界够不着」的对象，把它们释放了。")

# 4. 分代回收
section("4. 分代回收（Generational GC）")

print("GC 把对象分成 3 代，越老越少被检查：")
print("  gc.get_count()     =", gc.get_count(), "  # (gen0, gen1, gen2) 待回收计数")
print("  gc.get_threshold() =", gc.get_threshold(), "  # 触发阈值")
print()
print("直觉：")
print("  * 新对象进 gen0，gen0 满了才检查 gen1，gen1 满了才检查 gen2。")
print("  * 大多数对象很快死亡（年轻代高死亡率），所以主要扫 gen0。")
print("  * 活得越久越可能是常驻对象，少扫省时间。")
print()

# 5. 什么时候需要手动关心 GC
section("5. 工程上何时手动 gc")

print("绝大多数情况：不用管，GC 自动跑。")
print("少数情况才手动干预：")
print("  * gc.collect()   手动触发一次完整回收")
print("  * gc.disable()   性能敏感、大量临时对象的场景临时关闭（高级用法）")
print("  * 内存持续上涨时，怀疑有循环引用泄漏，可 gc.collect() 排查")
print()
print("原则：优先写干净代码（用 with、及时 del、避免不必要的全局引用），")
print("      而不是依赖手动 gc。")

section("小结")
print("1. 引用计数搞不定的场景：循环引用。")
print("2. GC 专门回收『不可达』的循环引用对象。")
print("3. GC 是分代的：gen0 最频繁，gen2 最懒。")
print("4. 弱引用 weakref 是观察对象回收的利器。")
