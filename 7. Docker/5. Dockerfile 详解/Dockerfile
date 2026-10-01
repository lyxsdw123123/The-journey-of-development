# 一个 FastAPI 应用的 Dockerfile 示例
FROM python:3.12

WORKDIR /app

# 先复制依赖清单，利用 Docker 层缓存：只改代码时不重装依赖
COPY requirements.txt .

RUN pip install -r requirements.txt

# 再复制项目代码
COPY . .

# 监听 0.0.0.0（而非 127.0.0.1），外部才能访问到容器里的服务
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
