# -*- coding: utf-8 -*-
"""
7. 完整实战项目 —— 可运行讲解脚本
==================================

核心认知：

    最终目标：把 FastAPI + PostgreSQL + Redis + Nginx 全部容器化，
    一条命令 docker compose up -d 启动完整后端。

    本脚本展示完整项目结构与配置，无需本机安装 Docker。

运行：python "7. 完整实战项目.py"
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


# 1. 项目结构
section("1. 最终项目结构")

print("""backend/
├── app/
│   ├── main.py
│   ├── routers/
│   ├── models/
│   ├── services/
│   └── database/
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
└── .env""")
print()
print(".dockerignore 告诉 Docker 哪些文件不复制进镜像（如 .git、__pycache__）。")
print(".env 存放敏感配置（数据库密码等），不进 git。")

# 2. 完整 compose.yaml（含 Nginx）
section("2. 完整 compose.yaml（FastAPI + PostgreSQL + Redis + Nginx）")

yaml = """services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    depends_on:
      - api

  api:
    build: .
    expose:
      - "8000"
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/app
      REDIS_URL: redis://redis:6379

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
print("架构：")
print("  Nginx（80 端口，反向代理）-> FastAPI（8000）-> PostgreSQL / Redis")

# 3. 一条命令启动
section("3. 一条命令启动整个系统")

print("docker compose up -d")
print()
print("启动后：")
print("  Nginx -> FastAPI -> PostgreSQL")
print("  FastAPI -> Redis")
print()
print("查看状态：")
print("  docker compose ps")
print("  会看到 api / db / redis / nginx 全部运行。")

# 4. 请求链路
section("4. 完整请求链路（容器化后）")

print("浏览器")
print("  ↓ :80")
print("Nginx（反向代理）")
print("  ↓ 转发到 api:8000")
print("FastAPI 容器")
print("  ↓ db:5432          ↓ redis:6379")
print("PostgreSQL           Redis")

section("小结")
print("1. 项目结构：app/ + Dockerfile + compose.yaml + .dockerignore + .env。")
print("2. compose 编排 nginx + api + db + redis 四个服务。")
print("3. docker compose up -d 一键启动，docker compose ps 查看状态。")
