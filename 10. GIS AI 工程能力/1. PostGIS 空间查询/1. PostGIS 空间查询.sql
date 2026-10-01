-- PostGIS 空间查询示例（需 PostgreSQL + PostGIS 环境）
-- 执行前：CREATE EXTENSION postgis;

-- 1. 建一张带空间列的表
CREATE TABLE schools (
    id   SERIAL PRIMARY KEY,
    name TEXT,
    geom GEOMETRY(Point, 4326)   -- 点几何，4326 = WGS84 经纬度
);

-- 2. 插入点数据（长沙市中心附近）
INSERT INTO schools (name, geom) VALUES
    ('湖南大学', ST_SetSRID(ST_Point(112.939, 28.170), 4326)),
    ('中南大学', ST_SetSRID(ST_Point(112.933, 28.155), 4326)),
    ('湖南师范大学', ST_SetSRID(ST_Point(112.943, 28.182), 4326));

-- 3. 创建空间索引（GiST，加速空间查询）
CREATE INDEX idx_schools_geom ON schools USING GIST (geom);

-- 4. 查询 5000 米内的学校
SELECT name
FROM schools
WHERE ST_DWithin(
    geom,
    ST_SetSRID(ST_Point(112.93, 28.18), 4326),
    5000
);

-- 5. 常用空间函数示例
-- 距离（米）
SELECT name, ST_Distance(geom, ST_SetSRID(ST_Point(112.93, 28.18), 4326)) AS dist
FROM schools
ORDER BY dist;

-- 缓冲区：某点周围 1000 米的范围
SELECT ST_Buffer(ST_SetSRID(ST_Point(112.93, 28.18), 4326)::geography, 1000);

-- 相交：学校是否与某个区域相交
-- SELECT * FROM schools WHERE ST_Intersects(geom, region_geom);

-- 质心：多边形的中心点
-- SELECT ST_Centroid(polygon_geom) FROM districts;
