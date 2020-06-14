# -*- coding: utf-8 -*-
"""
@Time ： 2020/6/14 上午11:13
@Auth ： LX
@File ：spider_major.py
@IDE ：PyCharm

"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time




driver = webdriver.Chrome(executable_path="/usr/local/chromedriver")
# 设置隐式等待时间为15秒
driver.implicitly_wait(15)
driver.get("https://www.in985.com/dataCenter/scoreLine/collegeAdmissions")
#模拟登录
try:
    driver.find_element_by_css_selector(".form-node div input[type='text']").send_keys("13518151051")
    driver.find_element_by_css_selector(".form-node div input[type='password']").send_keys("lwy0318")
    driver.find_element_by_css_selector(".layout-btn[data-v-9d71a452]").click()
except NoSuchElementException as e:
    print(e)


#进入详情页面爬取高校录取分数
def get_detail_data():
    try:
        detail_btu = driver.find_elements_by_class_name("link-btn")
    except NoSuchElementException as e:
        print(e)
    # 获取当前页面句柄
    current_handle = driver.current_window_handle
    # 遍历所有详情按钮
    for detail in detail_btu:
        # 点击详情跳转到具体页面
        driver.execute_script("arguments[0].click();", detail)
        # 获取当前打开的所有句柄
        all_handle = driver.window_handles
        for handle in all_handle:
            # 当前句柄和当前打开的句柄不相同，则打开了新的页面，即点击详情打开的页面，跳转过去获取到数据。
            if handle != current_handle:
                driver.switch_to.window(handle)
                # 设置等待时间15秒
                driver.implicitly_wait(15)
                # 沉睡3秒,这里是因为表格的是js生成的，数据是ajax动态请求生成的，先生成了表格，如果不沉睡，
                # 那么可能获取不到数据
                time.sleep(3)
                try:
                    #获取到专业录取分数按钮
                    major_detail_btn = driver.find_element_by_id("tab-two")
                    driver.execute_script("arguments[0].click();", major_detail_btn)
                    table = driver.find_element_by_id("pane-two")

                    driver.find_elements_by_css_selector("#pane-two .card_inner_table tbody tr td")
                    # 获取到 [ 北京大学 理科 本科第一批录取院校 ]
                    university_infos = driver.find_elements_by_css_selector("#pane-two .haha span[data-v-4c8d845f]")
                    # [ 北京大学 理科 本科第一批录取院校 ]保存为列表
                    info_list = []
                    for info in university_infos:
                        info_list.append(info.text)
                    #定位到并展开下拉框  展开后才能获取下拉框的数据
                    select = driver.find_element_by_css_selector("#pane-two .el-input__inner")
                    driver.execute_script("arguments[0].click();", select)

                    time.sleep(2)
                    #拿到下拉框中的数据
                    years = driver.find_elements_by_css_selector(".el-select-dropdown__item ")
                    #先把year的值保存下来，下面取不到，可能是下拉框收缩之后，取不到值
                    all_year = []
                    for yea in years:
                        all_year.append(yea.text)
                    #遍历数据，依次点击
                    for i in range(len(years)):
                        #点击下拉框中的年
                        driver.execute_script("arguments[0].click();", years[i])
                        #获取最大页面
                        #获取到显示页面的上一个ul，主要是用于判断里面是否有显示的页面 页数，有些页面没有页数
                        ul = driver.find_element_by_css_selector(".el-pager ")
                        #判断是否有页面，没有就说明没有数据，不进行操作
                        if len(ul.text) != 0:
                            #获取到所有的页面
                            nums = driver.find_elements_by_css_selector(".el-pager li")
                            #遍历，页面多的需要点击下一页爬取数据
                            for num in nums:
                                time.sleep(3)
                                #拿到表格里面的tr
                                trs = driver.find_elements_by_css_selector("#pane-two .card_inner_table tbody tr")
                                print(len(trs))
                                for tr in trs:
                                    arr = []
                                    arr.append(info_list[0][1:])
                                    arr.append(info_list[1])
                                    arr.append(info_list[2][:-1])
                                    arr.append(all_year[i])
                                    tds = tr.find_elements_by_css_selector("#pane-two .card_inner_table tbody tr td")
                                    for td in tds:
                                        arr.append(td.text)
                                    print(arr)

                                if len(nums) > 1:
                                    # 点击下一页
                                    next_btn = driver.find_element_by_css_selector("#pane-two .el-pagination .btn-next")
                                    driver.execute_script("arguments[0].click();", next_btn)
                                    time.sleep(5)


                    # 关闭新弹出的页面
                    driver.close()
                    # 回到原始页面
                    driver.switch_to.window(current_handle)
                except NoSuchElementException as e:
                    print(e)

#获取到最大的页面数
try:
    numbers = driver.find_elements_by_css_selector(".el-pager li ")
except NoSuchElementException as e:
    print(e)

# -1 就是最大页面对应的索引
max_num = numbers[-1].text
for i in range(int(max_num)):

    get_detail_data()
    try:
        next_page = driver.find_element_by_css_selector(".el-pagination .btn-next")
    except NoSuchElementException as e:
        print(e)
    driver.execute_script("arguments[0].click();", next_page)
    time.sleep(2)