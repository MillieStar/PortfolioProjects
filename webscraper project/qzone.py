# Author:Manni
# -*- coding = utf-8 -*-
# @Time :7:23 PM
# @Author:manniau
# @Site : 
# @File : qzone.py
# @Software: PyCharm
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions

# bro=webdriver.Chrome(executable_path='./chromedriver')
# bro.get('https://qzone.qq.com')
#
# bro.switch_to.frame('login_frame')
# a_tag=bro.find_element_by_id('switcher_plogin')
# a_tag.click()
#
# #username
# userName_tag=bro.find_element_by_id('u')
# #password
# password_tag=bro.find_element_by_id('p')
# sleep(1)
# userName_tag.send_keys('1669636301')
# sleep(1)
# password_tag.send_keys('deathcabforcutie')
# sleep(1)
# btn=bro.find_element_by_id('login_button')
# btn.click()
#
# sleep(3)
# bro.quit()

#no head
#无可视化界面（无头） phantomJs

chrome_options=Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

#如何实现让selenium规避被检测的风险
option=ChromeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])

# webdriver.phantomjs
bro=webdriver.Chrome(executable_path='./chromedriver',chrome_options=chrome_options,options=option)



bro.get('https:www.baidu.com')
print(bro.page_source)
sleep(2)
bro.quit()




