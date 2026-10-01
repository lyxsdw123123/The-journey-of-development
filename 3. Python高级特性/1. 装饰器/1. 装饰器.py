# -*- coding: utf-8 -*-
"""
1. 装饰器（Decorator）—— 可运行演示脚本
========================================

核心认知：

    装饰器就是在「不修改原函数代码」的前提下，给函数增加额外功能。

        @log
        def hello():
            print("hello")

    实际上等价于：

        hello = log(hello)

    FastAPI 里的 @app.get("/users") 也是一样：
        get_users = app.get("/users")(get_users)

运行：python "1. 装饰器.py"
"""
import sys
import time
import functools

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. 手写一个最简单的装饰器
section("1. 手写一个简单装饰器：@log")


def log(func):
    def wrapper():
        print("    开始执行")
        func()
        print("    执行结束")
    return wrapper


@log
def hello():
    print("    hello")


print("调用 hello()：")
hello()
print()
print("等价关系：@log 写在 hello 上，等价于 hello = log(hello)。")
print("log 接收原函数，返回包装后的 wrapper，之后调用的是 wrapper。")

# 2. 装饰器支持参数和返回值
section("2. 装饰器支持参数和返回值（*args, **kwargs）")


def log2(func):
    @functools.wraps(func)   # 保留原函数的元信息（名字、文档等）
    def wrapper(*args, **kwargs):
        print(f"    调用 {func.__name__}{args}")
        result = func(*args, **kwargs)
        print(f"    返回 {result!r}")
        return result
    return wrapper


@log2
def add(a, b):
    return a + b


print("调用 add(1, 2)：")
print("  add(1, 2) =", add(1, 2))

# 3. 计时装饰器 @timer
section("3. 实战：@timer 计时装饰器")


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        dt = time.perf_counter() - t0
        print(f"    [{func.__name__}] 耗时 {dt:.4f} 秒")
        return result
    return wrapper


@timer
def train_model():
    time.sleep(0.5)   # 模拟模型训练
    return "训练完成"


train_model()
print()
print("后端大量用 @timer 统计耗时，比如：模型训练耗时 30 秒。")

# 4. FastAPI 的 @app.get("/users")
section("4. FastAPI 的 @app.get('/users') 是什么")

print("代码：")
print('  @app.get("/users")')
print('  def get_users():')
print('      return {"name": "Tom"}')
print()
print("FastAPI 实际做了：")
print('  handler = app.get("/users")   # 返回一个装饰器（handler）')
print('  get_users = handler(get_users)  # 把 get_users 注册进路由表')
print()
print("于是 FastAPI 内部保存了一张路由表：")
print("  GET /users  ->  get_users 函数")
print()
print("当浏览器访问 http://localhost:8000/users：")
print("  请求 -> 匹配路由 -> 执行 get_users() -> 返回 JSON")
print()
print("所以 @app.get 本质就是一个装饰器，用来『注册路由』。")

# 5. 后端常见装饰器场景
section("5. 后端常见装饰器场景")

print("1. 路由注册：")
print('   @app.get("/users")')
print()
print("2. 权限认证：")
print('   @login_required')
print('   def user_info(): ...')
print('      请求 -> 权限检查 -> 原函数')
print()
print("3. 日志：")
print('   @log')
print()
print("4. 计时：")
print('   @timer')
print()
print("共同点：都是『在不改原函数的前提下，包装一层通用逻辑』。")

section("小结")
print("1. 装饰器 = 不改原函数代码，给它加功能。")
print("2. @log 等价于 hello = log(hello)。")
print("3. wrapper 用 *args/**kwargs 透传参数，用 functools.wraps 保留元信息。")
print("4. FastAPI 的 @app.get 本质是装饰器，用于注册路由。")
