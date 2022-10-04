import re
from HTMLParser import HTMLParser

def dealHtmlTags(html):

    '''

    去掉html标签

    '''

    html=html.strip()

    html=html.strip("\n")

    result=[]

    parse=HTMLParser()

    parse.handle_data=result.append

    parse.feed(html)

    parse.close()

    return "".join(result)

def dealUrl(text):

    '''

    去掉微博信息中的url地址

    '''

    return re.sub('''http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+''', '',text)



html = "接下来一年，我希望在惠普电脑看到更人性化，各科技化的东西，更能提升视觉享受的东西。 地址：http://t.cn/8kUAX2z"

html = dealHtmlTags(html)

print(dealUrl(html))