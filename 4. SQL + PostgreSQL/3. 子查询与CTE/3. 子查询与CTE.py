# -*- coding: utf-8 -*-
"""
3. 子查询与 CTE —— 可运行演示脚本
=================================

核心认知：

    复杂查询需要「套娃」：先算一个中间结果，再在它上面继续查。
    有两种写法：子查询（Subquery）和 CTE（Common Table Expression）。

    子查询：
        SELECT * FROM users
        WHERE id IN (SELECT user_id FROM orders);

    CTE（更清晰，可复用）：
        WITH user_orders AS (
            SELECT user_id, COUNT(*) AS cnt
            FROM orders
            GROUP BY user_id
        )
        SELECT * FROM user_orders WHERE cnt > 1;

运行：python "3. 子查询与CTE.py"
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
cur.executemany("INSERT INTO orders VALUES (?, ?)",
                [(10, 1), (11, 1), (12, 2), (13, 1)])
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


# 0. 看数据
section("0. 两张表")

run("SELECT * FROM users", "users")
run("SELECT * FROM orders", "orders")

# 1. 子查询：IN
section("1. 子查询：IN")

run("""
SELECT name
FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
)
""", "找出『下过单』的用户")
print("内层子查询先执行，得到 (1,1,2,1)，再拿它去匹配外层。")

# 2. 子查询：标量子查询
section("2. 标量子查询：子查询返回单个值")

run("""
SELECT name,
       (SELECT COUNT(*) FROM orders WHERE orders.user_id = users.id) AS order_cnt
FROM users
""", "每个用户 + 他的订单数（标量子查询）")

# 3. CTE：WITH
section("3. CTE：WITH 定义可读的中间结果")

run("""
WITH user_orders AS (
    SELECT user_id, COUNT(*) AS cnt
    FROM orders
    GROUP BY user_id
)
SELECT * FROM user_orders WHERE cnt > 1
""", "先统计每个用户订单数，再筛出 > 1 的")
print("CTE 把复杂查询拆成『命名步骤』，像写代码一样读起来更清晰。")

# 4. CTE 可复用
section("4. CTE 可复用、可组合")

run("""
WITH user_orders AS (
    SELECT user_id, COUNT(*) AS cnt
    FROM orders
    GROUP BY user_id
)
SELECT users.name, user_orders.cnt
FROM users
LEFT JOIN user_orders ON users.id = user_orders.user_id
""", "同一个 CTE 拿去 JOIN，列出所有用户和订单数")
print("注意：Amy 没订单，cnt 是 NULL（LEFT JOIN 的效果）。")

section("小结")
print("1. 子查询：把查询嵌套在 WHERE/SELECT 里，适合简单条件。")
print("2. CTE（WITH）：给中间结果命名，复杂查询更清晰、可复用。")
print("3. CTE 在复杂后端查询、数据分析、GIS 查询中都很有用。")
