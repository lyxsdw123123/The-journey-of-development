# -*- coding: utf-8 -*-
"""
2. Python 变量模型 —— 可运行演示脚本
=====================================

核心认知（非常重要）：

    Python 的「变量」不是装数据的盒子，而是贴在对象上的「名字/标签」。
    变量保存的是「对象引用」（指向对象内存地址的指针），不是数据本身。

        a = [1, 2, 3]   ->  创建一个列表对象，a 保存指向它的引用
        b = a           ->  b 也保存指向「同一个」列表对象的引用（没有复制！）

    所以执行 b.append(4) 之后，a 看到的数据也变了——因为它们指向同一个对象。

运行：python "2. Python变量模型.py"
"""
import sys
import copy

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. 变量是引用，不是盒子
section("1. 变量是引用：a 和 b 指向同一个列表对象")

a = [1, 2, 3]
b = a

print("a =", a)
print("b =", b)
print("a 的地址 id(a) =", id(a))
print("b 的地址 id(b) =", id(b))
print("a is b ?", a is b)
print()
print("结论：a 和 b 的 id 完全相同 —— 它们指向同一个对象。")
print("      b = a 没有复制数据，只是让 b 也指向同一处。")

# 2. 通过 b 修改，a 也变化
section("2. 通过 b 修改对象，a 也「跟着变」")

b.append(4)
print("执行 b.append(4) 之后：")
print("  a =", a)
print("  b =", b)
print()
print("原因：b.append 不是「改 b」，而是「顺着 b 找到列表对象，改那个对象」。")
print("       a 也指向那个对象，所以 a 看到的数据自然变了。")

# 3. 可变 vs 不可变
section("3. 可变对象 vs 不可变对象")

print("可变对象（list / dict / set）：可以原地修改，所有引用者都看到变化。")
print("不可变对象（int / str / tuple）：无法原地改，只能创建新对象再重新绑定。")
print()

x = 10
y = x
print("x = 10; y = x  ->  x is y ?", x is y, "  (小整数被缓存，指向同一对象)")

y = 20
print("y = 20 之后：")
print("  x =", x, "  y =", y)
print("  x is y ?", x is y)
print("  注意：这里不是『把 10 改成 20』，而是让 y 重新指向新对象 20。")
print("        10 这个整数对象本身永远不变（不可变）。")

# 4. is 与 == 的区别
section("4. is（身份）与 ==（值）的区别")

a = [1, 2, 3]
b = [1, 2, 3]   # 一个「新的」列表，内容相同但对象不同

print("a = [1,2,3]; b = [1,2,3]（两个独立对象）")
print("  a == b ?", a == b, "   # 比较『值』是否相等 -> True")
print("  a is b ?", a is b, "   # 比较『是否同一个对象』 -> False")
print("  id(a) =", id(a))
print("  id(b) =", id(b))

# 5. 浅拷贝 vs 深拷贝
section("5. 浅拷贝 vs 深拷贝（想真正『复制一份』时怎么办）")

original = [[1, 2], [3, 4]]

shallow = copy.copy(original)    # 浅拷贝：只复制最外层
deep = copy.deepcopy(original)   # 深拷贝：递归复制所有层

print("original =", original)
print()
print("浅拷贝 shallow 是独立的外层列表，但内层列表仍是共享的：")
print("  shallow is original ?", shallow is original)              # False（外层不同）
print("  shallow[0] is original[0] ?", shallow[0] is original[0])  # True（内层共享！）

shallow[0].append(999)
print("  执行 shallow[0].append(999) 后：")
print("    original =", original)   # 被影响！
print("    shallow  =", shallow)

print()
print("深拷贝 deep 连内层也复制，互不影响：")
original2 = [[1, 2], [3, 4]]
deep2 = copy.deepcopy(original2)
print("  deep2 is original2 ?", deep2 is original2)              # False
print("  deep2[0] is original2[0] ?", deep2[0] is original2[0])  # False
deep2[0].append(999)
print("  执行 deep2[0].append(999) 后：")
print("    original2 =", original2)   # 不受影响
print("    deep2     =", deep2)

# 6. 函数传参：也是引用传递
section("6. 函数参数：传的也是引用")


def mutate(lst):
    lst.append("函数里加的")


def rebind(lst):
    lst = ["新的列表"]   # 只是把形参 lst 重新绑定，不影响调用方


data = [1, 2]
mutate(data)
print("mutate(data) 后 data =", data)   # 变了：函数拿到了原对象的引用

data = [1, 2]
rebind(data)
print("rebind(data) 后 data =", data)   # 没变：函数里只是重新绑定局部名字
print()
print("含义：函数能『修改』传入的可变对象，但无法『替换』调用方持有的引用。")

section("小结")
print("1. 变量 = 名字 + 引用，不是数据的容器。")
print("2. 赋值 b = a 复制的是『引用』，不是对象。")
print("3. 可变对象可原地改（影响所有引用者），不可变对象只能重新绑定。")
print("4. is 比较身份（同一对象），== 比较值。")
print("5. 想真正复制：浅拷贝 copy.copy，深拷贝 copy.deepcopy。")
