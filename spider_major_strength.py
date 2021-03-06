# -*- coding: utf-8 -*-
"""
@Time ： 2020/6/17 上午11:33
@Auth ： LX
@File ：spider_major_strength.py
@IDE ：PyCharm
@DES : 爬取专业实力
"""
from urllib import request
import json
import csv
import time

headers = {
        'Cookie':'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjM5NjY4MCwiSWF0IjoxLCJKdGkiOiIxOTY0NTk4MzgifQ.4BYvfo-ortjSyCSArWLaQQJLgRwm_Uw15OIiK1PJ7x0; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592361159',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'referer':'https://www.in985.com/dataCenter/collegeLib',
        'authorization':'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjM5NjY4MCwiSWF0IjoxLCJKdGkiOiIxOTY0NTk4MzgifQ.4BYvfo-ortjSyCSArWLaQQJLgRwm_Uw15OIiK1PJ7x0',
    }
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

#返回学校的code
def spider_universities_info():
    url = 'https://in985.com/api/v1/college/query?ProvinceIds=&Categorys=&PlanOrders=&Properties=&Levels=&Keyword=&PageIndex=1&PerPageSize=2400&sort='
    #获得学校的信息，str格式
    universities_json = get_page_data(url,headers)
    universities_json = universities_json['items']
    #用于保存universityCode
    universities_code_list = []
    for universitiy in universities_json:
        #以下字段都是点击详情所需要的
        collegeCode = universitiy['code']
        universities_code_list.append(collegeCode)
    return universities_code_list

def spider_universities_detali():
    f = open('major_strength.csv', 'w', encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["collegeCode","collegeName","specialtyCode","speicaltyName","specialtyPlace","specialtyComment","collegeCount","isKeyConstruction","specialtyLevelName"])
    universities_code_list = spider_universities_info()
    i = 0
    j = 0
    for collegeCode in universities_code_list:
        url='https://in985.com/api/v1/college/specialties/'+collegeCode+'?Keyword=&PageIndex=1&PerPageSize=1000&Sort='
        university_json = get_page_data(url,headers)
        #获取学校名称
        url1 = 'https://in985.com/api/v1/college/detail/'+collegeCode
        data = get_page_data(url1,headers)
        name = data['name']
        if university_json['totalItems'] > 0:
            marjors_info = university_json['items']
            for marjor_info in marjors_info:
                data = []
                collegeCode = marjor_info['collegeCode']
                specialtyCode = marjor_info['specialtyCode']
                speicaltyName = marjor_info['speicaltyName']
                specialtyPlace = marjor_info['specialtyPlace']
                specialtyComment = marjor_info['specialtyComment']
                collegeCount = marjor_info['collegeCount']
                isKeyConstruction = marjor_info['isKeyConstruction']
                data.append(collegeCode)
                data.append(name)
                data.append(specialtyCode)
                data.append(speicaltyName)
                data.append(specialtyPlace)
                data.append(specialtyComment)
                data.append(collegeCount)
                data.append(isKeyConstruction)
                #获取本科还是专科
                url = 'https://in985.com/api/v1/specialties/introduction/'+specialtyCode
                json_data = get_page_data(url,headers)
                if json_data is None:
                    specialtyLevelName = None
                else:
                    specialtyLevelName = json_data['specialtyLevelName']
                data.append(specialtyLevelName)
                i += 1
                csv_writer.writerow(data)
                print(i)
        else:continue
    f.close()
    print("done")
if __name__ == '__main__':
    spider_universities_detali()