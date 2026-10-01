# -*- coding: utf-8 -*-
"""
2. Image 与 Container —— 可运行讲解脚本
========================================

核心认知：

    Docker 最重要的基础概念之一：区分「镜像」和「容器」。

        Image（镜像）   = 打包好的运行环境模板（不是正在运行的程序）
        Container（容器）= 镜像运行起来之后的实例

    关系：

        Image -> 运行 -> Container

    本脚本展示命令，无需本机安装 Docker。

运行：python "2. Image 与 Container.py"
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


# 1. Image 镜像
section("1. Image：环境模板")

print("Image 可以理解成：一个已经打包好的『运行环境模板』。")
print()
print("常见镜像：")
print("  python:3.12      Python 3.12 环境")
print("  postgres:17      PostgreSQL 17")
print("  redis:latest     Redis（最新版）")
print("  nginx:latest     Nginx")
print()
print("下载镜像：")
print("  docker pull python:3.12")
print()
print("注意：镜像本身不是正在运行的程序，只是一个『模板』。")

# 2. Container 容器
section("2. Container：镜像运行起来的实例")

print("Container 可以理解成：镜像运行起来之后的实例。")
print()
print("关系：")
print("  Image")
print("     ↓ 运行")
print("  Container")
print()
print("用 python:3.12 镜像创建容器：")
print("  docker run python:3.12")
print()
print("同一个镜像可以运行出多个容器实例。")

# 3. 类比理解
section("3. 类比：类与对象")

print("Image 和 Container 的关系，就像『类』和『对象』：")
print("  Image（镜像）   ≈ 类 class       —— 模板")
print("  Container（容器）≈ 对象 instance  —— 实例")
print()
print("或者：")
print("  Image      = 菜谱（模板）")
print("  Container  = 按菜谱做出来的一盘菜（实例）")
print()
print("一个菜谱可以做很多盘菜；一个镜像可以跑很多个容器。")

# 4. 常用命令
section("4. 常用命令")

print("docker images          查看本地镜像列表")
print("docker pull <镜像>      下载镜像")
print("docker run <镜像>       运行容器")
print("docker ps              查看运行中的容器")
print("docker ps -a           查看所有容器（含已停止）")
print("docker rm <容器>        删除容器")
print("docker rmi <镜像>       删除镜像")

section("小结")
print("1. Image = 模板；Container = 实例。")
print("2. 关系：Image -> 运行 -> Container。")
print("3. 一个镜像可以运行多个容器（类与对象的关系）。")
