# -*- coding: utf-8 -*-
"""
10. PostGIS 空间数据库 —— 可运行讲解脚本
=========================================

核心认知：

    你是 GIS 专业，PostGIS 是 PostgreSQL 的空间扩展，是你的核心优势。

    整个技术栈可以变成：

        Python -> FastAPI -> SQL -> PostgreSQL -> PostGIS -> GeoAI / LLM

    PostGIS 让你在数据库里做空间查询，例如「找出 1000 米内的建筑」：

        SELECT * FROM buildings
        WHERE ST_DWithin(
            geom,
            ST_SetSRID(ST_Point(112.9388, 28.2282), 4326),
            1000
        );

    这已经不是普通后端，而是「空间数据库 + 后端 + AI」。

运行：python "10. PostGIS 空间数据库.py"
"""
import sys
import math

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SEP = "=" * 70
SUB = "-" * 70


def section(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


# 1. 什么是 PostGIS
section("1. 什么是 PostGIS")

print("PostGIS = PostgreSQL 的空间扩展，让数据库能存、能查『地理数据』。")
print()
print("  * 空间类型：点（Point）、线（LineString）、面（Polygon）等")
print("  * 空间函数：距离、相交、包含、缓冲区等")
print("  * 空间索引：GiST 索引加速空间查询")
print()
print("普通数据库只能查『age > 18』，PostGIS 能查『离我 1000 米内的建筑』。")

# 2. ST_DWithin：距离查询
section("2. ST_DWithin：找出 1000 米内的建筑")

print("PostGIS 空间查询：")
print()
print("  SELECT *")
print("  FROM buildings")
print("  WHERE ST_DWithin(")
print("      geom,")
print("      ST_SetSRID(ST_Point(112.9388, 28.2282), 4326),")
print("      1000")
print("  );")
print()
print("解读：")
print("  ST_Point(经度, 纬度)    -> 创建一个点（长沙市中心附近）")
print("  ST_SetSRID(..., 4326)   -> 指定坐标系（4326 = WGS84 经纬度）")
print("  ST_DWithin(geom, 点, 1000) -> 判断 geom 是否在点周围 1000 米内")

# 3. 用 Python 计算球面距离（类比 ST_DWithin）
section("3. 用 Python 模拟球面距离（理解 1000 米内）")


def haversine(lon1, lat1, lon2, lat2):
    """计算两个经纬度点之间的球面距离（米）。"""
    R = 6371000  # 地球半径（米）
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


center = (112.9388, 28.2282)      # 长沙市中心附近
near = (112.9450, 28.2282)        # 约几百米
far = (113.0000, 28.3000)         # 约 10 公里

print("中心点：", center)
print(f"  近点距离：{haversine(*center, *near):.0f} 米  -> 在 1000 米内")
print(f"  远点距离：{haversine(*center, *far):.0f} 米  -> 不在 1000 米内")
print()
print("ST_DWithin 就是数据库版的这个判断，还带空间索引，海量数据也快。")

# 4. 完整技术栈
section("4. 你的完整技术栈：空间数据库 + 后端 + AI")

print("  Python")
print("     ↓")
print("  FastAPI")
print("     ↓")
print("  SQL")
print("     ↓")
print("  PostgreSQL")
print("     ↓")
print("  PostGIS")
print("     ↓")
print("  GeoAI / LLM")
print()
print("这已经不是普通后端，而是『空间数据库 + 后端 + AI』，")
print("和你的 GIS 背景非常契合，是你区别于普通后端的核心竞争力。")

section("小结")
print("1. PostGIS 让 PostgreSQL 能存查地理数据。")
print("2. ST_DWithin 做距离查询（1000 米内的建筑）。")
print("3. 空间函数 + 空间索引 = 海量地理数据也快。")
print("4. Python + FastAPI + PostgreSQL + PostGIS + AI 是你的优势技术栈。")
