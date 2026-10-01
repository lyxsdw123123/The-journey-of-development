# -*- coding: utf-8 -*-
"""
4. 索引与查询优化 —— 可运行演示脚本
===================================

核心认知：

    没有索引时，数据库要「全表扫描」（Full Table Scan）：
        user1 -> user2 -> user3 -> ... -> user10000000  一个个检查。

    有索引时，数据库能快速定位，就像查字典的目录。

    但不要简单理解成「有索引 = 一定快」。真正要看执行计划：

        SQL -> Query Planner（查询规划器）-> 选择执行计划
            -> Index Scan / Seq Scan / ... -> 执行

    本脚本用 EXPLAIN QUERY PLAN 看 sqlite 的执行计划（PostgreSQL 用 EXPLAIN ANALYZE）。

运行：python "4. 索引与查询优化.py"
"""
import sys
import sqlite3
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 建一个 10 万行的表
N = 100_000
conn = sqlite3.connect(":memory:")
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)")
cur.executemany("INSERT INTO users (username) VALUES (?)",
                [(f"user{i}",) for i in range(N)])
conn.commit()
print(f"已建表 users，共 {N:,} 行。")
print()


def explain(sql, title=""):
    if title:
        print(title)
    print("  SQL: " + " ".join(sql.split()))
    cur.execute("EXPLAIN QUERY PLAN " + sql)
    for row in cur.fetchall():
        print("  计划:", row[0])
    print()


# 1. 没有索引：全表扫描
section("1. 没有索引：全表扫描（Full Table Scan）")

explain("SELECT * FROM users WHERE username = 'user99999'",
        "按 username 查（无索引）")
print("计划显示 SCAN —— 数据库要一行行扫过 10 万行。")

# 2. 建索引
section("2. 建索引")

cur.execute("CREATE INDEX idx_users_username ON users(username)")
print("执行：CREATE INDEX idx_users_username ON users(username);")
print("索引就像给 username 列建了『目录』，可快速定位。")
print()

# 3. 有索引：走索引
section("3. 有索引：走索引（Index Search）")

explain("SELECT * FROM users WHERE username = 'user99999'",
        "按 username 查（有索引）")
print("计划显示 SEARCH USING INDEX —— 直接定位，不用扫全表。")

# 4. 时间对比
section("4. 时间对比")

def time_query(sql, n=200):
    t0 = time.perf_counter()
    for _ in range(n):
        cur.execute(sql)
        cur.fetchall()
    return (time.perf_counter() - t0) / n

# 无索引（先删掉索引）
cur.execute("DROP INDEX idx_users_username")
t_no = time_query("SELECT * FROM users WHERE username = 'user99999'")

# 有索引（重新建）
cur.execute("CREATE INDEX idx_users_username ON users(username)")
t_yes = time_query("SELECT * FROM users WHERE username = 'user99999'")

print(f"无索引平均耗时：{t_no*1000:.4f} ms")
print(f"有索引平均耗时：{t_yes*1000:.4f} ms")
if t_no > 0:
    print(f"快了约 {t_no/t_yes:.0f} 倍")

# 5. 索引不是万能的
section("5. 索引不是万能的")

print("不是『有索引就一定快』：")
print("  1. 小表：全表扫描可能反而更快（索引本身有开销）。")
print("  2. 索引占空间，且 INSERT/UPDATE/DELETE 时要同步维护索引。")
print("  3. 低区分度列（如性别男/女）建索引收益小。")
print("  4. 要看执行计划（EXPLAIN）决定，而不是拍脑袋。")
print()
print("PostgreSQL 里对应命令：EXPLAIN ANALYZE SELECT ...;")
print("这是从『会写 SQL』进入『会优化 SQL』的关键一步。")

section("小结")
print("1. 无索引 = 全表扫描；有索引 = 快速定位。")
print("2. EXPLAIN（PG 用 EXPLAIN ANALYZE）看执行计划。")
print("3. 索引不是万能：小表/低区分度/写多读少都可能不划算。")
print("4. 优化靠看执行计划，而不是凭感觉。")
