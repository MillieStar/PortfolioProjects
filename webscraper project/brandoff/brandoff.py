# Author:Manni
# -*- coding = utf-8 -*-
# @Time :12:20 AM
# @Author:manniau
# @Site : 
# @File : brandoff.py
# @Software: PyCharm

from lxml import etree
import requests
# import ssl
from time import sleep
import csv
import pandas as pd

if __name__ == '__main__':
    # try:
    #     _create_unverified_https_context = ssl._create_unverified_context
    # except AttributeError:
    #     # Legacy Python that doesn't verify HTTPS certificates by default
    #     pass
    # else:
    #     # Handle target environment that doesn't support HTTPS verification
    #     ssl._create_default_https_context = _create_unverified_https_context

    url='https://tokyohk.brandoff.com.hk/hk/category/index.php?p=%d&category_id=181&num=30&range=0&item=&sort=0&brand=&rank=&key_sh=&min_price=&max_price='
    head={'user-agent':
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
    # url_list=[]
    num=int(input('Enter pages: '))
    for pageNum in range(1,num):
        new_url=format(url%pageNum)
        # url_list.append(new_url)
    # print(url_list)
    #     for url in url_list:
        page_text=requests.get(url=new_url,headers=head).text
        sleep(1)


        #etree
        # for url in url_list:
        tree=etree.HTML(page_text)

    # div_list=tree.xpath('//span[@class="block2"]')
    # for div in div_list:

        name_list=tree.xpath('.//span[@class="name1"]/text()')
        brand_list=tree.xpath('.//span[@class="name2"]/text()')
        rank_list=tree.xpath('.//span[@class="rank"]/text()')
        price_list=tree.xpath('.//span[@class="boff_val"]/text()')

        # Display Chinese correctly

        fp=open('./brandoff.csv','a', newline='',encoding='utf-8-sig')

        for bag in range(0,len(name_list)):
            data=[brand_list[bag], name_list[bag], rank_list[bag], price_list[bag]]
            print(brand_list[bag], name_list[bag], rank_list[bag], price_list[bag])
            # fp.write(brand_list[bag] + ' ' + name_list[bag] + ' ' + rank_list[bag] + ' ' + price_list[bag] + '\n')


            writer=csv.writer(fp)
            writer.writerow(data)




        print(type(name_list),name_list)




# df = pd.read_csv('./brandoff.csv')
# print(df)
