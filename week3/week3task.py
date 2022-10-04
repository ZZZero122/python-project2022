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