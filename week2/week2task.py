from audioop import reverse
from ctypes import sizeof
from fileinput import filename
from pydoc import describe
from warnings import filterwarnings
import pandas as pd
import jieba
import collections
import wordcloud
import numpy as np
import jieba.analyse

#取出的弹幕数
dmnum = 100000

def read_csvfile(csvname):
    '''
    运用pandas读取csv文件中的content
    '''
    data = pd.read_csv(csvname)
    data1 = data['content']
    data1 = data1.head(dmnum)
    return data1

def filter_stopword(stwdname,words):
    '''
    读入停用词并筛选
    '''
    with open(stwdname,'r',encoding='utf-8') as file2:
        stop_words = file2.read()
    filtered_words = [word for word in words if word not in stop_words]
    return filtered_words

def split_word(data):
    '''
    分词
    '''
    jieba.load_userdict("stopwords_list.txt")
    wordlist = []
    for line in data:
        wordlist += jieba.lcut(str(line))
    return wordlist

def word_count(words):
    '''
    统计词频并删去词频小于5的词
    '''
    freq=collections.Counter(words)
    print("\n词频")
    print(freq)
    hifreqwords = {}
    for k in freq.keys():
        if (freq[k]>5):
            hifreqwords[k]=freq[k]
    #转换为字典按值排序
    hifreqwords = dict(sorted(hifreqwords.items(),key=lambda x:x[1],reverse = True))
    print("\n高频词")
    print(hifreqwords)
    return freq,hifreqwords


def words_matrix(data,hifreqwords):
    '''
    通过高频词来为每条弹幕生成向量表示，并组成一个向量矩阵
    '''
    speset = list(hifreqwords.keys())
    length = len(speset)
    matrix = np.zeros((dmnum,length))
    for i in range(dmnum):
        spl = jieba.lcut(str(data1[i]))
        for j in range(length):
            if speset[j] in spl:
                matrix[i][j] = 1
            else:
                continue
    return matrix

def sen_dist(x,y,x1,y1):
    '''
    计算弹幕间的欧氏距离
    '''
    dist1 = np.sqrt(sum((x1-y1)**2))
    print("'" + str(x) + "'和'" + str(y) + "'"+"的距离是%.2f"%dist1)
    return

def tfidf(text):
    '''
    使用tfidf方法提取特征词
    '''
    tags = jieba.analyse.extract_tags(text,withWeight = True)
    worddic = {}
    for i in tags:
        worddic[i[0]]=i[1]
    print("\nTFIDF特征词")
    print(worddic)
    return worddic

def word_cloud(words):
    '''
    生成词云图
    '''
    wordtxt = " ".join(words)
    cloud = wordcloud.WordCloud(font_path="STFANGSO.TTF",background_color='white',collocations=False,width=800,height=600,max_font_size=200)
    cloud.generate(wordtxt)
    cloud.to_file("词云图.jpg")


#读入数据
data1 = read_csvfile('danmuku.csv')

#导入自定义字典
jieba.load_userdict("stopwords_list.txt")

#分词
words = split_word(data1)
print(words)

#去除停用词
filtered_words = filter_stopword("stopwords_list.txt",words)

#统计词频
freq,hifreqwords = word_count(filtered_words)

matrix = words_matrix(data1,hifreqwords)

#计算弹幕欧式距离
sen_dist(data1[5162],data1[5165],matrix[5162],matrix[5165])
sen_dist(data1[5151],data1[6817],matrix[5151],matrix[6817])

#TF-IDF提取关键词
text = ','.join(data1.tolist())
jieba.analyse.set_stop_words("stopwords_list.txt")
worddic = tfidf(text)

#生成词云
word_cloud(filtered_words)
