# -*- coding: utf-8 -*-
"""
6. 运算符重载与容器协议 —— 可运行演示脚本
==========================================

核心认知：

    Python 里的运算符，本质也是「魔术方法」在背后支撑：

        a + b          ->  a.__add__(b)
        len(obj)       ->  obj.__len__()
        obj[0]         ->  obj.__getitem__(0)
        x in obj       ->  obj.__contains__(x)

    重写这些方法，就能让自定义对象支持 +、len()、[]、in 等操作，
    让对象用起来像「内置类型」一样自然。

运行：python "6. 运算符重载与容器协议.py"
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


# 1. 运算符 = 魔术方法
section("1. 运算符背后是魔术方法")


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


v1 = Vector(1, 2)
v2 = Vector(3, 4)
print("v1 =", v1)
print("v2 =", v2)
print("v1 + v2 =", v1 + v2)
print()
print("因为 v1 + v2 等价于 v1.__add__(v2)。")
print("重写 __add__ 后，+ 就能作用于我们的自定义对象。")

# 2. 比较运算符
section("2. 比较运算符：__eq__、__lt__ 等")


class Money:
    def __init__(self, amount):
        self.amount = amount

    def __eq__(self, other):
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __repr__(self):
        return f"Money({self.amount})"


m1 = Money(100)
m2 = Money(200)
m3 = Money(100)
print("m1 == m3 ?", m1 == m3)   # True
print("m1 < m2  ?", m1 < m2)    # True
print()
print("== 对应 __eq__，< 对应 __lt__，> <= >= 也都有对应方法。")

# 3. 容器协议
section("3. 容器协议：len、[]、in")


class Deck:
    def __init__(self):
        self.cards = ["A", "K", "Q"]

    def __len__(self):
        return len(self.cards)          # len(deck) -> deck.__len__()

    def __getitem__(self, index):
        return self.cards[index]        # deck[0]  -> deck.__getitem__(0)

    def __contains__(self, card):
        return card in self.cards       # 'A' in deck -> deck.__contains__('A')


deck = Deck()
print("len(deck)   ->", len(deck))      # 3
print("deck[0]     ->", deck[0])        # A
print("'A' in deck ->", "A" in deck)    # True
print("'9' in deck ->", "9" in deck)    # False
print()
print("重写这些方法后，自定义对象就能用 len()、[]、in 等语法。")

# 4. 常用运算符/协议速查
section("4. 常用运算符与协议速查")

print("运算符重载：")
print("  a + b   ->  __add__      a - b  ->  __sub__")
print("  a * b   ->  __mul__      a / b  ->  __truediv__")
print("  a == b  ->  __eq__       a < b  ->  __lt__")
print()
print("容器协议：")
print("  len(obj)    ->  __len__")
print("  obj[key]    ->  __getitem__")
print("  x in obj    ->  __contains__")
print("  for x in obj->  __iter__ / __next__")
print()
print("好处：自定义对象用起来像内置类型，代码更自然、可读。")

section("小结")
print("1. 运算符本质是魔术方法：a + b -> a.__add__(b)。")
print("2. 重写运算符方法，让自定义对象支持 +、==、< 等。")
print("3. 容器协议让对象支持 len()、[]、in。")
print("4. 这是写出『自然、可读』API 的关键。")
