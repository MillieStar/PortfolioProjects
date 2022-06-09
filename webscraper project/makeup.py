# Author:Manni
# -*- coding = utf-8 -*-
# @Time :11:16 AM
# @Author:manniau
# @Site : 
# @File : makeup.py
# @Software: PyCharm
import requests, json


if __name__ == '__main__':
    index_url = 'http://scxk.nmpa.gov.cn:81/xk/'
    url='http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList'
    post_url='http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
    #detail_url='http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById'
    head = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

    id_list = []
    all_data_list = []  # save all bus info

    for page in range(1,6):
        page=str(page)
        data={
            'on':'true',
            'page': page,
            'pageSize':' 15',
            'productName':'',
            'conditionType':' 1',
            'applyname':'',
            'applysn':'',
        }
        json_ids = requests.post(url=url, data=data, headers=head).json()


    # page_text=requests.post(url=url,data=data,headers=head).text

    # with open('./makeup.html','w',encoding='utf-8') as fp:
    #     fp.write(page_text)
    # fp=open('./id.json','w',encoding='utf-8')
    # json.dump(json_ids,fp=fp,ensure_ascii=False)
    # print('done!!!')
    #for every dic in ['list'] in json_ids


        for dic in json_ids['list']:
            id_list.append(dic['ID'])
    # print(id_list)
    #get company info
    for id in id_list:
        data={
            'id':id
        }
        detail_json=requests.post(url=post_url,data=data,headers=head).json()
        # fp=open('./detail.json','w',encoding='utf-8')
        # json.dump(detail_json,fp=fp,ensure_ascii=False)
        # print(detail_json,'________End____________')
        #get bus license number
        all_data_list.append(detail_json)
        #save
        fp=open('./allData.json','w',encoding='utf-8')
        json.dump(all_data_list,fp=fp,ensure_ascii=False)
    print('done!!!')
        # count=0
        #
        # for num in id['businessLicenseNumber']:
        #
        #     count+=1
        #     print('No. '+count+' is: '+num)













'''
'''

    # url='http://125.35.6.84:81/xk/'
    #
    # index_url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsList'
    #
    # detail_url = 'http://125.35.6.84:81/xk/itownet/portalAction.do?method=getXkzsById'
    #
    #
    # head = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    #
    # data={
    #     'on': 'true',
    #     'page': '1',
    #     'pageSize': '15',
    #     'productName': '',
    #     'conditionType': '1',
    #     'applyname': '',
    #     'applysn': ''
    # }
    # # page_text=requests.get(url=url,headers=head)
    #
    # list=requests.post(index_url,data=data).json.get('list')
    #
    # def write(pro_name, text):
    #     with open(f'{pro_name}.json','w',encoding='utf-8') as f:
    #         f.write(text)
    #
    # for pro in list:
    #     res=requests.post(url=detail_url,data={'id':pro.get{'ID'}},headers=headers)
    #     write(pro.get('EPS_NAME'),res.text)



