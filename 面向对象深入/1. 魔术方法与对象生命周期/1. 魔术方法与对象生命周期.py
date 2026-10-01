# -*- coding: utf-8 -*-
"""
1. 魔术方法与对象生命周期 —— 可运行演示脚本
============================================

核心认知：

    魔术方法（Magic Methods / Dunder Methods）就是 Python 给对象定义的
    「协议接口」。你实现这些方法，Python 在特定场景会自动调用它们。

        class User:
            def __str__(self):
                return self.name

        print(user)         # 你没有调用 user.__str__()
                            # 但 Python 自动执行了 user.__str__()

    对象的一生：__new__ 创建 -> __init__ 初始化 -> 使用（str/repr/call）
              -> __enter__/__exit__ 收尾 -> __del__ 销毁。

运行：python "1. 魔术方法与对象生命周期.py"
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


# 1. 魔术方法 = 协议接口
section("1. 魔术方法 = 协议接口，Python 自动调用")


class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


user = User("Tom")

print("我们没有写 user.__str__()，但 print(user) 会自动调用它：")
print("  print(user)  ->", end=" ")
print(user)
print()
print("因为 print 内部会做：str(user) -> user.__str__()")
print("这就是『协议接口』：你定义 __str__，print/str 就按协议调用它。")

# 2. __str__ 与 __repr__ 的区别
section("2. __str__（给用户看）与 __repr__（给开发者看）")


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"


p = Point(3, 4)
print("print(p)      ->", p)          # 用 __str__
print("str(p)        ->", str(p))      # 用 __str__
print("repr(p)       ->", repr(p))     # 用 __repr__
print("交互式/调试里  ->", repr(p))    # 开发者调试用 __repr__
print()
print("列表里显示元素时用的是 __repr__：")
print("  [p, p]       ->", [p, p])
print()
print("区别：__str__ 给人看（友好简洁），__repr__ 给开发者看（信息完整、可还原）。")
print("      只写一个的话，优先写 __repr__（__str__ 会回退到 __repr__）。")

# 3. 魔术方法的共同特征
section("3. 魔术方法的共同特征")

print("1. 名字固定：前后双下划线（dunder = double underscore）。")
print("2. 你负责『实现』，Python 负责『调用』，调用时机由协议决定。")
print("3. 几乎不手动调用（不写 user.__str__()），交给 Python 触发。")
print()
print("常见魔术方法一览：")
print("  __init__    初始化对象        -> User('Tom')")
print("  __str__     字符串表示        -> print(user)")
print("  __repr__    调试表示          -> repr(user)")
print("  __call__    让对象可调用      -> user()")
print("  __enter__/__exit__  上下文    -> with user:")
print("  __len__     长度              -> len(obj)")
print("  __add__     加法              -> a + b")

# 4. 对象生命周期全景
section("4. 对象生命周期全景")

print("一个对象的完整一生：")
print()
print("  User('Tom')         调用 __new__    -> 分配内存、创建对象")
print("       ↓")
print("                       调用 __init__   -> 初始化、填充数据")
print("       ↓")
print("  使用对象             print(user)  -> __str__")
print("                       user()      -> __call__")
print("                       with user   -> __enter__ / __exit__")
print("       ↓")
print("  引用计数归零         调用 __del__    -> 销毁对象")
print()
print("本主题后续小节将逐个展开：")
print("  * __new__ / __init__（第 2 节）")
print("  * __call__（第 3 节）")
print("  * __enter__ / __exit__（第 4 节）")
print("  * 属性访问协议（第 5 节）")
print("  * 运算符重载与容器协议（第 6 节）")

section("小结")
print("1. 魔术方法是对象与 Python 之间的「协议接口」。")
print("2. 你实现，Python 在特定场景自动调用。")
print("3. __str__ 给人看，__repr__ 给开发者看。")
print("4. 对象生命周期：new -> init -> 使用 -> 销毁。")
