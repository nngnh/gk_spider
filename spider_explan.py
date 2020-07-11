# -*- coding: utf-8 -*-
"""
@Time ： 2020/6/24 下午8:38
@Auth ： LX
@File ：spider_explan.py
@IDE ：PyCharm
@DES : 爬取计划招生人数
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import csv

driver = webdriver.Chrome(executable_path="/usr/local/chromedriver")
# 设置隐式等待时间为15秒
driver.implicitly_wait(15)
driver.get("https://www.in985.com/dataCenter/explan")

# 模拟登录
def login():
    try:
        driver.find_element_by_css_selector(".form-node div input[type='text']").send_keys("13880711194")
        driver.find_element_by_css_selector(".form-node div input[type='password']").send_keys("lwy0318")
        driver.find_element_by_css_selector(".layout-btn[data-v-9d71a452]").click()
    except NoSuchElementException as e:
        print(e)

#爬取数据
# def get_data(year):
#     try:
#         #为了使页面数据加载完毕
#         driver.find_element_by_css_selector(".el-table .cell")
#         driver.find_elements_by_class_name("el-table__row")
#
#         trs = driver.find_elements_by_class_name("el-table__row")
#         for tr in trs:
#             tds = tr.find_elements_by_css_selector(".el-table__body td")
#             data = []
#
#             collegename = tds[1].text
#             province = tds[2].text
#             code = tds[3].text
#             subject = tds[4].text
#             squence = tds[5].text
#             plan = tds[6].text
#             isadd = tds[8].text
#             data.append(collegename)
#             data.append(province)
#             data.append(code)
#             data.append(subject)
#             data.append(squence)
#             data.append(plan)
#             data.append(isadd)
#             data.append(year)
#
#             print(data)
#     except NoSuchElementException as e:
#         print(e)

#点击下一页爬取数据
# def spider_by_page(year):
#     try:
#         numbers = driver.find_elements_by_css_selector(".el-pager li ")
#         max_num = numbers[-1].text
#         for i in range(int(max_num)):
#             get_data(year)
#             next_page = driver.find_element_by_css_selector(".el-pagination .btn-next")
#             driver.execute_script("arguments[0].click();", next_page)
#     except NoSuchElementException as e:
#         print(e)

def spider_by_year():
    try:
        f = open('artsexplan1.csv', 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            ["identifyid", "collegename", "province", "code", "subject", "squence", "plan","isadd"])
        # 为了使页面数据加载完毕
        driver.find_element_by_css_selector(".el-table .cell")
        driver.find_elements_by_class_name("el-table__row")
        # 获取到页面所有的radios div
        radios = driver.find_elements_by_class_name("el-radio-group")
        # 第二个为选择年份
        year_div = radios[1]
        year_radios = year_div.find_elements_by_css_selector(".el-radio")
        # 循环设置点击事件
        j = 0
        for year in year_radios:
            time.sleep(5)
            # year.click()
            driver.execute_script("arguments[0].click();", year)

            time.sleep(5)
            # spider_by_page(year.text)
            numbers = driver.find_elements_by_css_selector(".el-pager li ")
            max_num = numbers[-1].text
            for i in range(int(max_num)):
                time.sleep(0.5)
                # get_data(year)
                # 为了使页面数据加载完毕
                driver.find_element_by_css_selector(".el-table .cell")
                driver.find_elements_by_class_name("el-table__row")
                trs = driver.find_elements_by_class_name("el-table__row")
                for tr in trs:
                    tds = tr.find_elements_by_css_selector(".el-table__body td")
                    data = []
                    j = j + 1
                    collegename = tds[1].text
                    province = tds[2].text
                    code = tds[3].text
                    subject = tds[4].text
                    squence = tds[5].text
                    plan = tds[6].text
                    isadd = tds[8].text
                    data.append(j)
                    data.append(collegename)
                    data.append(province)
                    data.append(code)
                    data.append(subject)
                    data.append(squence)
                    data.append(plan)
                    data.append(isadd)
                    data.append(year.text)
                    csv_writer.writerow(data)
                next_page = driver.find_element_by_css_selector(".el-pagination .btn-next")
                driver.execute_script("arguments[0].click();", next_page)
        f.close()
        print("done")
    except NoSuchElementException as e:
        print(e)
if __name__ == '__main__':
    login()
    # get_data()
    spider_by_year()
