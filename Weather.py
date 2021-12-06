# -*-coding:utf-8-*-
# @author: "andyxk"
# @Time: 2021-12-06 12:46
# @File: tcwetaher.py


import requests
from bs4 import BeautifulSoup
import re
import datetime


'''一个微信推送天气的程序。'''
'''
本程序最终使用腾讯云函数，并使用了server酱（https://sct.ftqq.com/）可以实时的把天气推送到微信上。
'''



r = requests.get("http://www.weather.com.cn/weather/101111001.shtml")     ## get 请求指定的页面信息
statue = r.status_code  # 检查状态码是否正确，状态为 200，说明访问成功
print("连接服务器状态：%s"%statue)
print("")
r.encoding = r.apparent_encoding  # 转换成 utf-8 的编码

html = r.text  # 获取页面内容

soup = BeautifulSoup(html, "html.parser")   #解析网页


# print(soup)
'''获取并分析数据'''
lv3_tag = soup.find_all('li',attrs={"class":"sky skyid lv3"})
lv2_tag = soup.find_all('li',attrs={"class":"sky skyid lv2"})
for i in lv3_tag:
    # print(lv3_tag)
    pass
for x in lv2_tag:
    # print(lv2_tag)
    pass



'''获取日期标题'''
dateList = []
dateTitle = soup.find_all('h1')
title = re.compile(r'<h1>(.*?\（.*?\）)</h1>')
for q in dateTitle:
    q = str(q)  #转为字符串
    dateR = re.findall(title,q)
    # print(dateR)
    for v in dateR:
        # print(v,end="")      #打印标题
        dateList.append(v)
    print()


'''获取天气情况'''
weatherList = []
dateTitle = soup.find_all("p",attrs={'class':'wea'})
title = re.compile(r'<p class="wea" title="(.*?)">')
for z in dateTitle:
    z = str(z)  #转为字符串
    weatherR = re.findall(title,z)
    # print(weatherR)
    for s in weatherR:
        # print(s,end="")      #打印标题
        weatherList.append(s)
    print()


'''获取最高温度'''
maxTempList = []
maxTemp = soup.find_all('span')
maxtemp_re = re.compile(r'<span>(\d|\d\d)</span>')
for d in maxTemp:
    d = str(d)  #转为字符串
    tempmax = re.findall(maxtemp_re,d)
    for dd in tempmax:
        # print(dd,end="")      #打印标题
        maxTempList.append(dd)
    print()



'''获取最低温度'''
minTempList = []
minTemp = soup.find_all('i')
mintemp_re = re.compile(r'<i>(\d\℃|\d\d\℃|-\d\℃|-\d\d\℃)</i>')
for min in minTemp:
    min = str(min)  #转为字符串
    tempmin = re.findall(mintemp_re,min)
    for nn in tempmin:
        # print(dd,end="")      #打印标题
        minTempList.append(nn)
    print()

'''server酱'''
sendKey = "SCT10137sd4as5d4s5a46d5s65othOOy7m0x49"  #输入自己的server酱的key
# 获取现在时间
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
scurl = f"https://sc.ftqq.com/{sendKey}.send"
page_re = re.compile(r'<a href="/f/like/mylike?&amp;pn=(.*?)">(.*?)</a>')


'''最终结果'''
def tcwetaher(nowtime):
    i = 0
    while i < len(dateList):
        # print("铜川：" + dateList[i] + "的天气：" + weatherList[i] + " | " + "温度是：" + maxTempList[i] + "/" + minTempList[i])
        '''server酱推微信送到手机'''
        params = {
            'text':"铜川:" + dateList[i] + "的天气：" + weatherList[i] + " | " + "温度是：" + maxTempList[i] + "/" + minTempList[i],
            'desp':"时间" + str(nowtime)
        }
        requests.post(scurl, params=params)
        i += 1


'''提醒：main(a,b)上传腾讯云函数加入a,b才不会报错，本地运行是会报错，需要修改程序。但是云函数不会'''
def main(a,b):
    tcwetaher(nowtime=nowtime)




if __name__ == '__main__':
    main()

