# -*- coding: utf-8 -*-
"""
6. Docker Compose 多容器编排 —— 可运行讲解脚本
================================================

核心认知：

    一个 FastAPI 用 Dockerfile 就够；真实后端（FastAPI + PostgreSQL + Redis + Nginx）
    需要 Docker Compose 同时管理多个容器。

    一条命令 docker compose up，全部一起启动。

    本脚本展示配置，无需本机安装 Docker。

运行：python "6. Docker Compose 多容器编排.py"
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


# 1. 为什么需要 Compose
section("1. 为什么需要 Compose")

print("单容器：Dockerfile 就够。")
print("多容器：FastAPI + PostgreSQL + Redis + Nginx，需要统一编排。")
print()
print("Docker Compose 负责：同时管理多个容器。")

# 2. 完整 compose.yaml
section("2. 完整 compose.yaml")

yaml = """services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  db:
    image: postgres:17
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:latest

volumes:
  postgres_data:
"""
print(yaml)

# 3. 逐字段解释
section("3. 逐字段解释")

print("services          定义所有服务（容器）")
print("  api              第一个服务：FastAPI 应用")
print("    build: .       用当前目录的 Dockerfile 构建镜像")
print("    ports          端口映射 宿主机:容器 = 8000:8000")
print("    depends_on     依赖 db 和 redis（先启动它们）")
print("  db               PostgreSQL 服务")
print("    image          直接用官方 postgres:17 镜像")
print("    environment    环境变量（数据库名/用户/密码）")
print("    volumes        数据卷挂载（持久化数据）")
print("  redis            Redis 服务")
print("volumes           声明命名数据卷 postgres_data")
print()
print("启动：docker compose up   ->  api + db + redis 一起启动。")

# 4. 常用 compose 命令
section("4. 常用 compose 命令")

print("docker compose up          前台启动（看日志）")
print("docker compose up -d       后台启动")
print("docker compose down        停止并删除容器")
print("docker compose ps          查看服务状态")
print("docker compose logs -f     跟踪日志")
print("docker compose build       重新构建镜像")

section("小结")
print("1. Compose 用一个 YAML 描述多容器应用。")
print("2. services/build/image/ports/environment/depends_on/volumes 各司其职。")
print("3. docker compose up 一键启动整个后端。")
