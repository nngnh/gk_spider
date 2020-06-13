from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import ctime

driver = webdriver.Chrome(executable_path="/usr/local/chromedriver")
# cookie模拟登录
# brower.get("https://www.in985.com/index")
# # time.sleep(5)
# brower.find_element_by_css_selector(".icon-ipt input[type='text']").send_keys("13518151051")
# brower.find_element_by_css_selector(".icon-ipt input[type='password']").send_keys("lwy0318")
# brower.find_element_by_css_selector(".login-box .form-ctr .login-btn[data-v-14ff15b5]").click()
# 点击历史数据

# 设置隐式等待时间为15秒
driver.implicitly_wait(15)
driver.get("https://www.in985.com/dataCenter/scoreLine/collegeAdmissions")
try:
    driver.find_element_by_css_selector(".form-node div input[type='text']").send_keys("13518151051")
    driver.find_element_by_css_selector(".form-node div input[type='password']").send_keys("lwy0318")
    driver.find_element_by_css_selector(".layout-btn[data-v-9d71a452]").click()
except NoSuchElementException as e:
    print(e)

# 登录成功，进入到历史数据页面，获取到该页面的所有详情按钮
detail_btu = driver.find_elements_by_class_name("link-btn")
# 获取当前页面句柄
current_handle = driver.current_window_handle
# 遍历所有详情按钮
for detail in detail_btu:
    # 点击详情跳转到具体页面
    detail_page = driver.execute_script("arguments[0].click();", detail)
    # 获取当前打开的所有句柄
    all_handle = driver.window_handles
    for handle in all_handle:
        # 当前句柄和当前打开的句柄不相同，则打开了新的页面，即点击详情打开的页面，跳转过去获取到数据。
        if handle != current_handle:
            driver.switch_to.window(handle)
            driver.implicitly_wait(15)
            try:
                # 获取到 [ 北京大学 理科 本科第一批录取院校 ]
                university_infos = driver.find_elements_by_css_selector(".haha span[data-v-4c8d845f]")
                for info in university_infos:
                    print(info.text)
                # 获取到table
                university_scores = driver.find_element_by_css_selector(".card_inner_table ")
                #用于存放table的所有数据
                arr = []
                #用于存放table的thead
                arr_thead = []
                # 获取到thead（即年份）
                yesrs = university_scores.find_element_by_css_selector(".card_inner_table thead tr ")
                arr_thead = (yesrs.text).split(" ")
                arr.append(arr_thead)
                tbody = university_scores.find_elements_by_css_selector(".card_inner_table tbody tr ")

                for i in range(len(tbody)):
                    #获取到每行的数据
                    tr = tbody[i].find_elements_by_css_selector(".card_inner_table tbody tr td ")
                    arr_tbody = []
                    for i in range(len(tr)):
                        #获取行中每列的数据
                        arr_tbody.append(tr[i].text)
                    arr.append(arr_tbody)
                print(arr)
                #关闭新弹出的页面
                driver.close()
                #回到原始页面
                driver.switch_to.window(current_handle)
            except NoSuchElementException as e:
                print(e)


    # break;
