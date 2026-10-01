# -*- coding: utf-8 -*-
"""
6. GIL（Global Interpreter Lock，全局解释器锁）—— 可运行演示脚本
================================================================

核心认知：

    CPython 的 GIL 是一把全局锁：同一时刻，只有一个线程能执行 Python 字节码。

        线程1 ──┐
                ├── GIL（同一时刻只放行一个线程）── Python 字节码
        线程2 ──┘

    所以「多线程 = 速度 ×2」在 CPU 密集场景是错觉；
    但在 I/O 密集场景（等数据库/网络/文件）多线程依然有效。

运行：python "6. GIL.py"（CPU 密集部分需要几秒）
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


# 1. CPU 密集：多线程几乎不加速
section("1. CPU 密集：多线程 vs 单线程（几乎不加速）")


def cpu_task(n):
    s = 0
    for i in range(n):
        s += i
    return s


N = 5_000_000   # 每份任务 500 万次纯计算

print("每份任务做", N, "次纯计算（不涉及 I/O）。")
print()

# 单线程：串行做两份
t0 = time.perf_counter()
cpu_task(N)
cpu_task(N)
single = time.perf_counter() - t0
print(f"单线程串行做两份：  {single:.3f} 秒")

# 双线程：并行做两份
t0 = time.perf_counter()
t1 = threading.Thread(target=cpu_task, args=(N,))
t2 = threading.Thread(target=cpu_task, args=(N,))
t1.start()
t2.start()
t1.join()
t2.join()
multi = time.perf_counter() - t0
print(f"双线程并行做两份：  {multi:.3f} 秒")
print()
if single > 0:
    print(f"加速比 = 单线程 / 双线程 = {single / multi:.2f}x")
print()
print("结论：双线程没有变快（甚至更慢），因为 GIL 让两个线程轮流抢一把锁，")
print("      同一时刻只有一个线程在算，还额外付出了切换开销。")

# 2. I/O 密集：多线程有效
section("2. I/O 密集：多线程明显加速（GIL 在 I/O 时被释放）")


def io_task(name, seconds):
    print(f"  [{name}] 开始等待 {seconds}s ...")
    time.sleep(seconds)   # sleep 会释放 GIL，让别的线程有机会跑
    print(f"  [{name}] 完成")


print("串行：等两次 1 秒")
t0 = time.perf_counter()
io_task("A", 1)
io_task("B", 1)
serial = time.perf_counter() - t0
print(f"  串行耗时：{serial:.2f} 秒")
print()

print("双线程：同时等两次 1 秒")
t0 = time.perf_counter()
t1 = threading.Thread(target=io_task, args=("A", 1))
t2 = threading.Thread(target=io_task, args=("B", 1))
t1.start()
t2.start()
t1.join()
t2.join()
parallel = time.perf_counter() - t0
print(f"  双线程耗时：{parallel:.2f} 秒")
print()
print("结论：等待 I/O（睡眠/网络/磁盘/数据库）时线程会释放 GIL，")
print("      所以多个线程能「同时等」，I/O 密集场景多线程几乎线性加速。")

# 3. GIL 如何切换线程
section("3. GIL 会周期性切换线程")

print("GIL 不是一直霸占，而是每隔一段时间主动释放一次，让其他线程有机会拿到锁。")
print("这个间隔叫 switch interval：")
print("  sys.getswitchinterval() =", sys.getswitchinterval(), "秒")
print()
print("这解释了为什么纯计算多线程『看起来也在跑』，只是轮流跑，不并行。")
print()

# 4. 解法
section("4. CPU 密集的正确解法")

print("CPU 密集（矩阵计算、图像处理、大量循环）应该：")
print("  1. multiprocessing：多进程，每个进程有自己的解释器和 GIL")
print("  2. C 扩展 / Cython / Numba：把重活搬出 Python 层（C 代码可释放 GIL）")
print("  3. NumPy 等库：底层用 C 实现，运算时释放 GIL")
print("  4. CUDA：GPU 并行")
print()
print("I/O 密集（Web 服务、爬虫、等数据库/网络/文件）：")
print("  * 多线程 threading：有效，简单")
print("  * asyncio：单线程异步并发，现代 Python 推荐，适合大量连接")
print()
print("补充：Python 3.13 提供了实验性的 free-threaded 版本（可关闭 GIL），")
print("      但当前主流仍是「带 GIL 的 CPython」。")

section("小结")
print("1. GIL：同一时刻只有一个线程执行 Python 字节码。")
print("2. CPU 密集：多线程无效，用 multiprocessing / C 扩展 / NumPy。")
print("3. I/O 密集：多线程有效（GIL 在 I/O 时释放）。")
print("4. asyncio 是单线程并发，也绕开了多线程的 GIL 争抢问题。")
