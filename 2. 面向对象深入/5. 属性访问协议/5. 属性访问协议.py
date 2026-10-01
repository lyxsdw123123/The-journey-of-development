# -*- coding: utf-8 -*-
"""
5. 属性访问协议 —— 可运行演示脚本
==================================

核心认知：

    访问对象的属性，其实也是「协议」：user.name 实际上会触发
    user.__getattribute__("name")。

        __getattribute__  每次访问属性都会调用（先执行）
        __getattr__       只有属性「找不到」时才调用（兜底）
        __setattr__       每次设置属性都会调用
        __delattr__       删除属性时调用

    框架（ORM、序列化、代理对象）大量使用这些方法做拦截和懒加载。

运行：python "5. 属性访问协议.py"
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


# 1. 属性访问也是协议
section("1. 属性访问也是协议")

print("user.name 实际上会触发 user.__getattribute__('name')。")
print("Python 属性访问的四个钩子：")
print("  __getattribute__  每次访问属性都调用（先执行）")
print("  __getattr__       属性找不到时才调用（兜底）")
print("  __setattr__       每次设置属性都调用")
print("  __delattr__       删除属性时调用")

# 2. __getattr__：找不到时的兜底
section("2. __getattr__：属性不存在时才调用")


class LazyUser:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        # 只有访问「不存在的属性」才会走到这里
        print(f"    [__getattr__] 属性 {item!r} 不存在，返回默认值")
        return f"默认_{item}"


u = LazyUser("Tom")
print("u.name ->", u.name)       # 存在，不触发 __getattr__
print("u.age  ->", u.age)        # 不存在，触发 __getattr__
print("u.email->", u.email)      # 不存在，触发 __getattr__

# 3. __setattr__：每次赋值都调用
section("3. __setattr__：每次设置属性都调用")


class Logged:
    def __init__(self, name):
        self.name = name   # 这行也会触发 __setattr__

    def __setattr__(self, key, value):
        print(f"    [__setattr__] 设置 {key} = {value!r}")
        super().__setattr__(key, value)   # 关键：真正写入，避免递归


print("创建 obj = Logged('Tom')：")
obj = Logged("Tom")
print()
print("执行 obj.age = 18：")
obj.age = 18
print()
print("注意：__setattr__ 里必须用 super().__setattr__ 真正写入，")
print("      否则 self.xxx = ... 会无限递归调用自己。")

# 4. __getattribute__：每次访问都调用（最底层）
section("4. __getattribute__：每次访问都调用")


class Traced:
    def __init__(self, name):
        super().__setattr__("name", name)   # 直接写入，避免干扰演示

    def __getattribute__(self, item):
        print(f"    [__getattribute__] 访问 {item}")
        return super().__getattribute__(item)   # 关键：真正取值


t = Traced("Tom")
print("访问 t.name：")
print("  ->", t.name)
print()
print("注意：__getattribute__ 是最底层的钩子，每次访问都会经过它；")
print("      实现时必须用 super().__getattribute__ 真正取值，否则递归。")

# 5. __getattr__ 与 __getattribute__ 的区别（重点）
section("5. __getattr__ 与 __getattribute__ 的区别（重点）")

print("调用顺序：")
print("  1. 先调用 __getattribute__（每次都调用）")
print("  2. 若它抛 AttributeError（属性不存在），再调用 __getattr__（兜底）")
print()
print("对比表：")
print("  __getattribute__  每次访问都触发，用于『监控所有访问』")
print("  __getattr__       仅在属性缺失时触发，用于『懒加载/默认值』")

section("小结")
print("1. 属性访问是协议：user.name -> user.__getattribute__('name')。")
print("2. __getattr__ 兜底（属性缺失才调用），__getattribute__ 全拦截。")
print("3. __setattr__ / __delattr__ 拦截设置和删除。")
print("4. 重写这些方法时，务必用 super().__xxx__ 真正读写，避免无限递归。")
