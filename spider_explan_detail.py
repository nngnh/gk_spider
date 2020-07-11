# -*- coding: utf-8 -*-
"""
@Time ： 2020/6/27 下午8:16
@Auth ： LX
@File ：spider_explan_detail.py
@IDE ：PyCharm
@DES : 
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
        driver.find_element_by_css_selector(".form-node div input[type='text']").send_keys("13518151051")
        driver.find_element_by_css_selector(".form-node div input[type='password']").send_keys("lwy0318")
        driver.find_element_by_css_selector(".layout-btn[data-v-9d71a452]").click()
    except NoSuchElementException as e:
        print(e)


def spider_detail():
    try:
        f = open('explan_deatil.csv', 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(
            ["identifyid", "majorname", "majorcode", "plan", "year", "money"])
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
        #年
        for year in year_radios:
            time.sleep(3)
            driver.execute_script("arguments[0].click();", year)
            time.sleep(3)
            numbers = driver.find_elements_by_css_selector(".el-pager li ")
            max_num = numbers[-1].text
            #下一页
            for i in range(int(max_num)):
                time.sleep(0.5)
                # 为了使页面数据加载完毕
                driver.find_element_by_css_selector(".el-table .cell")
                driver.find_elements_by_class_name("el-table__row")
                btns = driver.find_elements_by_class_name("link-btn")
                #每一列的详情
                for i in range(len(btns)):
                    driver.find_elements_by_class_name("link-btn")
                    driver.find_elements_by_class_name("el-table__row")
                    j = j + 1
                    # 点击详情跳转到具体页面
                    btns = driver.find_elements_by_class_name("link-btn")
                    driver.execute_script("arguments[0].click();", btns[i])
                    nums = driver.find_elements_by_css_selector(".el-pager li ")
                    for num in nums:
                        print(len(nums))
                        trs = driver.find_elements_by_css_selector(".card_inner_table tbody tr")
                        for tr in trs:
                            tds = tr.find_elements_by_css_selector(".card_inner_table tbody tr td ")
                            data = []
                            majorName = tds[0].text
                            majorCode = tds[1].text
                            explan = tds[2].text
                            educationTime = tds[3].text
                            tuition = tds[4].text
                            data.append(j)
                            data.append(majorName)
                            data.append(majorCode)
                            data.append(explan)
                            data.append(educationTime)
                            data.append(tuition)
                            csv_writer.writerow(data)
                            print(data)
                            time.sleep(0.5)
                        if len(nums) > 1:
                            next_btn = driver.find_element_by_css_selector(".default_card  .el-pagination .btn-next")
                            driver.execute_script("arguments[0].click();", next_btn)
                            time.sleep(1)
                    return_btn = driver.find_element_by_css_selector(".btn-box span[data-v-433f5d3e]")
                    driver.execute_script("arguments[0].click();", return_btn)
                    time.sleep(2)
                next_page = driver.find_element_by_css_selector(".el-pagination .btn-next")
                driver.execute_script("arguments[0].click();", next_page)

        f.close()
        print("done")
    except NoSuchElementException as e:
        print(e)
if __name__ == '__main__':
    login()
    # get_data()
    spider_detail()
