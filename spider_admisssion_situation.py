# -*- coding: utf-8 -*-
"""
@Time ： 2020/6/18 下午5:20
@Auth ： LX
@File ：spider_admisssion_situation.py
@IDE ：PyCharm
@DES : 爬取录取情况
文科和理科只需要把cookie和authorization 变换了就行
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


#爬取2909所学校基本信息，把详情页面需要的参数都保存到list中
def spider_universities_info():
    url = 'https://in985.com/api/v1/history/college?OrderIds=&ProvinceIds=&Keyword=&PageIndex=1&PerPageSize=3000&subject=0'
    headers = {
        # 'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592273437,1592354849,1592401952,1592470252; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592481766',
        'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592359019',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'referer':'https://www.in985.com/dataCenter/scoreLine/collegeAdmissions',
        #理科
        # 'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw'
        'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg',
    }
    #获得学校的信息，str格式
    universities_json = get_page_data(url,headers)
    universities_json = universities_json['items']
    universities_list = []
    for universitiy in universities_json:
        #arr = [641,'北京','北京大学','理科','本科第一批录取院校']
        arr = []
        #以下字段都是点击详情所需要的
        collegeHistoryId = universitiy['collegeHistoryId']
        province = universitiy['province']
        collegeName = universitiy['collegeName']
        subject = universitiy['subject']
        order = universitiy['order']
        collegeCode = universitiy['collegeCode']
        arr.append(collegeHistoryId)
        arr.append(province)
        arr.append(collegeName)
        arr.append(subject)
        arr.append(order)
        arr.append(collegeCode)
        universities_list.append(arr)
    return universities_list


def spider_universities_major():
    f = open('artadmission_situation.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["collegeCode","collegeHistoryId","province","collegeName","subject","order","historyProYear","realRecruitTotal","firstWishTotal","enrollProperty","firstWishSucTotal","secondWishSucTotal"])
    universities_list = spider_universities_info()
    #构造时间列表
    i = 0
    j = 0
    for university_list in universities_list:
        collegeHistoryId = str(university_list[0])
        url = 'https://in985.com/api/v1/history/college/enrollDetail/' + collegeHistoryId
        headers = {
            # 'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592273437,1592354849,1592401952,1592470252; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592481766',
            'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592359019',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'referer': 'https://www.in985.com/dataCenter/scoreLine/collegeDetail',
            # 'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw'
            'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg',
        }

        universities_json = get_page_data(url, headers)
        j += 1
        if j == 10:
            time.sleep(1)
            j = 0
        if len(universities_json) > 0:
            for university_json in universities_json:
                data = []
                # 地区
                province = university_list[1]
                # 学校名称
                collegeName = university_list[2]
                # 理科
                subject = university_list[3]
                # 本科第一批录取学校
                order = university_list[4]
                # 学校id
                collegeCode = university_list[5]
                historyProYear = university_json['historyProYear']
                realRecruitTotal = university_json['realRecruitTotal']
                firstWishTotal = university_json['firstWishTotal']
                enrollProperty = university_json['enrollProperty']
                firstWishSucTotal = university_json['firstWishSucTotal']
                secondWishSucTotal = university_json['secondWishSucTotal']
                data.append(collegeCode)
                data.append(collegeHistoryId)
                data.append(province)
                data.append(collegeName)
                data.append(subject)
                data.append(order)
                data.append(historyProYear)
                data.append(realRecruitTotal)
                data.append(firstWishTotal)
                data.append(enrollProperty)
                data.append(firstWishSucTotal)
                data.append(secondWishSucTotal)
                csv_writer.writerow(data)
                i += 1
                print(i)
    f.close()
    print("done")

if __name__ == '__main__':
    spider_universities_major()
