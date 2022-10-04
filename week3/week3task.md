## 第三周作业 20377019 詹嘉杰 

**代码：**

```python
import string
import webbrowser
import pandas as pd
import re
import jieba
import datetime
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from math import radians,sin,cos,asin,sqrt
from pyecharts.charts import Geo
from pyecharts import options as opts
from pyecharts.globals import GeoType
from pyecharts.globals import ChartType, SymbolType

def read_text(filename):
    '''
    读入数据
    '''
    file = pd.read_csv(filename,sep='\t')
    return file

def url_clean(text):
    '''
    清洗url
    '''
    cleantext = []
    for line in text:
        x = re.sub(r'^(https:\S+)', ' ',line)
        x = re.sub(r'[a-zA-Z]+://[^\s]*', '',x)
        cleantext.append(x)
    return cleantext

def emotionjudge():
    '''
    判断情绪
    '''
    with open("anger.txt",'r',encoding='utf-8') as file:
        anger = file.read()
    with open("disgust.txt",'r',encoding='utf-8') as file:
        disgust = file.read()
    with open("fear.txt",'r',encoding='utf-8') as file:
        fear = file.read()
    with open("joy.txt",'r',encoding='utf-8') as file:
        joy = file.read()
    with open("sadness.txt",'r',encoding='utf-8') as file:
        sadness = file.read()
    jieba.load_userdict("anger.txt")
    jieba.load_userdict("disgust.txt")
    jieba.load_userdict("fear.txt")
    jieba.load_userdict("joy.txt")
    jieba.load_userdict("sadness.txt")
    def judge(sentance):
        nonlocal anger,disgust,fear,joy,sadness
        sentance = jieba.lcut(sentance)
        emo = [0,0,0,0,0]
        for word in sentance:
            if word in anger:
                emo[0]+=1
            elif word in disgust:
                emo[1]+=1
            elif word in fear:
                emo[2]+=1
            elif word in joy:
                emo[3]+=1
            elif word in sadness:
                emo[4]+=1
            else:
                continue
        if (sorted(emo)[4]==sorted(emo)[3]):
            return "none"
        else:
            loc = emo.index(max(emo))
            if (loc == 0):
                return "anger"
            elif (loc == 1):
                return "disgust"
            elif (loc == 2):
                return "fear"
            elif (loc == 3):
                return "joy"
            elif (loc == 4):
                return "sadness"
    return judge

def time_convert(data):
    '''
    将文本转化为时间格式，返回所有时间组成的列表
    '''
    timelist = []
    format = '%a %b %d %H:%M:%S %Y'
    for line in data["weibo_created_at"]:
        time = line.replace('+0800 ', '')
        time = datetime.datetime.strptime(time,format)
        timelist.append(time)
    return timelist

def emotion_mode(data,emotion,time):
    '''
    情绪变化模式
    '''
    if (time == "hour"):
        emo = [0]*24    
        for line in data[data["emotion"]==emotion]["time"]:
            emo[line.hour]+=1
    elif time == "week":
        emo = [0]*7
        for line in data[data["emotion"]==emotion]["time"]:
            emo[line.weekday()]+=1
    return emo

def emotion_image(emotionmode):
    '''
    把情绪随时间变化图绘制出来
    '''
    fig,ax = plt.subplots()
    ax.plot(emotionmode)
    plt.show()

def haversine_dis(loc1,loc2):
    '''
    由经纬度计算地理距离
    '''
    #将十进制转为弧度
    lon1, lat1, lon2, lat2 = map(radians, [loc1[0], loc1[1], loc2[0], loc2[1]])
    #haversine公式
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    aa = sin(d_lat/2)**2 + cos(lat1)*cos(lat2)*sin(d_lon/2)**2
    c = 2 * asin(sqrt(aa))
    r = 6371 # 地球半径，千米
    return c*r #千米

def emotion_circle(data,emotion,loc):
    '''
    围绕某个中心点,随着半径增加该情绪所占比例的变化,每5公里分界一次,50公里以外统一归进50公里,loc为中心点所在经纬度的列表
    '''
    emo = [0]*11
    centerloc = loc
    for line in data[data["emotion"]==emotion]["location"]:
        wbloc = eval(line)
        
        dis = haversine_dis(wbloc,centerloc)
        if ((dis/5)>10):
            emo[10]+=1
        else:
            emo[int(dis/5)]+=1
    return emo

def emotion_map(data):
    '''
    在地图上显示出微博情绪分布图
    '''
    geo = Geo(init_opts=opts.InitOpts(width="600px",height="400px",bg_color="white"))
    geo.add_schema(maptype='北京')
    loc = list(data['location'])
    emotion = list(data['emotion'])
    emo_tuple = []

    for i in range(len(emotion)):
        emo_tuple.append(tuple([emotion[i]+str(i),1]))
    for i in range(len(emotion)):
        emo_loc = eval(loc[i])
        geo.add_coordinate(name=emotion[i]+str(i),latitude=emo_loc[0],longitude=emo_loc[1])
        if emotion[i]=="anger":
            geo.add('',[emo_tuple[i]], type_=GeoType.EFFECT_SCATTER, symbol_size=5,color="red")
        elif emotion[i]=="disgust":
            geo.add('',[emo_tuple[i]], type_=GeoType.EFFECT_SCATTER, symbol_size=5,color="green")
        elif emotion[i]=="fear":
            geo.add('',[emo_tuple[i]], type_=GeoType.EFFECT_SCATTER, symbol_size=5,color="blue")
        elif emotion[i]=="joy":
            geo.add('',[emo_tuple[i]], type_=GeoType.EFFECT_SCATTER, symbol_size=5,color="yellow")
        elif emotion[i]=="sadness":
            geo.add('',[emo_tuple[i]], type_=GeoType.EFFECT_SCATTER, symbol_size=5,color="grey")
        else:
            continue
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False,font_size=10,position="top"))
    geo.set_global_opts(title_opts=opts.TitleOpts(title="情绪分布图"))
    image=geo.render("emotionmap.html")
    webbrowser.open(image)
    return image
    
        

#main
data = read_text("weibo.txt")
text = data['text']
print(repr(text))
cleantext = url_clean(text[0:100000])
print(cleantext)
#判断情绪
emojudge = emotionjudge()
emodf = []
for line in cleantext:
    emodf.append(emojudge(line))
emodf = pd.DataFrame(emodf,columns=['emotion'])
data1 = pd.concat([data[0:100000],emodf],axis=1)
data1 = pd.concat([data1,pd.DataFrame(time_convert(data1),columns=["time"])],axis=1)
print(repr(data1))
#情绪半径分布
emomatrix = emotion_circle(data1,'anger',[39.5427,116.2317])
print(emomatrix)
#情绪模式
anger = emotion_mode(data1,"anger","hour")
sad = emotion_mode(data1,"sadness","week")
emotion_image(anger)
emotion_image(sad)
#地理分布
emotion_map(data1[0:10000])
```

