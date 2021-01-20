#!/usr/bin/env python
# coding: utf-8

# In[2]:


# 网络文献标题抓取器
# Written by yecy

# 2021-01-20 ver 2.0
# 增加对Elsevier的支持，优化交互及使用体验

# 2020-04-28 ver 1.0
# 实现抓取Wiley文献标题并提供翻译

from requests_html import HTMLSession
import requests
import pandas as pd
import json


# In[3]:


def get_titles(sel):
    titles = []
    try:
        results = rec.html.find(sel)
        for result in results:
            get_title = result.text
            titles.append(get_title)
        return titles
    except:
        return None


# In[4]:


# 有道翻译
# edited from https://blog.csdn.net/qq_36771895/article/details/90510742
    
def translator(str):
    """
    input : str 需要翻译的字符串
    output：translation 翻译后的字符串
    """
    # API
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=null'
    # 传输的参数， i为要翻译的内容
    key = {
        'type': "AUTO",
        'i': str,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "ue": "UTF-8",
        "action": "FY_BY_CLICKBUTTON",
        "typoResult": "true"
    }
    # key 这个字典为发送给有道词典服务器的内容
    response = requests.post(url, data=key)
    # 判断服务器是否相应成功
    if response.status_code == 200:
        # 通过 json.loads 把返回的结果加载成 json 格式
        result = json.loads(response.text)
#         print ("输入的词为：%s" % result['translateResult'][0][0]['src'])
#         print ("翻译结果为：%s" % result['translateResult'][0][0]['tgt'])
        translation = result['translateResult'][0][0]['tgt']
        return translation
    else:
        # 相应失败就返回空
        return None


# In[5]:


def get_translations(titles):
    results = []
    for title in titles:
        trans_results = translator(title)
        results.append(trans_results)
    return results


# In[6]:


session = HTMLSession()
url = input('Enter the URL of the page you want to grab from: ') # Need to be edited
rec = session.get(url)
# print(rec.html.text)
# print(rec.html.links)


# In[7]:


if 'wiley' in url:
    sel = '#main-content > div.page-body.pagefulltext > div > section > div > div > div > div.main-content.col-md-8 > div.toc-wrapper > div.table-of-content > div > div > div > a > h2'
elif 'sciencedirect' in url:
    sel = '#article-0 > ol > li > dl > dt > h3 > a > span > span'
# 根据不同页面相应修改

results = rec.html.find(sel)
# results


# In[8]:


# print(get_titles(sel))
titles = get_titles(sel)
check = input('Translate?(Y or N)')
while 1:
    if check == 'Y':
        translations = get_translations(titles)
        df = pd.DataFrame({'English': titles, 'Chinese': translations})
        break
    elif check == 'N':
        df = pd.DataFrame(titles)
        break
    else:
        print('Please enter Y or N')

# df


# In[9]:


# output
df.to_excel('article_grab.xlsx')

