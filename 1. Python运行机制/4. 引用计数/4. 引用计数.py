# -*- coding: utf-8 -*-
"""
4. 引用计数（Reference Counting）—— 可运行演示脚本
=====================================================

核心认知：

    CPython 最核心的内存机制：每个对象都有一个「引用计数」，
    记录有多少个名字 / 容器在引用它。

        a = [1,2,3]   ->  列表对象 ref_count = 1
        b = a         ->  ref_count = 2
        del a         ->  ref_count = 1
        del b         ->  ref_count = 0  ->  立即释放

    引用计数归零，对象立刻被销毁（确定性回收），不用等垃圾回收器。

运行：python "4. 引用计数.py"
"""
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


# 1. 查看引用计数
section("1. 用 sys.getrefcount 查看引用计数")

a = [1, 2, 3]
print("a = [1,2,3]")
print("  sys.getrefcount(a) =", sys.getrefcount(a))
print("  （注意：结果比『真实值』多 1，因为把 a 传给 getrefcount 时，")
print("        参数本身又临时多了一个引用。真实值 = 返回值 - 1。）")
print()

b = a
print("b = a 之后：")
print("  sys.getrefcount(a) =", sys.getrefcount(a), "  # 多了一个引用")
print()

container = [a]
print("把 a 放进容器 container = [a] 之后：")
print("  sys.getrefcount(a) =", sys.getrefcount(a), "  # 又多了一个引用")
print()

del b
print("del b 之后：")
print("  sys.getrefcount(a) =", sys.getrefcount(a), "  # 减一")
print()

del container
print("del container 之后：")
print("  sys.getrefcount(a) =", sys.getrefcount(a), "  # 再减一")

# 2. 引用归零 -> 立即释放（用弱引用观察生死）
section("2. 引用计数归零 -> 对象立即被回收")


class Foo:
    def __del__(self):
        print("    [Foo.__del__] 对象被销毁了！")


obj = Foo()
print("创建 obj = Foo()")
# weakref.ref 是「弱引用」：能看到对象，但不增加引用计数
r = weakref.ref(obj)
print("弱引用 r() 现在指向：", r())
print()
print("执行 del obj ...")
del obj
print()
print("del 之后，弱引用 r() 指向：", r())
print("  -> None 说明对象已被立即回收（引用计数归零，无需等 GC）")

# 3. 引用计数规则小结
section("3. 哪些操作会改变引用计数")

print("引用 +1 的常见操作：")
print("  * 赋值给名字        b = a")
print("  * 放进容器          lst.append(a)、d[key] = a")
print("  * 函数传参          f(a)（函数内部临时 +1，返回后 -1）")
print()
print("引用 -1 的常见操作：")
print("  * del 名字          del a")
print("  * 离开作用域        局部变量随函数返回而失效")
print("  * 从容器移除        lst.remove(a)")
print()
print("引用归 0 -> 对象立刻销毁（__del__ 被调用）。")

section("小结")
print("1. 每个对象都有引用计数，记录被引用的次数。")
print("2. sys.getrefcount 返回值比真实值多 1（参数本身）。")
print("3. 引用计数归零，对象『立即』释放，不是等垃圾回收。")
print("4. weakref（弱引用）能观察对象生死，却不增加引用计数。")
