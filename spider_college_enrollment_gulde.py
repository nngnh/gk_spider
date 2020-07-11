# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/8 下午7:45
@Auth ： LX
@File ：spider_college_enrollment_gulde.py
@IDE ：PyCharm
@DES : 爬取学校招生简章
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

#返回学校的code
def spider_universities_info():
    '''
    获得学校code的list
    :return:
    '''
    url = 'https://in985.com/api/v1/college/query?ProvinceIds=&Categorys=&PlanOrders=&Properties=&Levels=&Keyword=&PageIndex=1&PerPageSize=2400&sort='
    headers = {
        'Cookie':'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjM5NjY4MCwiSWF0IjoxLCJKdGkiOiIxOTY0NTk4MzgifQ.4BYvfo-ortjSyCSArWLaQQJLgRwm_Uw15OIiK1PJ7x0; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592361159',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'referer':'https://www.in985.com/dataCenter/collegeLib',
        'authorization':'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjM5NjY4MCwiSWF0IjoxLCJKdGkiOiIxOTY0NTk4MzgifQ.4BYvfo-ortjSyCSArWLaQQJLgRwm_Uw15OIiK1PJ7x0',
    }
    #获得学校的信息，str格式
    universities_json = get_page_data(url,headers)
    universities_json = universities_json['items']
    #用于保存universityCode
    universities_code_list = []
    for universitiy in universities_json:
        #以下字段都是点击详情所需要的
        collegeCode = universitiy['code']
        universities_code_list.append(collegeCode)
    # print(universities_code_list)
    return universities_code_list

def spider_universitie_enrollment_gulde():
    f = open('universitie_enrollment_gulde.csv', 'w', encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["collegeCode","title","enrollmentGulde"])
    universities_code_list = spider_universities_info()
    i = 0
    for collegeCode in universities_code_list:

        url='https://in985.com/api/v1/college/rule/'+collegeCode
        # url='https://in985.com/api/v1/college/rule/0118'
        headers={
            'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjM5NjY4MCwiSWF0IjoxLCJKdGkiOiIxOTY0NTk4MzgifQ.4BYvfo-ortjSyCSArWLaQQJLgRwm_Uw15OIiK1PJ7x0; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592361159',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'referer': 'https://www.in985.com/dataCenter/scoreLine/collegeDetail',
            'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjM5NjY4MCwiSWF0IjoxLCJKdGkiOiIxOTY0NTk4MzgifQ.4BYvfo-ortjSyCSArWLaQQJLgRwm_Uw15OIiK1PJ7x0',
        }
        university_json = get_page_data(url,headers)
        if university_json is None:
            continue
        # time.sleep(1)
        data = []
        code = collegeCode
        title = university_json['title']
        enrollmentGulde = university_json['publisher']
        data.append(code)
        data.append(title)
        data.append(enrollmentGulde)
        i += 1
        # print(data)
        csv_writer.writerow(data)
        print(i)
    f.close()
    print("done")
if __name__ == '__main__':
    spider_universitie_enrollment_gulde()