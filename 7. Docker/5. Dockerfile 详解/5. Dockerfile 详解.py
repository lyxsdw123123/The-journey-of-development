# -*- coding: utf-8 -*-
"""
5. Dockerfile 详解 —— 可运行讲解脚本
====================================

核心认知：

    Dockerfile 告诉 Docker：「如何构建我的 Python 应用镜像」。

    FROM     基础镜像
    WORKDIR  容器内工作目录
    COPY     复制文件进容器
    RUN      构建时执行命令（装依赖）
    CMD      容器启动时执行的命令

    本脚本展示配置，无需本机安装 Docker。

运行：python "5. Dockerfile 详解.py"
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
section("1. 一个 FastAPI 项目 + Dockerfile")

print("""my_project/
├── main.py
├── requirements.txt
└── Dockerfile""")
print()

# 2. 完整 Dockerfile
section("2. 完整 Dockerfile")

dockerfile = """FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
print(dockerfile)
print("下面逐行解释。")

# 3. 逐行解释
section("3. 逐行解释")

print("FROM python:3.12")
print("  从 Python 3.12 镜像开始构建（基础环境）。")
print()
print("WORKDIR /app")
print("  设置容器内工作目录为 /app，之后的 COPY/RUN/CMD 都在这里执行。")
print()
print("COPY requirements.txt .")
print("  把本地的 requirements.txt 复制到容器的 /app/。")
print()
print("RUN pip install -r requirements.txt")
print("  构建时执行：安装依赖（结果固化进镜像）。")
print()
print("COPY . .")
print("  把项目代码复制进容器的 /app/。")
print()
print('CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]')
print("  容器启动时执行：跑 uvicorn 启动 FastAPI。")

# 4. 0.0.0.0 vs 127.0.0.1
section("4. 为什么是 0.0.0.0 而不是 127.0.0.1")

print("127.0.0.1  只监听本机（容器内部），宿主机访问不到。")
print("0.0.0.0   监听所有网络接口，允许外部（宿主机/其他容器）访问。")
print()
print("容器是隔离环境，必须监听 0.0.0.0，")
print("外部才能通过端口映射访问到容器里的 FastAPI。")

# 5. COPY 顺序的讲究
section("5. COPY 顺序的讲究（缓存优化）")

print("先 COPY requirements.txt，再 COPY . .：")
print("  * 依赖文件变化少，依赖安装层可被 Docker 缓存复用。")
print("  * 只改代码时，pip install 不会重跑，构建更快。")
print()
print("如果反过来（先 COPY . . 再 RUN pip install），")
print("  代码一变，pip install 就得重新执行。")

section("小结")
print("1. Dockerfile 描述如何构建应用镜像。")
print("2. FROM/WORKDIR/COPY/RUN/CMD 各司其职。")
print("3. 容器要监听 0.0.0.0，外部才能访问。")
print("4. COPY 顺序影响构建缓存效率。")
