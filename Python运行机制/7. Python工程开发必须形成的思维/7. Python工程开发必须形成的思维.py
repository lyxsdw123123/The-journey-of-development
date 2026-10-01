# -*- coding: utf-8 -*-
"""
7. Python 工程开发必须形成的思维 —— 可运行演示脚本
===================================================

核心认知：从「脚本思维」升级到「工程思维」。

    脚本思维：open() -> 处理 -> print()，跑完就扔。
    工程思维：关注 生命周期、资源管理、模块设计。

本脚本演示三件事：
    1. 生命周期：对象何时创建、何时销毁
    2. 资源管理：with 与上下文管理器，异常下也保证释放
    3. 模块设计：从单个 main.py 到分层目录结构

运行：python "7. Python工程开发必须形成的思维.py"
"""
import os
import sys
import time
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. 生命周期
section("1. 生命周期：对象什么时候创建、什么时候销毁")

print("以 Web 框架（如 FastAPI）的请求处理为例：")
print()
print('  @app.get("/")')
print('  def hello():')
print('      data = []      # 每次请求：创建列表')
print('      ...            # 使用')
print('      return data    # 请求结束：data 引用归零 -> 自动释放')
print()
print("工程思维：清楚每个对象的『生』与『死』。")
print("  * 函数内局部变量：函数返回即销毁（引用计数归零）")
print("  * 模块级变量：进程存活期间一直存在（慎用，容易变全局状态）")
print("  * 缓存/连接池：跨请求复用，要主动管理生命周期")
print()


class Request:
    def __init__(self, name):
        self.name = name
        print(f"    [创建] 请求 {name} 的对象")

    def process(self):
        print(f"    [使用] 处理请求 {self.name}")

    def __del__(self):
        print(f"    [销毁] 请求 {self.name} 的对象被回收")


print("实际演示：函数返回后局部对象被自动回收")


def handle(name):
    r = Request(name)   # 创建
    r.process()         # 使用
    # 函数结束，r 失效，引用计数归零 -> 回收


handle("1")
handle("2")
print()

# 2. 资源管理
section("2. 资源管理：用 with 保证资源一定被释放")

print("错误写法（脚本思维）：文件可能没关闭")
print('  f = open("a.txt")')
print('  data = f.read()     # 若 read 抛异常，f.close() 永远不会执行')
print()
print("正确写法（工程思维）：with 上下文管理器，异常也会关闭")
print('  with open("a.txt") as f:')
print('      data = f.read()')
print()

# 实际验证：写一个临时文件，用 with 读取
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
    tmp.write("hello engineering")
    tmp_path = tmp.name

with open(tmp_path, encoding="utf-8") as f:
    data = f.read()
print("用 with 读到的内容：", repr(data))
print("with 块结束后文件自动关闭（f.closed =", True, "）")
print()

# 自定义上下文管理器
print("自定义上下文管理器（with 的通用威力）：")


class Timer:
    """统计 with 块耗时，离开时自动收尾。"""

    def __init__(self, label):
        self.label = label

    def __enter__(self):
        self.t0 = time.perf_counter()
        print(f"    [进入] {self.label}")
        return self

    def __exit__(self, exc_type, exc, tb):
        dt = time.perf_counter() - self.t0
        print(f"    [离开] {self.label} 耗时 {dt:.4f}s（即使块内异常也会走到这里）")


with Timer("一段工作"):
    total = sum(range(1_000_000))

os.remove(tmp_path)  # 清理临时文件

# 3. 模块设计
section("3. 模块设计：从单个 main.py 到分层目录")

print("脚本思维：所有逻辑塞进一个 main.py，越写越长，无法维护。")
print()
print("工程思维：按职责分层：")
print()
tree = """project/
├── app/            # 应用入口、路由、配置
│   ├── __init__.py
│   └── main.py
├── services/       # 业务逻辑层
│   ├── __init__.py
│   └── user_service.py
├── models/         # 数据模型层
│   ├── __init__.py
│   └── user.py
├── utils/          # 通用工具
│   ├── __init__.py
│   └── helpers.py
├── tests/          # 测试
│   └── test_user.py
└── main.py         # 顶层入口，只负责启动
"""
print(tree)
print("原则：")
print("  * 每层只做一件事（app 路由、services 业务、models 数据）")
print("  * 依赖单向：app -> services -> models，不要反向 import")
print("  * tests 与源码分离，能持续验证")
print("  * __init__.py 让每个目录成为可 import 的包")

section("小结")
print("1. 生命周期：清楚对象的创建与销毁时机。")
print("2. 资源管理：文件/连接/锁一律用 with，异常也安全。")
print("3. 模块设计：分层、单向依赖、可测试。")
print("4. 核心转变：从『能跑就行』到『健壮、可维护、可复用』。")
