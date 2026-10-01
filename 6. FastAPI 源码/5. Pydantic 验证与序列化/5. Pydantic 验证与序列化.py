# -*- coding: utf-8 -*-
"""
5. Pydantic 验证与序列化 —— 可运行演示脚本
==========================================

核心认知：

    请求进来：HTTP JSON -> Python 数据 -> Pydantic Model -> Validation -> Python 对象
    响应出去：Python 对象 -> Pydantic -> Serialization -> JSON -> HTTP Response

    三个关键词：

        Model        class User(BaseModel): name: str; age: int
        Validation   User(name="Tom", age="18") -> 自动转成 int 18、校验
        Serialization  user.model_dump() / user.model_dump_json()

运行：python "5. Pydantic 验证与序列化.py"
"""
import sys
from pydantic import BaseModel, ValidationError

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. Model
section("1. Model：定义数据模型")


class User(BaseModel):
    name: str
    age: int


print("class User(BaseModel):")
print("    name: str")
print("    age: int")
print("字段和类型一目了然。")

# 2. Validation
section("2. Validation：数据处理和校验")

u = User(name="Tom", age="18")   # 注意 age 传的是字符串 "18"
print("User(name='Tom', age='18') ->", u)
print("  age 的类型：", type(u.age).__name__, "（字符串被自动转成 int）")
print()
print("传非法值会报错：")
try:
    User(name="Tom", age="abc")
except ValidationError as e:
    print("  ValidationError:", e.errors()[0]["msg"])

# 3. Serialization
section("3. Serialization：序列化")

print("Python 对象 -> dict：")
print("  ", u.model_dump())
print()
print("Python 对象 -> JSON 字符串：")
print("  ", u.model_dump_json())
print()
print("理解这个过程：Python 对象 -> dict -> JSON。")

# 4. 完整数据流
section("4. 完整数据流")

print("请求进来：")
print("  HTTP JSON -> Python 数据 -> Pydantic Model -> Validation -> Python 对象")
print()
print("响应出去：")
print("  Python 对象 -> Pydantic -> Serialization -> JSON -> HTTP Response")

section("小结")
print("1. Model：用 BaseModel + 类型注解定义数据结构。")
print("2. Validation：自动类型转换 + 校验（age='18' 转 int）。")
print("3. Serialization：model_dump() 转 dict，model_dump_json() 转 JSON。")
print("4. FastAPI 靠 pydantic 做请求解析和响应序列化。")
