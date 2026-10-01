# -*- coding: utf-8 -*-
"""
2. Redis 数据类型 —— 可运行演示脚本
===================================

核心认知：

    Redis 有 5 种核心数据类型，后端最常用前 4 种：

        String  字符串    -> 缓存、计数
        List    列表      -> 队列、时间线
        Set     集合      -> 去重、标签
        Hash    哈希      -> 对象、字段
        ZSet    有序集合  -> 排行榜

运行：python "2. Redis 数据类型.py"（需本机已启动 Redis）
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


r = redis.Redis(host="127.0.0.1", port=6379, db=15, decode_responses=True, protocol=2)  # protocol=2 兼容老版 Redis
r.flushdb()


# 1. String
section("1. String 字符串（最常用：缓存、计数）")

r.set("name", "Tom")
r.set("counter", 10)
r.incr("counter")          # 自增 1
print('set name =', r.get("name"))
print('incr counter ->', r.get("counter"))
print("用途：缓存一个值、计数器。")

# 2. List
section("2. List 列表（有序、可重复：队列）")

r.rpush("queue", "task1", "task2", "task3")   # 从右边入队
print("rpush 后 lrange:", r.lrange("queue", 0, -1))
print("lpop 取出一个:", r.lpop("queue"))
print("用途：任务队列、消息列表。")

# 3. Set
section("3. Set 集合（无序、去重：标签）")

r.sadd("tags", "gis", "ai", "gis")   # gis 重复，只会存一次
print("smembers:", r.smembers("tags"))
print("sismember 'ai':", r.sismember("tags", "ai"))
print("用途：标签、去重、共同关注。")

# 4. Hash
section("4. Hash 哈希（字段-值：存对象）")

# Redis 3.x 的 HSET 一次只接受一个 field-value，逐个写入（Redis 4+ 可用 mapping= 一次写多个）
r.hset("user:1001", "name", "Tom")
r.hset("user:1001", "age", "20")
r.hset("user:1001", "city", "长沙")
print("hgetall:", r.hgetall("user:1001"))
print("hget name:", r.hget("user:1001", "name"))
print("用途：存一个对象的多个字段（类似一行记录）。")

# 5. ZSet
section("5. ZSet 有序集合（带分数：排行榜）")

r.zadd("scores", {"Tom": 90, "Jack": 85, "Amy": 95})
print("按分数升序:", r.zrange("scores", 0, -1))
print("按分数降序:", r.zrevrange("scores", 0, -1))
print("用途：排行榜、按时间/分数排序。")

section("小结")
print("1. String：缓存、计数。")
print("2. List：队列。")
print("3. Set：去重、标签。")
print("4. Hash：存对象字段。")
print("5. ZSet：排行榜。")
