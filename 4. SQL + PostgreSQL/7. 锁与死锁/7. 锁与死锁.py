# -*- coding: utf-8 -*-
"""
7. 锁与死锁 —— 可运行讲解脚本（PostgreSQL 专属概念）
=====================================================

核心认知：

    事务并发执行时，多个事务可能同时读写同一行数据，需要「锁」来协调：

        事务 -> 并发 -> 锁

    PostgreSQL 里最常用的行级锁：

        SELECT * FROM accounts WHERE id = 1 FOR UPDATE;

    要理解：共享锁/排他锁、行锁/表锁、死锁。

    （本脚本用 Python 线程锁模拟「死锁」，用文字 + PostgreSQL SQL 讲解其余概念。
    真实 FOR UPDATE 需要 PostgreSQL 环境。）

运行：python "7. 锁与死锁.py"
"""
import sys
import threading
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


# 1. 为什么需要锁
section("1. 为什么需要锁")

print("两个事务同时给同一行扣款，可能读到同一份余额，导致『丢失更新』。")
print("锁的作用：协调并发访问，保证同一时刻只有一个事务能改某一行。")
print()

# 2. FOR UPDATE：行级锁
section("2. FOR UPDATE：行级锁（PostgreSQL）")

print("PostgreSQL 里给一行加排他锁：")
print()
print("  BEGIN;")
print("  SELECT * FROM accounts WHERE id = 1 FOR UPDATE;")
print("  UPDATE accounts SET balance = balance - 100 WHERE id = 1;")
print("  COMMIT;")
print()
print("FOR UPDATE 会『锁住』查出来的这一行，别的事务要改这行就得等。")
print("这是『先读后改』场景下防止并发冲突的标准做法。")

# 3. 共享锁 vs 排他锁
section("3. 共享锁 vs 排他锁")

print("共享锁（Share）：多个事务可同时读，但不能写。")
print("排他锁（Exclusive）：独占，别的事务不能读也不能写。")
print()
print("  FOR UPDATE          -> 排他锁（我要改，别人别动）")
print("  FOR SHARE           -> 共享锁（我要读，别人别改）")
print()
print("类比：")
print("  共享锁 = 图书馆的书，多人可以同时看，但没人能撕")
print("  排他锁 = 你正在改的文档，别人既不能看也不能改")

# 4. 行锁 vs 表锁
section("4. 行锁 vs 表锁")

print("行锁：只锁住相关的几行，并发度高（PostgreSQL 默认，最常用）。")
print("表锁：锁住整张表，简单粗暴，并发差（如 DDL、批量操作）。")
print()
print("  行锁 -> SELECT ... FOR UPDATE")
print("  表锁 -> LOCK TABLE accounts IN EXCLUSIVE MODE;")

# 5. 死锁（用 Python 线程锁模拟）
section("5. 死锁：互相等待，谁也走不了")

print("死锁场景：")
print("  事务1：先锁 A 行，再想锁 B 行")
print("  事务2：先锁 B 行，再想锁 A 行")
print("  结果：事务1 等 B，事务2 等 A，互相等待 -> 死锁")
print()
print("用 Python 线程锁模拟这个过程：")

lock_a = threading.Lock()
lock_b = threading.Lock()


def tx1():
    lock_a.acquire()
    print("    事务1：拿到 A 行锁")
    time.sleep(0.2)
    print("    事务1：想拿 B 行锁 ...")
    got = lock_b.acquire(timeout=0.5)
    print(f"    事务1：拿到 B 行锁？{got}")


def tx2():
    lock_b.acquire()
    print("    事务2：拿到 B 行锁")
    time.sleep(0.2)
    print("    事务2：想拿 A 行锁 ...")
    got = lock_a.acquire(timeout=0.5)
    print(f"    事务2：拿到 A 行锁？{got}")


t1 = threading.Thread(target=tx1)
t2 = threading.Thread(target=tx2)
t1.start()
t2.start()
t1.join()
t2.join()
print()
print("两个事务都拿不到对方的锁（False），这就是死锁。")
print("数据库的做法：检测到死锁后，自动回滚其中一个事务来打破僵局。")

section("小结")
print("1. 锁协调并发访问，防止丢失更新。")
print("2. FOR UPDATE 加行级排他锁，先读后改的标准做法。")
print("3. 共享锁（多人读）vs 排他锁（独占写）。")
print("4. 死锁 = 互相等待；数据库会自动回滚一方来解除。")
