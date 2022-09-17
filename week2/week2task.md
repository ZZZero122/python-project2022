## 第二周作业 20377019 詹嘉杰

##### 代码

```python
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

#选取了四条弹幕并计算他们之间的欧式距离
sen_dist(data1[5162],data1[5165],matrix[5162],matrix[5165])
sen_dist(data1[5151],data1[6817],matrix[5151],matrix[6817])

#TF-IDF提取关键词
text = ','.join(data1.tolist())
jieba.analyse.set_stop_words("stopwords_list.txt")
worddic = tfidf(text)

#生成词云
word_cloud(filtered_words)
```



##### 1.读入数据并分词

![image-20220911231259485](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220911231259485.png)



##### 2.过滤停用词后统计词频

由于处理时间过长就选取了前十万条弹幕

![image-20220917230539748](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220917230539748.png)



##### 3.将词频小于5的词删除

![image-20220917230623362](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220917230623362.png)



##### 4.为弹幕生成向量表示

以前1000条弹幕为例：为每条弹幕创建一个向量，当特征词出现时为1，未出现为0，组成矩阵

![image-20220912230408667](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220912230408667.png)

可以看到视频刚开始大家会发一些“x小时前”的消息，所以小时为最高频的词，而矩阵中第一列的1出现的行数也与“小时”出现在弹幕中的所在行一致。



##### 5.向量表示计算欧式距离

![image-20220917230635308](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220917230635308.png)

我选取了四条弹幕，分别是：

5163  牛杂汤里面萝卜才是亮点啊

5166 吃牛杂我也喜欢吃萝卜！

5152 牛腩煲里萝卜才是主角！！！

6818 武汉吃烧烤，要蒜。老板说不知道什么是蒜

而前两条的欧式距离小于后两条，则前两条的句意之间相似度比较大，而后两条的句意就完全不同。所以有可能选出最有代表性的弹幕

但这一方法还是依靠所包含的特征词差距来大概区分句意，无法对语意进行具体的分析，例如“喜欢吃萝卜”与“不喜欢吃萝卜”在这种判断方式中会被判断为句意一致。



##### 6.词云图

![词云图](C:\Users\ASUS\Desktop\study\2022py\w2\词云图.jpg)

##### 7.TFIDF特征词对比

对前10000条弹幕处理

这是词频统计结果：

![image-20220917230708218](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220917230708218.png)

这是TFIDF特征词结果：

![image-20220917230651316](C:\Users\ASUS\AppData\Roaming\Typora\typora-user-images\image-20220917230651316.png)

可以看出特征词的排名发生了较大的变化，“啊啊啊”的排名大幅提升，我认为是因为大家对于在弹幕中经常重复打出很多个“啊”，而且一般单独出现在一条弹幕中，不结合其他词语，使tfidf值提高。但总体出现的特征词依旧与高频词差不多，只是排序变化较大。

我认为TFIDF与词频相比，以词频统计的结果更好一些，因为弹幕普遍较短，且大家会经常重复同一句话在弹幕中，比如“哈哈哈”“啊啊啊”之类的，这时TFIDF会提高这些词的排名，但这些词并不能代表所有弹幕的内容，只能作为一个标准来区别具有真实内容的弹幕和多含重复的弹幕。
