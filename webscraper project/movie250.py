# Author:Manni
# -*- coding = utf-8 -*-
# @Time :2020/8/1 9:48 PM
# @Author:manniau
# @Site : 
# @File : movie250.py
# @Software: PyCharm

import urllib.request,urllib.error,urllib.parse
import re,sqlite3,sys,os,xlwt,ssl
from bs4 import BeautifulSoup

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

def main():
    base:
    #save
    savepath=''
    saveDataDB()

    find

def getData(baseurl):

def main():
    baseurl = 'https://movie.douban.com/top250?start='
    #1.get site
    datalist=getData(baseurl)
    #save
    savepath='豆瓣Top250.xls'
    #dbpath='movie2.db'
    saveData(datalist,savepath)
    #saveData2DB(datalist,dbpath)

    findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则(字符串的模式)
    # 影片图片
    findImgsrc = re.compile(r'<img.* src="(.*?)"', re.S)  # re.S让换行符包括在字符中
    # 影片片名
    findTitle = re.compile(r'<span class="title">(.*)</span>')
    # 影片评分
    findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
    # 影片评价人数
    findNum = re.compile(r'<span>(\d*)人评价</span>')
    # 影片概况
    findContent = re.compile(r'<span class="inq">(.*)</span>')
    # 找到影片的相关内容
    findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


def getData(baseurl):
    datalist = []
    # 2.逐一解析数据
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)

        # 逐一解析数据
        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("div", class_="item"):  # 查找符合要求的字符串，形成列表
            # print(item) #测试;查看电影item全部信息
            data = []  # 保存一部电影的全部信息
            item = str(item)

            # re库通过正则表达式查找指定字符串
            link = re.findall(findLink, item)[0]
            data.append(link)  # 添加影片链接

            img = re.findall(findImgsrc, item)
            data.append(img)  # 添加影片图片

            title = re.findall(findTitle, item)
            if (len(title) == 2):
                data.append(title[0])  # 添加影片中文名
                otitle = title[1].replace("\xa0/\xa0", "")  # 去掉外文电影名中的\符号
                data.append(otitle)  # 添加影片外文名
            else:
                data.append(title)
                data.append(" ")

            rating = re.findall(findRating, item)[0]
            data.append(rating)  # 添加影片评分

            num = re.findall(findNum, item)[0]
            # print(type(num))
            data.append(num)  # 添加影片评分人数

            content = re.findall(findContent, item)
            if len(content) != 0:
                content = content[0].replace("。", "")
                data.append(content)  # 添加影片概述
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?", " ", bd)  # 去掉</br>
            bd = re.sub("/", " ", bd)
            data.append(bd.strip())  # 添加影片详情
            datalist.append(data)
        # print(datalist)
    return datalist

def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}  # 设置请求头，模拟浏览器向服务器发请求，并且让服务器知道我们浏览器的版本
    req=urllib.request.Request(url=url,headers=head)
    response=urllib.request.urlopen(req)
    html=response.read().decode('utf-8')
    print(html)
    return html


def saveData(datalist,savepath):
        book = xlwt.Workbook(encoding="utf-8")  # 创建workbook对象
        sheet = book.add_sheet("豆瓣电影top250", cell_overwrite_ok=True)  # 创建工作表
        col = ("电影详情链接", "图片链接", "影片中文名", "影片外文名", "评分", "评分人数", "概况", "相关信息")
        for i in range(0, 8):
            sheet.write(0, i, col[i])  # 列名
        print("save")
        for i in range(1, 251):
            print("第%d条数据" % i)
            for j in range(0, 8):
                sheet.write(i, j, datalist[i - 1][j])
        book.save(savepath)

def saveData2DB(datalist,dbpath):
    pass

def init_db(dbpath):
    sql='''
        create table movie250 #创建数据表
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar,
        ename varchar,
        score numeric,
        rating numeric,
        introduction text,
        info text,
        )
    '''

    conn=sqlite3.connect(dbpath)
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveDataDB(datalist,dbpath):
    init_db(dbpath)
    conn=sqlite3.connect(dbpath)
    curser=conn.cursor();
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index]=str(data[index])  #这句话大家可以删了试试，有的会出现list无法转换到str类型的错误，也是博主遇到的一个小bug
            data[index] = '"' + data[index] + '"'
        sql = '''
                insert into movie250 (
                info_link,pic_link,cname,ename,score,rated,instroduction,info) 
                values(%s)''' % ",".join(data)
        print(sql)
        curser.execute(sql)
        conn.commit()
    curser.close()
    conn.close()

if __name__ == '__main__':
    main()