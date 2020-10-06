import time
import random
import json
data = []
# avg=100 StandardDeviation=15
timestamp = int(time.time()) * 1000
# data.append([timestamp, 0])
for x in xrange(1, 69):
    timestamp = timestamp + x
    # integer = random.randint(85, 115)
    # array = [timestamp, integer]
    array = [timestamp, 115]
    if x >= 34:
        array = [timestamp, 85]
    data.append(array)
# 27 counts
for x in xrange(69, 97):
    timestamp = timestamp + x
    # integer = random.randint(70, 130)
    # array = [timestamp, integer]
    array = [timestamp, 130]
    if x >= 82:
        array = [timestamp, 70]
    data.append(array)
# 4 counts
for x in xrange(97, 101):
    timestamp = timestamp + x
    array = [timestamp, 145]
    if x >= 99:
        array = [timestamp, 55]
    # integer = random.randint(55, 145)
    # array = [timestamp, integer]
    data.append(array)


print json.dumps({
    "data": data,
    "return_score": True,
    "recent_window": -1,
    "method": "std",
    "std_threshold": 0,
    "max_anoms": 1,
    "alpha_level": 0.01
})

# "return_score": True,  show anomaly_score
# "recent_window": -1, 關注己秒內的異動 ,-1 此值不計算
# "method": "std", 標準差
# "std_threshold": 1, 幾個標準差後為計算範圍 例:1 表示 不計算1個標準差內的值 之外的值為計算範圍
# "max_anoms": 1, 百分之幾的資料是列為計算
# "alpha_level": 0.01 顯著水準/表示希望檢測時的誤判機率愈低(即希望檢測能愈準確),愈小愈精確
# "direction":"both"  是正數或負數 both指兩個都算在比較資料
