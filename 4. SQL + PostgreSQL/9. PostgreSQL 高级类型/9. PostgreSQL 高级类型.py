# -*- coding: utf-8 -*-
"""
9. PostgreSQL 高级类型 —— 可运行演示脚本
========================================

核心认知：

    PostgreSQL 不只是存「数字和字符串」，还有适合后端的强大类型：

        JSONB   直接存 JSON，还能在数据库里查询 JSON 字段
        ARRAY   数组类型（如 TEXT[]、INTEGER[]）
        UUID    全局唯一标识符，后端 API 非常常见

    这些类型对 GIS / GeoAI 方向尤其有用。

运行：python "9. PostgreSQL 高级类型.py"
"""
import sys
import json
import uuid
import sqlite3

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. JSONB
section("1. JSONB：在数据库里存 JSON 并查询")

meta = {
    "model": "Qwen",
    "temperature": 0.7,
    "task": "geospatial_reasoning",
}
print("PostgreSQL 建表：")
print("  CREATE TABLE tasks (metadata JSONB);")
print()
print("存入的 JSON 结构：")
print("  ", json.dumps(meta, ensure_ascii=False))
print()
print("PostgreSQL 里直接查 JSON 字段：")
print("  SELECT * FROM tasks WHERE metadata->>'model' = 'Qwen';")
print("  SELECT * FROM tasks WHERE metadata @> '{\"task\": \"geospatial_reasoning\"}';")
print()
print("  ->> 取 JSON 字段的文本值；@> 判断是否包含某 JSON。")
print()

# 用 sqlite 的 json 函数做可运行类比
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE tasks (metadata TEXT)")
cur.execute("INSERT INTO tasks VALUES (?)", (json.dumps(meta),))
cur.execute("SELECT json_extract(metadata, '$.model') FROM tasks")
print("sqlite 类比（json_extract 相当于 PG 的 ->）：")
print("  取 metadata.model =", cur.fetchone()[0])

# 2. ARRAY
section("2. ARRAY：数组类型")

print("PostgreSQL 数组类型：")
print("  CREATE TABLE items (tags TEXT[]);")
print("  CREATE TABLE geo (embedding_ids INTEGER[]);")
print()
print("  存：INSERT INTO items (tags) VALUES (ARRAY['gis','ai','backend']);")
print("  查：SELECT * FROM items WHERE 'ai' = ANY(tags);")
print()
tags = ["gis", "ai", "backend"]
print("Python 里的对应物就是列表：", tags)
print("用途：标签、embedding 向量 id、坐标序列等。")

# 3. UUID
section("3. UUID：全局唯一标识符")

print("PostgreSQL：")
print("  CREATE TABLE users (id UUID PRIMARY KEY);")
print("  id UUID 由应用或数据库生成，全局唯一。")
print()
print("Python 生成 UUID：")
for _ in range(3):
    print("  ", uuid.uuid4())
print()
print("为什么后端 API 常见 UUID：")
print("  * 分布式系统里保证全局唯一，不依赖单库自增。")
print("  * 不暴露业务量（自增 id 会泄露有多少用户/订单）。")

section("小结")
print("1. JSONB：数据库里存查 JSON，适合灵活元数据。")
print("2. ARRAY：数组类型，适合标签、embedding id 等。")
print("3. UUID：全局唯一主键，后端 API 常见。")
print("4. 这些类型正是 GIS / GeoAI 技术栈常用的。")
