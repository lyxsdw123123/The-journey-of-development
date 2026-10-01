# -*- coding: utf-8 -*-
"""
3. Volume 数据卷 —— 可运行讲解脚本
==================================

核心认知：

    Volume（数据卷）特别重要——它让「数据独立于容器生命周期存在」。

    问题：PostgreSQL 在容器里，docker rm 删除容器后，数据就没了。
    解决：把数据存到 Volume，容器删了，数据还在。

        Container -> Volume -> 数据

    本脚本展示配置，无需本机安装 Docker。

运行：python "3. Volume 数据卷.py"
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


# 1. 问题：容器删除数据就没了
section("1. 问题：容器删了，数据怎么办")

print("PostgreSQL 跑在容器里：")
print("  PostgreSQL Container")
print("      ↓")
print("    数据库（数据存在容器里）")
print()
print("如果执行：")
print("  docker rm postgres")
print("  数据库数据也一起没了！")
print()
print("数据库、用户上传的文件、日志等，都不能随容器一起消失。")

# 2. 解决：Volume
section("2. 解决：Volume 数据卷")

print("把数据存到 Volume（独立于容器的存储）：")
print()
print("  Container")
print("     ↓")
print("  Volume（数据卷，独立存储）")
print("     ↓")
print("  数据")
print()
print("容器删除后，Volume 还在，数据得以保留。")

# 3. compose.yaml 里的 Volume
section("3. compose.yaml 里的 Volume 配置")

yaml_example = """volumes:
  postgres_data:

services:
  db:
    image: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
"""
print(yaml_example)
print("解读：")
print("  postgres_data                      声明一个命名数据卷")
print("  /var/lib/postgresql/data           容器内 PG 存放数据的位置")
print("  - postgres_data:/var/lib/postgresql/data  把这个目录映射到数据卷")
print()
print("这样即使 docker compose down 删掉容器，postgres_data 卷里的数据还在。")

section("小结")
print("1. 容器是临时的，数据不能随容器一起消失。")
print("2. Volume 让数据独立于容器生命周期存在。")
print("3. compose 里用 volumes 声明并把容器目录映射到数据卷。")
