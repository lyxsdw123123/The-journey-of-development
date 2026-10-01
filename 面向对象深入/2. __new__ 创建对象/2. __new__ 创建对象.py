# -*- coding: utf-8 -*-
"""
2. __new__ 创建对象 —— 可运行演示脚本
======================================

核心认知：

    很多人以为「对象创建 = __init__」，其实真正的流程是：

        User()
          ↓
        __new__(cls)     真正分配内存、创建对象
          ↓
        创建对象
          ↓
        __init__(self)   给已存在的对象填充数据
          ↓
        初始化完成

    __new__ 负责「造出对象」，__init__ 负责「填充对象」。
    普通开发很少重写 __new__，但单例模式等高级场景会用到。

运行：python "2. __new__ 创建对象.py"
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


# 1. __new__ 与 __init__ 的执行顺序
section("1. __new__ 与 __init__ 的执行顺序")


class User:
    def __new__(cls):
        print("  1) __new__ 被调用：分配内存、创建对象")
        obj = super().__new__(cls)   # 真正分配内存
        return obj                    # 必须返回这个对象！

    def __init__(self):
        print("  2) __init__ 被调用：初始化对象")


print("执行 user = User()：")
user = User()
print()
print("顺序永远是：__new__ 先创建 -> __init__ 再初始化。")

# 2. __new__ 与 __init__ 的分工
section("2. __new__ 与 __init__ 的分工")

print("__new__ 负责：创建内存中的那个对象（分配内存）。")
print("              -> obj = super().__new__(cls)")
print("              -> 参数是 cls（类本身），返回值是实例。")
print()
print("__init__ 负责：给已存在的对象填充数据（初始化）。")
print("              -> 参数是 self（已创建的对象），无返回值（默认 None）。")
print()
print("对应关系：")
print("  user = User('Tom')")
print("    1. User.__new__(User)      创建对象（没名字）")
print("    2. User.__init__(实例,'Tom')  填充数据 -> self.name = 'Tom'")
print("    3. 把实例绑定给 user")

# 3. 为什么很少重写 __new__
section("3. 为什么普通开发很少重写 __new__")

print("1. 默认 __new__ 已经够用：object.__new__ 自动分配内存。")
print("2. 直接重写 __init__ 就能满足绝大多数初始化需求。")
print("3. 重写 __new__ 需要理解 cls/self、返回值，出错容易踩坑。")
print()
print("但高级场景会用到 __new__：单例模式、不可变类型定制、元类等。")

# 4. 单例模式：数据库连接池
section("4. 单例模式：__new__ 的经典应用")


class Database:
    instance = None   # 类属性：保存唯一实例

    def __new__(cls):
        if cls.instance is None:
            print("    第一次：创建唯一的 Database 实例")
            cls.instance = super().__new__(cls)
        else:
            print("    已存在：直接返回同一个实例")
        return cls.instance

    def connect(self):
        return "已连接数据库"


print("创建 db1 = Database()：")
db1 = Database()
print("创建 db2 = Database()：")
db2 = Database()
print()
print("db1 is db2 ?", db1 is db2)
print()
print("db1 和 db2 指向同一个对象 —— 全局只有一个 Database 实例。")
print("这正是数据库连接池、全局配置、日志器等场景想要的『单例』。")
print()
print("db1.connect() ->", db1.connect())
print("db2.connect() ->", db2.connect())

section("小结")
print("1. 对象创建 = __new__（分配内存）+ __init__（填充数据）。")
print("2. __new__ 参数是 cls，返回实例；__init__ 参数是 self，返回 None。")
print("3. 普通开发重写 __init__ 即可，__new__ 用于单例等高级场景。")
print("4. 单例：__new__ 里保证只创建一个实例并复用。")
