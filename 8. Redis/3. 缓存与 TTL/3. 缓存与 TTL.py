# -*- coding: utf-8 -*-
"""
3. 缓存与 TTL —— 可运行演示脚本
===============================

核心认知：

    缓存是 Redis 最重要的用途。配合 TTL（过期时间），热点数据自动失效。

        redis.set("llm:result:长沙高校", result, ex=3600)
        # ex=3600 表示：3600 秒后自动过期

    经典「缓存旁路（Cache-Aside）」模式：

        查 Redis -> 有？直接返回
                  -> 没有？计算/查库 -> 存入 Redis（带 TTL）-> 返回

运行：python "3. 缓存与 TTL.py"（需本机已启动 Redis）
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


# 1. TTL：过期时间
section("1. TTL：给缓存设过期时间")

r.set("temp", "value", ex=10)   # 10 秒后过期
print('set("temp", "value", ex=10)')
print("  剩余 TTL（秒）：", r.ttl("temp"))
print()
print("ex 参数 = 过期秒数；时间一到，键自动删除。")

# 2. 缓存旁路模式（模拟 LLM 结果缓存）
section("2. 缓存旁路：模拟 LLM 结果缓存")


def get_answer(question):
    """模拟：查缓存 -> 没有 -> 调 LLM -> 存缓存 -> 返回"""
    key = f"llm:{question}"
    cached = r.get(key)
    if cached is not None:
        return cached, True          # 命中缓存

    # 未命中：模拟昂贵的 LLM 调用
    answer = f"《{question}》的答案：长沙高校有中南大学、湖南大学等"
    r.set(key, answer, ex=3600)      # 缓存 1 小时
    return answer, False             # 未命中


print("用户两次问「长沙有哪些高校」：")
print()
ans, hit = get_answer("长沙有哪些高校")
print("  第 1 次：", "命中缓存" if hit else "未命中（调 LLM 并缓存）")
print("          ", ans)
ans, hit = get_answer("长沙有哪些高校")
print("  第 2 次：", "命中缓存" if hit else "未命中")
print("          ", ans)
print()
print("第二次直接命中 Redis，不再调 LLM —— 降低延迟和成本。")

# 3. 缓存模式的价值
section("3. 为什么 AI 后端特别常用")

print("  * 减少 LLM 调用：相同问题直接返回缓存。")
print("  * 降低延迟：内存读比 LLM 推理快几个数量级。")
print("  * 降低成本：少调 API，少花钱。")
print("  * 自动过期：TTL 保证缓存不会永远陈旧。")

section("小结")
print("1. TTL（ex 参数）让缓存自动过期。")
print("2. 缓存旁路：查缓存 -> miss 则计算 -> 回填缓存。")
print("3. 价值：减少 LLM 调用、降低延迟和成本。")
