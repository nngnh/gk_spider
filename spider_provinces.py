# -*- coding: utf-8 -*-
"""
@Time ： 2020/6/24 下午8:21
@Auth ： LX
@File ：spider_provinces.py
@IDE ：PyCharm
@DES :  爬取省份
"""
from urllib import request
import json
import csv
import time
#把字符串转换为json，只返回数据部分
def str2json(str):
    data = json.loads(str)
    data = data['data']
    return data

#获取页面数据
def get_page_data(url,headers):
    req = request.Request(url=url,headers=headers)
    response = request.urlopen(req)
    if response.getcode() == 200:
        #这里获取到的是bytes类型
        result = response.read()
        result = str(result,encoding='utf-8')
        # print(result)
        return str2json(result)
    else:
        print("请求失败")


#爬取省份
def spider_universities_info():
    url = 'https://in985.com/api/v1/address/provinces'
    headers = {
        'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592273437,1592354849,1592401952,1592470252; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592481766',
        # 'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592359019',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'referer':'https://www.in985.com/dataCenter/scoreLine/collegeAdmissions',
        #理科
        'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw'
        # 'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg',
    }
    #获得学校的信息，str格式
    provinces_json = get_page_data(url,headers)

    f = open('province.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    i = 0
    for province in provinces_json:
        province_list = []
        provinceName = province['provinceName']
        province_list.append(provinceName)
        csv_writer.writerow(province_list)
        i += 1
        print(i)

    f.close()
    print("done")






if __name__ == '__main__':
    spider_universities_info()
