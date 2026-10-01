# -*- coding: utf-8 -*-
"""
6. 事务与 ACID —— 可运行演示脚本
=================================

核心认知：

    事务把多条 SQL 打包成「一个不可分割的整体」：要么全部成功，要么全部回滚。

    银行转账：
        A 账户 -100
        B 账户 +100
    绝不能出现「A 扣了钱，B 没加上」——必须同生共死。

        BEGIN;  ...  COMMIT;   提交
        BEGIN;  ...  ROLLBACK; 回滚

    事务要满足 ACID：原子性、一致性、隔离性、持久性。

运行：python "6. 事务与ACID.py"
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
cur.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT, balance REAL)")
cur.executemany("INSERT INTO accounts VALUES (?, ?, ?)",
                [(1, "A", 1000.0), (2, "B", 1000.0)])
conn.commit()


def show_balances(label):
    print(label)
    for row in cur.execute("SELECT * FROM accounts").fetchall():
        print(f"    {row[1]} 账户余额 = {row[2]}")
    print()


show_balances("初始状态：")

# 1. 事务：BEGIN ... COMMIT
section("1. 事务：转账成功（BEGIN ... COMMIT）")

conn.execute("BEGIN")
cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")  # A -100
cur.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")  # B +100
conn.commit()

show_balances("COMMIT 之后（A 扣 100，B 加 100，一致）：")

# 2. 回滚：中途失败 ROLLBACK
section("2. 事务：中途失败回滚（ROLLBACK）")

conn.execute("BEGIN")
cur.execute("UPDATE accounts SET balance = balance - 200 WHERE id = 1")  # A -200
print("模拟中间出错，执行 ROLLBACK ...")
conn.rollback()   # 撤销事务里所有改动

show_balances("ROLLBACK 之后（A 的 -200 被撤销，余额回到之前）：")

# 3. ACID
section("3. ACID 四特性")

print("Atomicity   原子性：事务要么全部成功，要么全部回滚，不可分割。")
print("Consistency 一致性：事务前后，数据都满足约束（如余额不能为负）。")
print("Isolation   隔离性：并发事务互不干扰（见第 7、8 节 锁 与 MVCC）。")
print("Durability  持久性：提交后数据永久保存，即使断电也不丢。")
print()
print("对应关系：")
print("  Atomicity  -> COMMIT / ROLLBACK（本节）")
print("  Isolation  -> 锁 + MVCC（第 7、8 节）")

section("小结")
print("1. 事务 = 多条 SQL 打包成原子操作。")
print("2. BEGIN ... COMMIT 提交；出错 ROLLBACK 回滚。")
print("3. ACID：原子性、一致性、隔离性、持久性。")
print("4. 转账、下单扣库存等场景，必须用事务保证数据一致。")
