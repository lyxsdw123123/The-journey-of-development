# -*- coding: utf-8 -*-
"""
1. SELECT 与聚合查询 —— 可运行演示脚本
======================================

核心认知：

    SQL 查询有固定执行顺序，理解顺序比死记语法更重要：

        FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT

    本脚本用 Python 内置 sqlite3 建一个内存数据库，真实执行每条 SQL，
    让你「跑起来看」结果。这些标准 SQL 在 PostgreSQL 里用法完全一致。

运行：python "1. SELECT 与聚合查询.py"
"""
import sys
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


# 建内存数据库 + users 表
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    department TEXT
)
""")
users = [
    ("Tom",   20, "工程"),
    ("Jack",  25, "工程"),
    ("Alice", 17, "市场"),
    ("Bob",   30, "工程"),
    ("Cindy", 22, "市场"),
    ("David", 19, "销售"),
    ("Tom",   35, "工程"),   # 故意重名，演示 DISTINCT
]
cur.executemany("INSERT INTO users (name, age, department) VALUES (?, ?, ?)", users)
conn.commit()


def run(sql, title=""):
    """执行一条 SQL 并打印结果。"""
    if title:
        print(title)
    print("  SQL: " + " ".join(sql.split()))
    cur.execute(sql)
    cols = [d[0] for d in (cur.description or [])]
    rows = cur.fetchall()
    if cols:
        print("  " + " | ".join(cols))
        print("  " + "-" * 52)
        for r in rows:
            print("  " + " | ".join(str(v) for v in r))
    print()


# 1. SELECT / FROM / WHERE
section("1. SELECT / FROM / WHERE")

run("SELECT * FROM users", "全表查询")
run("SELECT * FROM users WHERE age > 18", "WHERE 过滤")
run("SELECT name, age FROM users WHERE age > 18", "只取部分列")

# 2. ORDER BY / LIMIT / OFFSET
section("2. ORDER BY / LIMIT / OFFSET")

run("SELECT name, age FROM users WHERE age > 18 ORDER BY age DESC LIMIT 3",
    "按年龄降序，取前 3 条")
run("SELECT name, age FROM users WHERE age > 18 ORDER BY age DESC LIMIT 3 OFFSET 1",
    "跳过 1 条再取 3 条（分页常用）")

# 3. DISTINCT
section("3. DISTINCT 去重")

run("SELECT name FROM users", "不去重（有重名 Tom）")
run("SELECT DISTINCT name FROM users", "DISTINCT 去重")

# 4. 聚合函数
section("4. 聚合函数：COUNT / SUM / AVG / MAX / MIN")

run("SELECT COUNT(*) FROM users", "总行数")
run("SELECT SUM(age) FROM users", "年龄总和")
run("SELECT AVG(age) FROM users", "平均年龄")
run("SELECT MAX(age) FROM users", "最大年龄")
run("SELECT MIN(age) FROM users", "最小年龄")

# 5. GROUP BY
section("5. GROUP BY 分组统计")

run("SELECT department, COUNT(*) FROM users GROUP BY department",
    "每个部门有多少人")

# 6. HAVING 与执行顺序
section("6. HAVING 与执行顺序")

run("""SELECT department, COUNT(*) AS cnt
       FROM users
       GROUP BY department
       HAVING COUNT(*) > 1""",
    "只保留人数 > 1 的部门")
print("执行顺序：FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT")
print("关键：WHERE 在『分组前』过滤行；HAVING 在『分组后』过滤组。")
print("所以聚合条件（如 COUNT(*) > 1）只能写在 HAVING，不能写在 WHERE。")

section("小结")
print("1. 基础结构：SELECT 列 FROM 表 WHERE 条件 ORDER BY 列 LIMIT 条数。")
print("2. 聚合函数：COUNT/SUM/AVG/MAX/MIN，通常配 GROUP BY 使用。")
print("3. 执行顺序：WHERE(过滤行) -> GROUP BY(分组) -> HAVING(过滤组)。")
print("4. DISTINCT 去重，OFFSET 配合 LIMIT 做分页。")
