# -*- coding: utf-8 -*-
"""
8. MVCC 多版本并发控制 —— 可运行讲解脚本（PostgreSQL 专属概念）
===============================================================

核心认知：

    MVCC（Multi-Version Concurrency Control，多版本并发控制）是
    PostgreSQL 并发机制的核心，它不是「一个事务把数据库锁死」。

    思想：
        事务 A  -> 看到某个版本的数据（快照）
        事务 B  -> 修改产生新的数据版本（不覆盖旧的）
        事务 A  -> 根据可见性规则，决定看到哪个版本

    好处：读不阻塞写、写不阻塞读，并发性能好。

运行：python "8. MVCC 多版本并发控制.py"
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


# 1. 传统做法 vs MVCC
section("1. 传统加锁 vs MVCC")

print("传统做法（简单粗暴）：一个事务写数据时，把整行锁死，别人读写都等。")
print("  问题：写会阻塞读，读也会阻塞写，并发性能差。")
print()
print("MVCC（PostgreSQL 的做法）：")
print("  写不覆盖旧数据，而是『产生新版本』；")
print("  读不阻塞，直接读『自己快照里的旧版本』。")
print("  结果：读和写互不阻塞，并发更好。")

# 2. 版本链：一行多个版本
section("2. 一行数据的多个版本（版本链）")

print("MVCC 下，修改不是覆盖，而是追加新版本：")
print()
versions = [
    ("版本 1（初始）      ", 100),
    ("版本 2（事务B提交）  ", 80),
    ("版本 3（事务C提交）  ", 120),
]
print("  balance 这一行的版本链：")
for label, v in versions:
    print(f"    {label} -> balance = {v}")
print()
print("旧版本不立刻删除，等没有事务再需要它们时才被清理（VACUUM）。")

# 3. 快照隔离
section("3. 快照：每个事务看到自己的版本")

print("事务开始时，数据库给它一个『快照』，之后它只看到快照那一刻的数据。")
print()
print("  事务A 开始 -> 快照 balance=100")
print("  事务B 修改 balance=80 并提交")
print("  事务A 再读 -> 仍看到 balance=100（自己的快照）")
print()
print("这就是『快照隔离』：事务A 不受并发修改的干扰。")

# 4. 用简单 Python 结构模拟「快照」
section("4. 用 Python 模拟快照读")

class Database:
    def __init__(self):
        self.value = 100          # 当前最新值
        self.history = [100]      # 历史版本

    def update(self, new_val):
        self.history.append(self.value)   # 旧值进历史
        self.value = new_val

    def snapshot(self):
        return self.history[0]            # 简化：快照=最早版本


db = Database()
print("初始 value =", db.value)

snap_A = db.snapshot()   # 事务A开始时记住快照
print("事务A 的快照 =", snap_A)

db.update(80)            # 事务B 修改并提交
print("事务B 提交后 value =", db.value)

print("事务A 再读自己快照 =", snap_A, "（不受事务B影响）")
print()
print("简化模拟，但表达了 MVCC 的核心：读拿的是『自己的快照』。")

# 5. 好处与代价
section("5. MVCC 的好处与代价")

print("好处：")
print("  * 读不阻塞写、写不阻塞读，高并发下性能好。")
print("  * 事务看到一致的数据快照，逻辑简单清晰。")
print()
print("代价：")
print("  * 旧版本要占空间，需要 VACUUM 定期清理。")
print("  * 不同事务看到不同版本，某些场景需注意（如长事务拖慢清理）。")
print()
print("以后学 FastAPI + PostgreSQL 并发问题时，这个知识非常重要。")

section("小结")
print("1. MVCC = 多版本并发控制，写不覆盖旧数据。")
print("2. 每个事务看自己的『快照』，读不阻塞写。")
print("3. 旧版本由 VACUUM 清理。")
print("4. MVCC 与锁互补，共同实现事务隔离。")