1.读入数据并去除噪声

![image-20220925185317194](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220925185317194.png)

去除url后的结果

![image-20220925185421518](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220925185421518.png)

2.情绪判断

![image-20220925185459999](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220925185459999.png)

采用情绪词最多的一类情绪作为此条文本的情绪，并将情绪判断的结果与读入的结果拼接

3.情绪变化模式

可以通过输入情绪的名称和“hour"或”week“来分别获得不同情绪的小时模式或周模式

下图是anger 的小时模式变化

![情绪变化模式](C:\Users\ASUS\Desktop\study\2022py\w3\情绪变化模式.png)

下图是sadness的周模式变化

![sad](C:\Users\ASUS\Desktop\study\2022py\w3\sad.png)

4.空间分布

我设置以天安门为中心，每5公里分界一次，可以输入情绪名称，计算距离天安门不同半径的情绪分布

以下是anger 的半径分布

![image-20220925185624678](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220925185624678.png)

下图是利用pyechart标注出的不同情绪所在位置，以北京市地图作为背景，不同颜色代表不同情绪，由于数量太多会卡，就选择了前1000条文本的数据绘图为例

![image-20220925190219425](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220925190219425.png)

5.情绪词典的优点是采取分词并对词语进行分类，这样非常快捷，且情绪词典可以进行调整，随时更新最新的情绪词汇。但缺点也在此，只能根据句子中的包含的情绪词语来分类，而不能准确理解句意，所以不能保证整个句子的准确性。

​	如果想要扩充词典来提升精确度的话，可以通过已经划分情绪的句子，将其句子中的一些不包含在情绪词典的高频词加入该情绪的情绪词典，比如划定为愤怒的句子中很多都包含“生气”，而情绪词典中又没有“生气”这个词语，就可以自动将“生气”加入情绪词典中。

6.

可视化结果已在3、4中给出

7.情绪时空模式的意义：首先是在城市管理方面，如果在愤怒情绪比较严重的区域，可以看看愤怒聚集的时间段是否发生了某些影响人民生活的时期，例如晚上八九点钟在广场上总是有大声跳广场舞的，可能这个时间这个地点的愤怒情绪就会聚集，此时可以派人进行引导，防止扰民现象。其次是营销方面，例如酒吧的选址，就可以选择夜晚悲伤情绪较为严重的区域，或许能提升客流量。