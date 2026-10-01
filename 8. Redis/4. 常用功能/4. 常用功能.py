# -*- coding: utf-8 -*-
"""
4. 常用功能：计数器 / 限流 / Session / 分布式锁 —— 可运行演示脚本
================================================================

核心认知：

    除了缓存，Redis 还有几个后端高频功能：

        计数器       INCR（原子自增）
        限流         计数器 + 过期时间
        Session      带 TTL 的键，存登录态
        分布式锁     SET key value NX EX（原子加锁）

运行：python "4. 常用功能.py"（需本机已启动 Redis）
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


# 1. 计数器
section("1. 计数器：INCR 原子自增")

r.set("page:views", 0)
for _ in range(5):
    r.incr("page:views")   # 每次 +1，原子操作
print("5 次 incr 后 page:views =", r.get("page:views"))
print("INCR 是原子的：并发下也不会少加。")

# 2. 限流
section("2. 限流：计数器 + 过期时间")


def allow_request(user_id, limit=5, window=60):
    key = f"rate:{user_id}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, window)   # 第一次请求时设置窗口
    return count <= limit


print("限制：60 秒内最多 5 次。模拟 7 次请求：")
for i in range(7):
    ok = allow_request("user:1", limit=5, window=60)
    print(f"  第 {i + 1} 次请求 -> {'允许' if ok else '拒绝（限流）'}")

# 3. Session
section("3. Session：带 TTL 的登录态")

r.set("session:abc123", "user_id=1001", ex=1800)   # 30 分钟
print('set("session:abc123", "user_id=1001", ex=1800)')
print("  读取 session:", r.get("session:abc123"))
print("  剩余时间：", r.ttl("session:abc123"), "秒")
print("  30 分钟后自动过期，用户需重新登录。")

# 4. 分布式锁
section("4. 分布式锁：SET NX EX")

print("SET key value NX EX 的语义：不存在才设置 + 设过期。")
print()
acquired = r.set("lock:task", "worker1", nx=True, ex=10)
print("  第一次获取锁 ->", acquired, "（成功）")
acquired2 = r.set("lock:task", "worker2", nx=True, ex=10)
print("  第二次获取锁 ->", acquired2, "（失败，锁已被占）")
print()
print("用途：多个服务实例抢同一个任务时，保证只有一个拿到锁。")

section("小结")
print("1. 计数器：INCR 原子自增。")
print("2. 限流：INCR + EXPIRE，控制频率。")
print("3. Session：带 TTL 的键存登录态。")
print("4. 分布式锁：SET NX EX，原子加锁。")
