#from week3task import emotionjudge
import jieba
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
print(pd.__doc__)

#emo = emotionjudge()
#print(emo("愁穷苦发火打死可喜合情合理所幸"))

from datetime import datetime
GMT_FORMAT = '%a %b %d %H:%M:%S %Y'
Time = 'Sun Oct 22 20:54:49 +0800 2017'
Time = Time.replace('+0800 ', '')
print(datetime.strptime(Time, GMT_FORMAT))

import datetime

today = datetime.date.today()
print(today)
print('ctime  :', today.ctime())
tt = today.timetuple()
print('tuple  : tm_year  =', tt.tm_year)
print('         tm_mon   =', tt.tm_mon)
print('         tm_mday  =', tt.tm_mday)
print('         tm_hour  =', tt.tm_hour)
print('         tm_min   =', tt.tm_min)
print('         tm_sec   =', tt.tm_sec)
print('         tm_wday  =', tt.tm_wday)
print('         tm_yday  =', tt.tm_yday)
print('         tm_isdst =', tt.tm_isdst)
print('ordinal:', today.toordinal())
print('Year   :', today.year)
print('Mon    :', today.month)
print('Day    :', today.day)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot([1, 2, 3, 4], [1, 4, 2, 3]);  # Plot some data on the axes.

a = "[35,42]"
print(repr(eval(a)))

from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

c = (
    Map()
    .add("商家A", [list(z) for z in zip(Faker.guangdong_city, Faker.values())], "广东")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Map-广东地图"), visualmap_opts=opts.VisualMapOpts()
    )
    .render("map_guangdong.html")
)

