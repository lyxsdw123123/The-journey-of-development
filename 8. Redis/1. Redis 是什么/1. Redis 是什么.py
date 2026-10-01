# -*- coding: utf-8 -*-
"""
1. Redis 是什么 —— 可运行演示脚本
=================================

核心认知：

    Redis 是一个速度非常快、主要把数据放在内存中的 Key-Value 数据库。

        redis.set("user:1001:name", "张三")
        name = redis.get("user:1001:name")   # "张三"

    相当于一张巨大的哈希表："user:1001:name" -> "张三"。

运行：python "1. Redis 是什么.py"（需本机已启动 Redis，默认 127.0.0.1:6379）
"""
import sys
import redis

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


def get_redis():
    try:
        r = redis.Redis(host="127.0.0.1", port=6379, db=15, decode_responses=True, protocol=2)  # protocol=2 兼容老版 Redis
        r.ping()
        return r
    except Exception as e:
        print("无法连接 Redis，请先启动：redis-server")
        print("错误：", e)
        sys.exit(1)


r = get_redis()
r.flushdb()   # 使用独立的 db 15 做演示，清空避免污染你的数据


# 1. Key-Value
section("1. Key-Value：内存中的哈希表")

r.set("user:1001:name", "张三")
name = r.get("user:1001:name")
print('set("user:1001:name", "张三")')
print('get("user:1001:name") ->', name)
print()
print('相当于："user:1001:name" -> "张三"')
print("Key 是唯一标识，Value 是对应的数据。")

# 2. 为什么快
section("2. 为什么这么快")

print("1. 数据在内存里（不是磁盘），读写极快。")
print("2. 单线程处理命令，没有锁竞争。")
print("3. 简单的 Key-Value 模型，无复杂查询开销。")
print()
print("常见性能：每秒几万 ~ 几十万次操作。")

# 3. Redis 的定位
section("3. Redis 的定位：与 PostgreSQL 互补")

print("Redis 不是取代 PostgreSQL，而是互补：")
print("  PostgreSQL -> 持久化、关系查询（源数据、复杂查询）")
print("  Redis      -> 缓存、Session、计数、限流（热点、临时数据）")
print()
print("典型分工：")
print("  FastAPI -> 先查 Redis（快）-> 没有 -> 查 PostgreSQL -> 回填 Redis")

section("小结")
print("1. Redis = 内存 Key-Value 数据库，速度极快。")
print("2. 核心操作：set(key, value) / get(key)。")
print("3. 定位：缓存/临时数据，与 PostgreSQL 互补。")
