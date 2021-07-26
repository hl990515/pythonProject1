import time
import math

lon = float(input("请输入当前经度："))
lat = float(input("请输入当前纬度："))
TimeZone = int(input("请输入当前时区号："))
station = input("请输入当前地区：")


JD0 = int(365.25 * (time.localtime().tm_year - 1)) + int(
    30.6001 * (1 + 13)) + 1 + time.localtime().tm_hour / 24 + 1720981.5
if time.localtime().tm_mon <= 2:
    JD2 = int(365.25 * (time.localtime().tm_year - 1)) + int(
        30.6001 * (time.localtime().tm_mon + 13)) + time.localtime().tm_mday + time.localtime().tm_hour / 24 + 1720981.5
else:
    JD2 = int(365.25 * time.localtime().tm_year) + int(
        30.6001 * (time.localtime().tm_mon + 1)) + time.localtime().tm_mday + time.localtime().tm_hour / 24 + 1720981.
DOY = JD2 - JD0 + 1
# N0   sitar=θ
N0 = 79.6764 + 0.2422 * (time.localtime().tm_year - 1985) - int((time.localtime().tm_year - 1985) / 4.0)
sitar = 2 * math.pi * (DOY - N0) / 365.2422
ED1 = 0.3723 + 23.2567 * math.sin(sitar) + 0.1149 * math.sin(2 * sitar) - 0.1712 * math.sin(
    3 * sitar) - 0.758 * math.cos(sitar) + 0.3656 * math.cos(2 * sitar) + 0.0201 * math.cos(3 * sitar)
ED = ED1 * math.pi / 180  # ED本身有符号

if lon >= 0:
    if TimeZone == -13:
        dLon = lon - (math.floor((lon * 10 - 75) / 150) + 1) * 15.0
    else:
        dLon = lon - TimeZone * 15.0  # 地球上某一点与其所在时区中心的经度差
else:
    if TimeZone == -13:
        dLon = (math.floor((lon * 10 - 75) / 150) + 1) * 15.0 - lon
    else:
        dLon = TimeZone * 15.0 - lon
# 时差
Et = 0.0028 - 1.9857 * math.sin(sitar) + 9.9059 * math.sin(2 * sitar) - 7.0924 * math.cos(sitar) - 0.6882 * math.cos(
    2 * sitar)
gtdt1 = time.localtime().tm_hour + time.localtime().tm_min / 60.0 + time.localtime().tm_sec / 3600.0 + dLon / 15  # 地方时

gtdt = gtdt1 + Et / 60.0

dTimeAngle1 = 15.0 * (gtdt - 12)
dTimeAngle = dTimeAngle1 * math.pi / 180
latitudeArc = lat * math.pi / 180

# 高度角计算公式
HeightAngleArc = math.asin(
    math.sin(latitudeArc) * math.sin(ED) + math.cos(latitudeArc) * math.cos(ED) * math.cos(dTimeAngle))
# 方位角计算公式
CosAzimuthAngle = (math.sin(HeightAngleArc) * math.sin(latitudeArc) - math.sin(ED)) / math.cos(
    HeightAngleArc) / math.cos(latitudeArc)
AzimuthAngleArc = math.acos(CosAzimuthAngle)
HeightAngle = HeightAngleArc * 180 / math.pi
ZenithAngle = 90 - HeightAngle
AzimuthAngle1 = AzimuthAngleArc * 180 / math.pi

if dTimeAngle < 0:
    AzimuthAngle = 180 - AzimuthAngle1
else:
    AzimuthAngle = 180 + AzimuthAngle1

print(f'站位：{station} 太阳天顶角(deg)：{ZenithAngle} 高度角(deg)：{HeightAngle} 方位角(deg):{AzimuthAngle}')
