# -*- coding: utf-8 -*-
"""
@Time ： 2020/6/15 下午8:58
@Auth ： LX
@File ：spider_json_major.py
@IDE ：PyCharm
@DES ：爬取各学校专业的录取分数线
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
        # 'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592359019',
        'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592273437,1592354849,1592401952,1592470252; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592481766',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'referer':'https://www.in985.com/dataCenter/scoreLine/collegeAdmissions',
        #'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg',
        'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw'
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
    f = open('major1_2019.csv', 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(
        ["collegeCode","collegeId", "地区", "学校名称", "类别", "批次", "年", "专业名称", "实录分数", "本一实录线差", "本一实录位次", "成都二诊同位实录分", "平均分数", "本一平均线差",
         "本一平均位次","成都二诊同位平均分"])
    universities_list = spider_universities_info()
    #构造时间列表
    # time_list = ['2018','2017','2016','2015','2014','2013','2012']
    # time_list = ['2019']
    i = 0
    for university_list in universities_list:
        # for year in time_list:
            collegeHistoryId = str(university_list[0])
            url = 'https://in985.com/api/v1/history/specialty/enrollDiff/'+collegeHistoryId+'?Years=2019&PageIndex=1&PerPageSize=100'
            headers = {
                #'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592140773,1592191119,1592273437,1592354849; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592359019',
                'Cookie': 'Hm_lvt_7f9735c173e6f4dfe9097fa62a339f96=1592273437,1592354849,1592401952,1592470252; xueyiyunOAuth=eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw; Hm_lpvt_7f9735c173e6f4dfe9097fa62a339f96=1592481766',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                'referer': 'https://www.in985.com/dataCenter/scoreLine/collegeDetail',
                #'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzODgwNzExMTk0OjExNjk4MjQwNDk6NzE0NDAiLCJBdWQiOiIxIiwiRXhwIjoxNTkyMzk1MDE3LCJJYXQiOjEsIkp0aSI6IjEyMDYwOTI1MTgifQ.bSqOfNYP-HF9FOd5VPe-yAjL1MiBAqTDfkYtNmR6hgg',
                'authorization': 'eyJBbGciOiJSUzI1NiIsIlR5cCI6IkpXVCJ9.eyJJc3MiOm51bGwsIlN1YiI6IjEzNTE4MTUxMDUxOjI1NzIxNTg1MTo0NDE2IiwiQXVkIjoiMiIsIkV4cCI6MTU5MjUxNzQ3OCwiSWF0IjoxLCJKdGkiOiIxODQ1MzE5NTMxIn0.I5nEKHotMDPYdiyLmsfBj7gDlIHV5qbtEQGop8RrcAw'
            }
            # time.sleep(1)
            universities_json = get_page_data(url,headers)
            majors_json = universities_json['items']
            if len(majors_json) > 0 :
                for major_json in majors_json:
                    # 保存数据的list
                    data_list = []
                    #地区
                    province = university_list[1]
                    #学校名称
                    collegeName = university_list[2]
                    #理科
                    subject = university_list[3]
                    #本科第一批录取学校
                    order = university_list[4]
                    collegeCode = university_list[5]
                    #year
                    year = 2019
                    #专业名称
                    speicaltyName = major_json['speicaltyName']
                    #实录分数
                    matricGrade = major_json['diffs'][0]['matricGrade']
                    #本一实录线差
                    specialtyGradeDiff = major_json['diffs'][0]['specialtyGradeDiff']
                    #本一实录位次
                    matricGradePosition = major_json['diffs'][0]['matricGradePosition']
                    #成都二诊同位实录分
                    positionMatricGrade = major_json['diffs'][0]['positionMatricGrade']
                    #平均分数
                    averageGrade = major_json['diffs'][0]['averageGrade']
                    #本一平均线差
                    averageGradeDiff = major_json['diffs'][0]['averageGradeDiff']
                    #本一平均位次
                    averageGradePosition = major_json['diffs'][0]['averageGradePosition']
                    #成都二诊同位平均分
                    positionAverageGrade = major_json['diffs'][0]['positionAverageGrade']
                    data_list.append(collegeCode)
                    data_list.append(collegeHistoryId)
                    data_list.append(province)
                    data_list.append(collegeName)
                    data_list.append(subject)
                    data_list.append(order)
                    data_list.append(year)
                    data_list.append(speicaltyName)
                    data_list.append(matricGrade)
                    data_list.append(specialtyGradeDiff)
                    data_list.append(matricGradePosition)
                    data_list.append(positionMatricGrade)
                    data_list.append(averageGrade)
                    data_list.append(averageGradeDiff)
                    data_list.append(averageGradePosition)
                    data_list.append(positionAverageGrade)
                    csv_writer.writerow(data_list)
                    i += 1
                    print(i)
                    # print(data_list)
    f.close()
    print("done")

if __name__ == '__main__':
    spider_universities_major()
