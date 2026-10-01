# -*- coding: utf-8 -*-
"""
4. Network 网络 —— 可运行讲解脚本
==================================

核心认知：

    多个容器之间需要通信。Docker Network 让容器互相访问。

    FastAPI 访问 PostgreSQL，不是写 localhost，而是写服务名 db：

        FastAPI -> PostgreSQL（服务名 db）
        FastAPI -> Redis（服务名 redis）

    本脚本展示配置，无需本机安装 Docker。

运行：python "4. Network 网络.py"
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


# 1. 多容器需要通信
section("1. 多容器需要通信")

print("真实后端有多个容器：")
print()
print("  FastAPI")
print("    │")
print("    ├──── PostgreSQL")
print("    │")
print("    └──── Redis")
print()
print("Docker Network 让这些容器在同一网络里互相访问。")

# 2. 服务名代替 localhost
section("2. 用服务名代替 localhost")

print("FastAPI 访问数据库，不写 localhost，而是写服务名 db：")
print()
print("  错误：DATABASE_URL = postgresql://user:pwd@localhost:5432/app")
print("  正确：DATABASE_URL = postgresql://user:pwd@db:5432/app")
print()
print("因为 compose 里：")
print("""  services:
    api:
      ...
    db:
      image: postgres""")
print()
print("在同一 compose 网络里，『db』就是 PostgreSQL 容器的服务名。")

# 3. 完整例子
section("3. 完整例子：FastAPI 连 db 和 redis")

yaml_example = """services:
  api:
    build: .
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/app
      REDIS_URL: redis://redis:6379

  db:
    image: postgres:17

  redis:
    image: redis:latest
"""
print(yaml_example)
print("FastAPI 的 DATABASE_URL 里写 @db，REDIS_URL 里写 @redis，")
print("它们会通过 Docker 网络自动解析成对应容器的地址。")

# 4. 关键点
section("4. 关键点")

print("1. 容器间通信用『服务名』，不是 localhost。")
print("2. localhost 在容器里指向『容器自己』，不是宿主机。")
print("3. compose 会自动创建一个网络，把 services 都连进去。")
print("4. 这是写 DATABASE_URL / REDIS_URL 时非常重要的概念。")

section("小结")
print("1. Docker Network 让容器互相访问。")
print("2. 容器间用服务名（db/redis）通信，不是 localhost。")
print("3. compose 自动建网络，连接所有 services。")
