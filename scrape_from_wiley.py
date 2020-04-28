#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 实现抓取Wiley文献标题并翻译
# Written by yecy
# 2020-04-28

from requests_html import HTMLSession
import requests
import pandas as pd
import json


# In[2]:


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


# In[3]:


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


# In[4]:


def get_translations(titles):
    results = []
    for title in titles:
        trans_results = translator(title)
        results.append(trans_results)
    return results


# In[5]:


session = HTMLSession()
url = 'https://onlinelibrary.wiley.com/toc/1099114x/2020/44/3' # Need to be edited
rec = session.get(url)
# print(rec.html.text)
# print(rec.html.links)


# In[6]:


sel = '#main-content > div.page-body.pagefulltext > div > section > div > div > div > div.main-content.col-md-8 > div.table-of-content > div > div > div > a > h2'
# Need to be edited

# results = rec.html.find(sel)
# results


# In[7]:


# print(get_titles(sel))
titles = get_titles(sel)
translations = get_translations(titles)


# In[8]:


df = pd.DataFrame({'English': titles, 'Chinese': translations})
# df


# In[9]:


# output
df.to_excel('wiley_scrape.xlsx')

