# -*- coding: utf-8 -*-
"""
@Time ： 2020/7/9 上午9:12
@Auth ： LX
@File ：spider_majorsinfo.py
@IDE ：PyCharm
@DES : 爬取专业库中的信息
"""
from urllib import request
import json
import csv
import time

headers = {
    'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjM5NjY4MCwiSWF0IjoxLCJKdGkiOiIxOTY0NTk4MzgifQ.4BYvfo-ortjSyCSArWLaQQJLgRwm_Uw15OIiK1PJ7x0; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592361159',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'referer': 'https://www.in985.com/dataCenter/majorLib/majorLibList',
    'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MzY4OTI5OSwiSWF0IjoxLCJKdGkiOiIzMTY3Mzg0MzQifQ.ZFCLdXSNMnAthudaxv9g6UWVcoIWv4z9l7aTMc_PQQ0',
}
def str2json(str):
    '''
    把字符串转换为json
    :param str:
    :return:
    '''
    data = json.loads(str)
    data = data['data']
    return data

def get_page_date(url,headers):
    '''
    获取页面的json数据
    :param url:
    :param header:
    :return:
    '''
    req = request.Request(url=url,headers=headers)
    response = request.urlopen(req)
    if response.getcode() is 200:
        #bytes类型
        result = response.read()
        result = str(result,encoding='utf-8')
        return str2json(result)

def spider_one_major_specialtyCategoryID():
    '''
    爬取本科的所有一级专业信息的specialtyCategoryID
    :return:
    '''
    #本科
    # url='https://in985.com/api/v1/specialties/categories/0/1'
    #专科
    url='https://in985.com/api/v1/specialties/categories/0/2'

    #获取本科的所有一级专业信息
    oneMajor_json = get_page_date(url,headers)
    specialtyCategoryID_list = []
    for specialtyCategory in oneMajor_json:
        specialtyCategoryID = specialtyCategory['specialtyCategoryID']
        specialtyCategoryID_list.append(specialtyCategoryID)

    return specialtyCategoryID_list

def spider_two_major_specialtyCategoryID():
    '''
    爬取二级菜单的specialtyCategoryID
    :return:
    '''
    oneSpecialtyCategoryID_list = spider_one_major_specialtyCategoryID()
    specialtyCategoryID_list = []
    for one_specialtyCategoryID in oneSpecialtyCategoryID_list:
        if one_specialtyCategoryID == 0:
            continue
        #本科
        # url = 'https://in985.com/api/v1/specialties/categories/'+str(one_specialtyCategoryID)+'/1'
        #专科
        url = 'https://in985.com/api/v1/specialties/categories/' + str(one_specialtyCategoryID) + '/2'
        two_major_json = get_page_date(url,headers)
        data_list = []
        for specialtyCategory in two_major_json:
            specialtyCategoryID = specialtyCategory['specialtyCategoryID']
            data_list.append(specialtyCategoryID)
        specialtyCategoryID_list.append(data_list)
    return specialtyCategoryID_list

def spider_two_major_info():
    '''
    爬取三级目录信息
    :return:
    '''
    f =  open('majors.csv', 'w', encoding='utf-8',newline='')
    writer =csv.writer(f)
    writer.writerow(['speicaltyName','categoryName','parentCategoryName','graduateScale','employInterval','specialtyLevelName'])
    i = 0
    twoSpecialtyCategoryID_list = spider_two_major_specialtyCategoryID()
    for specialtyCategoryID_list in twoSpecialtyCategoryID_list:
        for specialtyCategoryID in specialtyCategoryID_list:
            #本科
            #url ='https://in985.com/api/v1/specialties?CategoryId='+str(specialtyCategoryID)+'&LevelId=1&Keyword=&PageIndex=1&PerPageSize=1000&Sort='
            # 专科
            url = 'https://in985.com/api/v1/specialties?CategoryId=' + str(
                specialtyCategoryID) + '&LevelId=2&Keyword=&PageIndex=1&PerPageSize=1000&Sort='
            majors_info_json =get_page_date(url,headers)
            majors_info_json = majors_info_json['items']
            for major_json in majors_info_json:
                data_list = []
                speicaltyName = major_json['speicaltyName']
                categoryName = major_json['categoryName']
                parentCategoryName = major_json['parentCategoryName']
                graduateScale = major_json['graduateScale']
                employInterval = major_json['employInterval']
                specialtyLevelName = major_json['specialtyLevelName']
                data_list.append(speicaltyName)
                data_list.append(categoryName)
                data_list.append(parentCategoryName)
                data_list.append(graduateScale)
                data_list.append(employInterval)
                data_list.append(specialtyLevelName)
                print(data_list)
                i += 1
                writer.writerow(data_list)
                print(i)
    f.close()
    print('done')


if __name__ == '__main__':
    spider_two_major_info()