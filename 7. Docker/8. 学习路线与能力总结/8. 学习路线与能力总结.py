# -*- coding: utf-8 -*-
"""
8. 学习路线与能力总结 —— 可运行讲解脚本
========================================

核心认知：

    学完 Docker，你的 Python 后端能力就串起来了：

        Python -> asyncio -> SQL -> PostgreSQL -> FastAPI -> FastAPI源码 -> Docker
        -> FastAPI/PostgreSQL/Redis -> Nginx -> 后端部署

    你不再是「会调用 FastAPI 的学生」，而是
    「能理解 Python 后端运行机制，并独立构建、部署后端系统的开发者」。

运行：python "8. 学习路线与能力总结.py"
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


# 1. Docker 学习顺序
section("1. Docker 学习顺序")

steps = [
    "Docker",
    "① Image",
    "② Container",
    "③ docker run",
    "④ Dockerfile",
    "⑤ Port（端口映射）",
    "⑥ Volume",
    "⑦ Network",
    "⑧ Docker Compose",
    "⑨ FastAPI + PostgreSQL + Redis",
    "⑩ Nginx",
    "完整后端部署",
]
for i, s in enumerate(steps):
    indent = "  " * (0 if i == 0 else 1)
    print(indent + s)

# 2. 完整后端能力链
section("2. 你的完整后端能力链")

chain = """Python
  │
  ├── Python运行机制
  ├── OOP / 魔术方法
  ├── 装饰器 / 生成器
  └── 异常 / 类型 / 工程规范
        ↓
    asyncio
        ↓
     SQL
        ↓
  PostgreSQL
        ↓
    FastAPI
        ↓
  FastAPI源码
        ↓
     Docker
        ↓
 ┌──────┼──────┐
 ↓      ↓      ↓
FastAPI PostgreSQL Redis
 └──────┼──────┘
        ↓
      Nginx
        ↓
    后端部署"""
print(chain)

# 3. 身份的转变
section("3. 身份的转变")

print("之前：『会调用 FastAPI 的 Python 学生』")
print()
print("之后：『能理解 Python 后端运行机制，")
print("        并独立构建、部署后端系统的开发者』")
print()
print("你前面学的 asyncio + FastAPI源码 + SQL/PostgreSQL + Docker，")
print("正好是一条非常完整的 Python 后端进阶路线。")

section("小结")
print("1. Docker 学习顺序：Image -> Container -> Dockerfile -> Compose -> 实战。")
print("2. 能力链：Python -> asyncio -> SQL -> FastAPI -> Docker -> 部署。")
print("3. 终点：能独立构建、部署后端系统的开发者。")
