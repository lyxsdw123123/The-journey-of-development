# -*- coding: utf-8 -*-
"""
1. 为什么需要 Docker —— 可运行讲解脚本
======================================

核心认知：

    没有 Docker，换一台电脑就要重新装一遍环境（Python/PostgreSQL/Redis/Nginx...）。
    Docker 的思想：把「运行环境」也变成「项目的一部分」。

    最终目标：拿到一个 Python 后端项目，能自己把它容器化，
    并用一条命令（docker compose up）启动整个系统。

    本脚本展示命令与配置，无需本机安装 Docker。

运行：python "1. 为什么需要 Docker.py"
"""
import sys
import shutil

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


if shutil.which("docker"):
    print("本机已安装 Docker。")
else:
    print("本机未安装 Docker（本脚本为讲解式，展示命令与配置，可直接阅读）。")

# 1. 没有 Docker 的痛点
section("1. 没有 Docker 时的安装地狱")

print("换一台新电脑，部署一个 FastAPI + PostgreSQL + Redis 后端，你需要：")
steps = [
    "安装 Python",
    "创建虚拟环境",
    "pip install 依赖",
    "安装 PostgreSQL",
    "配置 PostgreSQL",
    "安装 Redis",
    "配置 Redis",
    "安装 Nginx",
    "配置环境变量",
    "启动 FastAPI",
]
for i, s in enumerate(steps, 1):
    print(f"  {i:>2}. {s}")
print()
print("换一台电脑，又得重新来一遍，还容易版本不一致、环境打架。")

# 2. Docker 的思想
section("2. Docker 的思想：环境也是项目的一部分")

print("Docker 把整个运行环境都描述出来：")
print()
print("  项目")
print("  ├── Python")
print("  ├── FastAPI")
print("  ├── PostgreSQL")
print("  ├── Redis")
print("  ├── Nginx")
print("  └── 配置")
print()
print("全部通过 Dockerfile / compose.yaml 描述，任何机器一条命令复现。")

# 3. 最终架构
section("3. 最终目标架构")

print("""                    ┌──────────────┐
                    │    Nginx     │
                    │  反向代理     │
                    └──────┬───────┘
                           │
                           ↓
                    ┌──────────────┐
                    │   FastAPI    │
                    │     API      │
                    └───┬──────┬───┘
                        │      │
              ┌─────────┘      └─────────┐
              ↓                           ↓
       ┌──────────────┐           ┌──────────────┐
       │ PostgreSQL   │           │    Redis     │
       │    数据库     │           │    缓存       │
       └──────────────┘           └──────────────┘""")
print()
print("一条命令启动整个后端环境：")
print("  docker compose up")

section("小结")
print("1. 没有 Docker：环境安装繁琐、易不一致。")
print("2. Docker：环境也是项目的一部分，可描述、可复现。")
print("3. 最终目标：一条命令 docker compose up 启动整个后端。")
