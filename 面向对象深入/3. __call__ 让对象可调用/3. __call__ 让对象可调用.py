# -*- coding: utf-8 -*-
"""
3. __call__ 让对象可调用 —— 可运行演示脚本
===========================================

核心认知：

    函数能调用，对象也能调用——只要实现 __call__。

        def hello():
            print("hello")
        hello()               # 函数调用

        model = AI()
        model("你好")          # 对象调用！等价于 model.__call__("你好")

    __call__ 让「对象」变得像「函数」一样可调用，
    很多装饰器、中间件、可调用对象都是这么实现的。

运行：python "3. __call__ 让对象可调用.py"
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


# 1. 函数可调用，对象也可调用
section("1. 函数能调用，对象也能调用")


def hello():
    print("  函数调用：hello")


print("函数：")
hello()
print()


class AI:
    def __call__(self, text):
        print("  AI 处理:", text)


print("对象：")
model = AI()
model("你好")
print()
print("因为 model('你好') 等价于 model.__call__('你好')。")
print("实现 __call__ 后，对象就『函数化』了。")

# 2. callable 判断
section("2. 用 callable() 判断是否可调用")

print("callable(hello)     ->", callable(hello))     # 函数 -> True
print("callable(model)     ->", callable(model))     # 有 __call__ 的对象 -> True
print("callable('abc')     ->", callable("abc"))     # 字符串 -> False
print()
print("判断依据：对象有没有 __call__ 方法。")

# 3. 带状态的函数：__call__ 的优势
section("3. __call__ 的优势：可调用对象能『记住状态』")


class Counter:
    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        print(f"    第 {self.count} 次调用")
        return self.count


counter = Counter()
counter()
counter()
counter()
print()
print("普通函数每次调用都『失忆』，而带 __call__ 的对象能保存内部状态（count）。")
print("这就是『可调用对象』比纯函数强的地方。")

# 4. 装饰器：__call__ 的实战应用
section("4. 实战：用 __call__ 实现装饰器")


class Logger:
    def __call__(self, func):
        def wrapper():
            print("    [执行前] 记录日志")
            func()
            print("    [执行后] 记录日志")
        return wrapper


@Logger()
def say_hello():
    print("    hello")


print("执行 say_hello()：")
say_hello()
print()
print("原理拆解：")
print("  @Logger()")
print("  def say_hello(): ...")
print()
print("  等价于： say_hello = Logger()(say_hello)")
print("          1) Logger() 创建装饰器对象")
print("          2) 调用它的 __call__，传入 say_hello")
print("          3) __call__ 返回 wrapper，say_hello 变成 wrapper")
print()
print("所以之后 say_hello() 实际执行的是 wrapper()。")

section("小结")
print("1. __call__ 让对象像函数一样可调用。")
print("2. obj(x) 等价于 obj.__call__(x)。")
print("3. 可调用对象能保存状态，比纯函数更灵活。")
print("4. 装饰器是 __call__ 的经典应用：@Logger() 本质是调用 __call__。")
