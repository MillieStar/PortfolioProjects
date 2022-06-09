# Author:Manni
# -*- coding = utf-8 -*-
# @Time :10:09 AM
# @Author:manniau
# @Site : 
# @File : baitran.py
# @Software: PyCharm
import requests
import json
'''
XMLHttpRequest (XHR) is an API in the form of an object 
whose methods transfer data between a web browser and a web server. 
The object is provided by the browser's JavaScript environment.
'''
if __name__ == '__main__':

    #UA
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    #part of the page - ajax - XHR
    #post same as get
    post_url='https://fanyi.baidu.com/sug'
    #sep data
    word=input('enter a word: ')
    data={
        'kw':word}

    #request get
    response=requests.post(url=post_url,data=data,headers=head)
    #get data - json() return obj - (dict)
    dic_obj=response.json()
    print(dic_obj)
    #save as json
    fileName=word+'.json'
    fp=open(fileName,'w',encoding='utf-8')
    json.dump(dic_obj,fp=fp,ensure_ascii=False)

    print('done!!!')



import re, js2py, requests

class BaiduFanyi(obj):

    def __init__(self,kw):
        #:param keywords:待检测语言

        self.kw=kw
        self.url_root='http://fanyi.baidu.com/'  # 翻译根url
        self.url_langdetect='https://fanyi.baidu.com/langdetect'
        self.url_trans='https://fanyi.baidu.com/v2transapi'

        self.head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                                 'origin': 'https://fanyi.baidu.com',
                                'referer': 'https://fanyi.baidu.com/?aldtype=16047'
        }

        self.data_langdetect={
            'query':self.kw}

        self.session=requests.sessions()
        self.session.head=self.head
        self.context=js2py.eval_js()




