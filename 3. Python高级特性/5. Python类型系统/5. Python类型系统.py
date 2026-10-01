# -*- coding: utf-8 -*-
"""
5. Python 类型系统 —— 可运行演示脚本
====================================

核心认知：

    Python 是动态类型：a = 10 之后还能 a = "hello"。

    但工程项目需要「类型提示（Type Hint）」来提升可读性、可维护性，
    并让 FastAPI 等框架自动做参数解析、数据验证、生成 API 文档。

运行：python "5. Python类型系统.py"
"""
import sys
import typing
from dataclasses import dataclass

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. 动态类型
section("1. Python 是动态类型")

a = 10
print("a = 10      ->", a, type(a))
a = "hello"
print('a = "hello" ->', a, type(a))
print()
print("同一个变量 a，先存 int 再存 str，都不报错——这就是动态类型。")
print("灵活，但大型项目里容易出错：函数参数/返回值到底该是什么类型？")

# 2. 类型提示
section("2. 类型提示（Type Hint）")


def get_users() -> list[str]:   # 现代写法：返回字符串列表
    return ["Tom", "Jack"]


print("def get_users() -> list[str]:")
print("  返回:", get_users())
print()
print("意思：这个函数返回『字符串列表』。")
print()
print("传统写法（老项目常见）：")
print("  from typing import List")
print("  def get_users() -> List[str]: ...")
print("两者等价，Python 3.9+ 推荐直接用内置 list[str]。")

# 3. 用 get_type_hints 查看类型标注
section("3. 用 typing.get_type_hints 查看标注")


def add(a: int, b: int) -> int:
    return a + b


print("def add(a: int, b: int) -> int: ...")
print("类型标注：", typing.get_type_hints(add))
print()
print("类型提示只是『提示』，运行时并不强制（不会因为传错类型就报错）。")

# 4. 类型化数据模型：dataclass
section("4. 类型化数据模型：dataclass")


@dataclass
class User:
    name: str
    age: int


u = User("Tom", 20)
print("User 数据模型：", u)
print("  u.name =", u.name, " u.age =", u.age)
print()
print("用类型标注定义数据模型，字段和类型一目了然。")
print("FastAPI 用的 pydantic BaseModel 就是这种思路的强化版。")

# 5. FastAPI 为什么依赖类型
section("5. FastAPI 为什么依赖类型（pydantic）")

print("FastAPI 代码：")
print()
print('  from pydantic import BaseModel')
print()
print('  class User(BaseModel):')
print('      name: str')
print('      age: int')
print()
print('  @app.post("/user")')
print('  def create_user(user: User):')
print('      return user')
print()
print("FastAPI 借助类型自动做三件事：")
print("  1. 参数解析：把 JSON 转换成 User 对象")
print('     {"name": "Tom", "age": 20}  ->  User(name="Tom", age=20)')
print("  2. 数据验证：类型不对自动报错")
print('     {"name": "Tom", "age": "abc"}  ->  报错（age 应是 int）')
print("  3. 自动生成 API 文档：Swagger /docs")
print("     自动出现 User 的 name:string、age:int")

section("小结")
print("1. Python 动态类型：灵活但工程上需要类型提示。")
print("2. 类型提示：-> list[str] 说明返回类型，提升可读性。")
print("3. 类型提示不强制，但 FastAPI/pydantic 用它做解析、验证、文档。")
print("4. 数据模型用 dataclass / pydantic 定义字段和类型。")
