# Author:Manni
# -*- coding = utf-8 -*-
# @Time :11:36 AM
# @Author:manniau
# @Site : 
# @File : sogou.py
# @Software: PyCharm

#get data from sougou.com homepage

import requests
#write a main
if __name__ == '__main__':
    #1. direct url
    url='https://www.sogou.com/web'
    #update url var
    kw=input('Enter a word: ')
    param={
        'query':kw
    }
    #2. request
    #2.1 will get a response
    response=requests.get(url=url,params=param)
    #3. get data (text as str)
    page_text=response.text
    print(page_text)
    fileName=kw+'.html'
    #save
    with open(fileNAme,'w',encoding='utf-8') as fp:
        fp.write(page_text)
    print(fileName,'crawler done!!!')



