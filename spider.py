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


#数据处理
def clear_data(province,university_infos_list,arr):

    #省份：北京
    prov = province.split("：")[1]
    #[ 北京大学 理科 本科第一批录取院校 ] 处理掉"["和"]"
    # info_list = []
    # info_list.append(university_infos_list[0][1:])
    # info_list.append(university_infos_list[1])
    # info_list.append(university_infos_list[2][:-1])
    university_name = university_infos_list[0][1:]
    #理科
    university_type = university_infos_list[1]
    #本科第一批录取院校
    university_class = university_infos_list[2][:-1]

    for i  in range(1,len(arr[0])):
        data = []
        data.append(prov)
        data.append(university_name)
        data.append(university_type)
        data.append(university_class)
        for j in range(len(arr)):
            data.append(arr[j][i])
        print(data)

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
                # 沉睡3秒
                time.sleep(3)
                try:
                    driver.find_element_by_css_selector(".card_inner_table tbody tr td")
                    # #获取到基础信息，类型，性质，省份，城市等基础信息
                    basic_infos = driver.find_elements_by_css_selector(".info p span[data-v-6444bd34]")
                    # 获取到省份
                    province = basic_infos[-4].text
                    # 获取到 [ 北京大学 理科 本科第一批录取院校 ]
                    university_infos = driver.find_elements_by_css_selector(".haha span[data-v-4c8d845f]")
                    # [ 北京大学 理科 本科第一批录取院校 ]保存为列表
                    info_list = []
                    for info in university_infos:
                        info_list.append(info.text)
                    # 获取到table
                    university_scores = driver.find_element_by_css_selector(".card_inner_table ")
                    # 用于存放table的所有数据
                    arr = []
                    # 用于存放table的thead
                    arr_thead = []
                    # 获取到thead（即年份）
                    yesrs = university_scores.find_element_by_css_selector(".card_inner_table thead tr ")
                    arr_thead = (yesrs.text).split(" ")
                    arr.append(arr_thead)
                    #获取到tbody
                    tbody = university_scores.find_elements_by_css_selector(".card_inner_table tbody tr ")
                    for i in range(len(tbody)):
                        # 获取到每行的数据
                        tr = tbody[i].find_elements_by_css_selector(".card_inner_table tbody tr td ")
                        arr_tbody = []
                        for i in range(len(tr)):
                            # 获取行中每列的数据
                            arr_tbody.append(tr[i].text)
                        arr.append(arr_tbody)
                    # print(arr)
                    # 关闭新弹出的页面
                    driver.close()
                    # 回到原始页面
                    driver.switch_to.window(current_handle)
                    #数据处理
                    clear_data(province,info_list,arr)
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









