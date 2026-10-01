# -*- coding: utf-8 -*-
"""
5. 数据库表设计与约束 —— 可运行演示脚本
========================================

核心认知：

    后端开发不能只会查询，还要会「设计表」。关键是约束与关系：

        约束：PRIMARY KEY / NOT NULL / UNIQUE / CHECK / DEFAULT / FOREIGN KEY
        关系：一对一 / 一对多 / 多对多

    本脚本用 sqlite3 真实建表、插入数据、触发约束报错，
    让你直观感受「数据库如何在底层保证数据正确」。

运行：python "5. 数据库表设计与约束.py"
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
conn.execute("PRAGMA foreign_keys = ON")   # sqlite 默认不启用外键，需手动开
cur = conn.cursor()


# 1. 建表 + 约束
section("1. 建表：主键与约束")

print("PostgreSQL 写法：")
print("""  CREATE TABLE users (
      id BIGSERIAL PRIMARY KEY,
      username VARCHAR(50) NOT NULL UNIQUE,
      age INTEGER CHECK (age >= 0),
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );""")
print()
print("sqlite 等价写法（本脚本实际执行）：")
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 0),
    created_at TEXT DEFAULT (datetime('now'))
)
""")
print("  （sqlite 用 INTEGER PRIMARY KEY 自增，PG 用 BIGSERIAL）")
print()

# 2. 约束逐一演示
section("2. 约束逐一演示：违反会报错")

print("约束 = 数据库层面的『数据校验』，让脏数据根本进不来。")
print()

try:
    cur.execute("INSERT INTO users (username, age) VALUES (NULL, 20)")
except sqlite3.IntegrityError as e:
    print("  NOT NULL 违反 ->", e)

cur.execute("INSERT INTO users (username, age) VALUES ('Tom', 20)")
print("  正常插入 'Tom' 成功")
try:
    cur.execute("INSERT INTO users (username, age) VALUES ('Tom', 30)")
except sqlite3.IntegrityError as e:
    print("  UNIQUE 违反  ->", e)

try:
    cur.execute("INSERT INTO users (username, age) VALUES ('Jack', -5)")
except sqlite3.IntegrityError as e:
    print("  CHECK 违反   ->", e)

cur.execute("INSERT INTO users (username, age) VALUES ('Amy', 25)")
conn.commit()

run = lambda sql: (cur.execute(sql), cur.fetchall())
print()
print("最终 users 表：")
for row in run("SELECT * FROM users")[1]:
    print("  ", row)

# 3. 一对多
section("3. 一对多：外键 FOREIGN KEY")

cur.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
""")
cur.executemany("INSERT INTO orders (user_id, amount) VALUES (?, ?)",
                [(1, 99.0), (1, 50.0), (2, 30.0)])
conn.commit()

print("User -> Order 是一对多：一个用户可以有多个订单。")
print("orders 表（user_id 是外键，指向 users.id）：")
for row in run("SELECT * FROM orders")[1]:
    print("  ", row)
print()
print("外键保证引用完整性：")
try:
    cur.execute("INSERT INTO orders (user_id, amount) VALUES (999, 10)")
except sqlite3.IntegrityError as e:
    print("  插入不存在的 user_id=999 ->", e)

# 4. 多对多
section("4. 多对多：中间表")

cur.execute("CREATE TABLE groups (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("""
CREATE TABLE user_groups (
    user_id INTEGER,
    group_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
)
""")
cur.executemany("INSERT INTO groups VALUES (?, ?)", [(1, "admin"), (2, "editor")])
cur.executemany("INSERT INTO user_groups VALUES (?, ?)",
                [(1, 1), (1, 2), (2, 2)])
conn.commit()

print("多对多需要一张『中间表』user_groups 连接两边：")
for row in run("SELECT * FROM user_groups")[1]:
    print("  ", row)
print()
print("关系总结：")
print("  一对一   两张表各一行对应（少用，可合并）")
print("  一对多   一表主键 -> 另一表外键（最常见）")
print("  多对多   需要中间表（users <-> user_groups <-> groups）")

section("小结")
print("1. 约束：PRIMARY KEY / NOT NULL / UNIQUE / CHECK / DEFAULT / FOREIGN KEY。")
print("2. 约束在数据库层兜底，脏数据进不来。")
print("3. 一对多用外键；多对多用中间表。")
print("4. 这是后端系统数据的基础，ORM 只是把这些映射成对象。")
