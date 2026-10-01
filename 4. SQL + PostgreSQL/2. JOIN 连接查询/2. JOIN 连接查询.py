# -*- coding: utf-8 -*-
"""
2. JOIN 连接查询 —— 可运行演示脚本
==================================

核心认知：

    JOIN 把多张表按条件「拼」到一起，是 SQL 的核心。

        users:  id | name         orders:  id | user_id
        ┌────┬──────┐            ┌────┬─────────┐
        │ 1  │ Tom  │            │ 10 │ 1       │
        │ 2  │ Jack │            │ 11 │ 1       │
        │ 3  │ Amy  │            │ 12 │ 2       │
        └────┴──────┘            └────┴─────────┘

    JOIN ON users.id = orders.user_id 后，按「共同键」把两张表对上。

    重点掌握 INNER JOIN（只留匹配）和 LEFT JOIN（左表全留）。

运行：python "2. JOIN 连接查询.py"
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


conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER)")
cur.executemany("INSERT INTO users VALUES (?, ?)", [(1, "Tom"), (2, "Jack"), (3, "Amy")])
cur.executemany("INSERT INTO orders VALUES (?, ?)", [(10, 1), (11, 1), (12, 2)])
conn.commit()


def run(sql, title=""):
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


# 0. 看两张表
section("0. 两张表的数据")

run("SELECT * FROM users", "users 表")
run("SELECT * FROM orders", "orders 表")
print("注意：Amy(id=3) 没有任何订单，这是演示 LEFT JOIN 的关键。")

# 1. INNER JOIN
section("1. INNER JOIN：只保留能匹配上的行")

run("""
SELECT users.name, orders.id
FROM users
JOIN orders
ON users.id = orders.user_id
""", "INNER JOIN（JOIN 默认就是 INNER）")
print("结果：Tom-10、Tom-11、Jack-12。Amy 没订单，被丢弃。")

# 2. LEFT JOIN
section("2. LEFT JOIN：左表全部保留，匹配不上补 NULL")

run("""
SELECT users.name, orders.id
FROM users
LEFT JOIN orders
ON users.id = orders.user_id
""", "LEFT JOIN")
print("结果：Amy 也在，订单号是 NULL（没有订单）。")
print("用途：『列出所有用户，即使没订单』，后端最常见。")

# 3. RIGHT JOIN
section("3. RIGHT JOIN：右表全部保留")

run("""
SELECT users.name, orders.id
FROM users
RIGHT JOIN orders
ON users.id = orders.user_id
""", "RIGHT JOIN（右表 orders 全保留）")
print("注意：sqlite 3.39+ / PostgreSQL 都支持 RIGHT JOIN。")

# 4. FULL OUTER JOIN
section("4. FULL OUTER JOIN：两边全保留")

run("""
SELECT users.name, orders.id
FROM users
FULL OUTER JOIN orders
ON users.id = orders.user_id
""", "FULL OUTER JOIN")

# 5. CROSS JOIN
section("5. CROSS JOIN：笛卡尔积（两两组合）")

run("""
SELECT users.name, orders.id
FROM users
CROSS JOIN orders
""", "CROSS JOIN（3 用户 × 3 订单 = 9 行）")
print("用途：生成所有组合，但通常要小心数据量爆炸。")

section("小结")
print("1. JOIN 按 ON 条件把多张表拼起来。")
print("2. INNER JOIN：只留匹配；LEFT JOIN：左表全留，匹配不上补 NULL。")
print("3. RIGHT/FULL/CROSS JOIN 了解即可，INNER 和 LEFT 必须非常熟。")
print("4. 后端『列用户+订单』基本都用 LEFT JOIN。")
