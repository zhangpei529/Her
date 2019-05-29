import random
import time
import pymysql

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class Spider:
    def __init__(self):
        self.debug_address = "127.0.0.1:9222"
        self.start_web_url = "https://rd5.zhaopin.com/custom/search"
        self.browser = self.handle_browser()
        self.db = pymysql.connect("localhost", "root", "1234", "the_littles")
        self.position_list = self.init_list("recuritment_position")
        self.pass_position_list = self.init_list("recuritment_passposition")
        self.name_elements = []
        self.job_elements = []
        self.basic_info = []

    def __del__(self):
        self.db.close()

    def handle_browser(self):
        """
        接管已打开的浏览器
        :return:
        """
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", self.debug_address)
        browser = webdriver.Chrome(chrome_options=chrome_options)
        return browser

    def init_list(self, table_name):
        """
        初始化欲搜索的工作内容列表和欲过滤的工作职位列表
        :return:
        """
        cursor = self.db.cursor()
        cursor.execute(f"select name from {table_name}")
        fetchall = cursor.fetchall()
        position_list = []
        for each in fetchall:
            position_list.append(each[0])
        return position_list

    def check_url(self):
        """
        检查接管页面的url是否正确
        :return:
        """
        flag = True
        while flag:
            if self.browser.current_url == self.start_web_url:
                flag = False
            else:
                print("页面错误, 请手动登陆到搜索简历页面, 系统休眠5秒钟")
                time.sleep(5)

    def search_information(self):
        """
        输入筛选条件
        :return:
        """
        for position in self.position_list:
            self.browser.get(self.start_web_url)
            print(position)
            time.sleep(5)
            # 工作内容
            work_content_element = self.browser.find_element_by_xpath('//*[@id="form-item-9"]/div/input')
            work_content_element.clear()
            work_content_element.send_keys(position)
            # 工作年限（6年)
            work_year_element = self.browser.find_element_by_xpath('//*[@id="form-item-13"]/div[1]/div/input')
            work_year_element.click()
            self.browser.find_element_by_xpath('/html/body/div[16]/ul/li[8]').click()
            # 学历(大专)
            education_level = self.browser.find_element_by_xpath('//*[@id="form-item-12"]/div[1]/div/input')
            education_level.click()
            self.browser.find_element_by_xpath('/html/body/div[14]/ul/li[6]').click()
            # 性别女
            gender = self.browser.find_element_by_xpath('//*[@id="form-item-17"]/div/label[3]/span[1]/span/i[1]')
            gender.click()
            # 更新日期(最近一个月)
            update = self.browser.find_element_by_xpath('//*[@id="form-item-38"]/div/div/input')
            update.click()
            self.browser.find_element_by_xpath('/html/body/div[11]/ul/li[5]').click()
            # 敲回车触发搜索
            work_year_element.send_keys(Keys.ENTER)
            time.sleep(5)
            # 依次处理页面以及翻页
            self.deal_page()

    def deal_page(self):
        """
        依次处理页面以及翻页
        :return:
        """
        while True:
            try:
                page_element = self.browser.find_element_by_class_name('k-pagination__total')
                print(page_element.text)
                popup_element = self.browser.find_element_by_class_name('k-message-box__wrapper')
                popup_attribute = popup_element.get_attribute('style')
                if 'block' not in popup_attribute:
                    self.get_statics_url()
                    self.browser.find_element_by_class_name('btn-next').click()
                    time.sleep(5)
                else:
                    return
                if self.browser.find_element_by_class_name('btn-next').get_attribute('disabled') == 'true':
                    return
            except NoSuchElementException:
                self.get_statics_url()
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                print("滑入页面最下方, 休息1秒")
                time.sleep(1)
                # self.browser.find_element_by_class_name('btn-next').click()
                if self.browser.find_element_by_class_name('btn-next').get_attribute('disabled') == 'true':
                    return
                else:
                    self.browser.find_element_by_class_name('btn-next').send_keys(Keys.ENTER)

    def get_statics_url(self):
        print("新开页面, 休眠5秒, 等待数据加载")
        time.sleep(5)
        self.name_elements = self.browser.find_element_by_class_name('k-table__body').find_elements_by_class_name(
            'is-text-normal')
        self.job_elements = self.browser.find_element_by_class_name('k-table__body').find_elements_by_class_name(
            'is-text-tiny')
        self.basic_info = self.browser.find_elements_by_class_name('resume-summary__basic-info')
        for key in range(0, len(self.name_elements)-1):
            insert_flag = True
            print(self.name_elements[key].text)
            # 过滤已查看的
            if '已查看' not in self.name_elements[key].text:
                for pass_position in self.pass_position_list:
                    # 根据关键词过滤职位
                    if self.job_elements[key * 4 + 1].text in pass_position:
                        insert_flag = False
                        break
                if insert_flag:
                    # self.name_elements[key].send_keys(Keys.ENTER)
                    # 滑动入视线范围中
                    if key + 1 == len(self.name_elements) -1:
                        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                    else:
                        self.basic_info[key+1].location_once_scrolled_into_view
                    print("滑入页面, 休息1秒")
                    time.sleep(2)
                    # self.browser.execute_script("arguments[0].click();", self.basic_info[key])
                    self.basic_info[key].click()
                    time.sleep(5)
                    handles = self.browser.window_handles
                    self.browser.switch_to.window(handles[-1])
                    print("获取新开页面" + self.browser.title)
                    self.get_detail_info()
                    self.browser.close()
                    handles = self.browser.window_handles
                    self.browser.switch_to.window(handles[-1])
                    self.name_elements = self.browser.find_element_by_class_name(
                        'k-table__body').find_elements_by_class_name(
                        'is-text-normal')
                    self.job_elements = self.browser.find_element_by_class_name(
                        'k-table__body').find_elements_by_class_name(
                        'is-text-tiny')
                    self.basic_info = self.browser.find_elements_by_class_name('resume-summary__basic-info')

    def get_detail_info(self):
        # 去除金领简历
        try:
            self.browser.find_element_by_class_name('is-gold-resume__icon')
            print("金领简历跳过")
        # 爬取个人数据
        except NoSuchElementException:
            # 避免页面加载超时
            try:
                unique_id = self.browser.find_element_by_class_name('resume-content--letter-spacing').text.split('：')[1]
                picture = "http:" + self.browser.find_element_by_class_name(
                    'resume-content__portrait-inner').get_attribute('style').split('"')[1]
                name = self.browser.find_element_by_class_name('resume-content__candidate-name').text
                gender = self.get_element_text_by_xpath(
                    '//*[@id="resume-detail-wrapper"]/div[1]/div[2]/div/div[1]/p[1]/span[1]')
                age = self.get_element_text_by_xpath(
                    '//*[@id="resume-detail-wrapper"]/div[1]/div[2]/div/div[1]/p[1]/span[2]')
                work_year = self.get_element_text_by_xpath(
                    '//*[@id="resume-detail-wrapper"]/div[1]/div[2]/div/div[1]/p[1]/span[3]')
                education_level = self.get_element_text_by_xpath(
                    '//*[@id="resume-detail-wrapper"]/div[1]/div[2]/div/div[1]/p[1]/span[4]')
                work_place = self.get_element_text_by_xpath('//*[@id="resumeDetail"]/div[1]/div/dl/dd[1]')
                work_reward = self.get_element_text_by_xpath('//*[@id="resumeDetail"]/div[1]/div/dl/dd[2]')
                current_situation = self.get_element_text_by_xpath('//*[@id="resumeDetail"]/div[1]/div/dl/dd[3]')
                work_character = self.get_element_text_by_xpath('//*[@id="resumeDetail"]/div[1]/div/dl/dd[4]')
                wanted_job = self.get_element_text_by_xpath('//*[@id="resumeDetail"]/div[1]/div/dl/dd[5]')
                wanted_industry = self.get_element_text_by_xpath('//*[@id="resumeDetail"]/div[1]/div/dl/dd[6]')
                education_elements = self.browser.find_element_by_class_name('timeline__header').find_elements_by_tag_name(
                    'span')
                education_experience = ""
                for key, value in enumerate(education_elements):
                    if key > 0:
                        education_experience += value.text + " "
                work_experience_list = []
                work_experience_elements = self.browser.find_element_by_xpath(
                    '//*[@id="resumeDetail"]/div[3]').find_elements_by_class_name('timeline__header')
                work_experience_sub_elements = self.browser.find_element_by_xpath(
                    '//*[@id="resumeDetail"]/div[3] ').find_elements_by_class_name('timeline__sub-title')
                for key, value in enumerate(work_experience_elements):
                    elements = value.find_elements_by_tag_name('span')
                    sub_elements = work_experience_sub_elements[key].find_elements_by_tag_name('span')
                    working_string = None
                    working_sub_string = ""
                    for second_key, second_value in enumerate(elements):
                        if working_string is None:
                            working_string = ""
                        else:
                            working_string += second_value.text + " "
                    for second_key, second_value in enumerate(sub_elements):
                        working_sub_string += second_value.text + " "
                    work_experience_list.append(working_string + " " + working_sub_string)
                url = self.browser.current_url
                self.insert_information_database(unique_id, picture, name, gender, age, work_year, education_level,
                                                 work_place, work_reward, current_situation, work_character, wanted_job,
                                                 wanted_industry, education_experience, work_experience_list, url)
                sleep_time = random.randint(1, 5)
                print(f"{name} 已爬取 即将休眠 休眠时间: {sleep_time}")
                time.sleep(sleep_time)
            except:
                pass

    def insert_information_database(self, unique_id, picture, name, gender, age, work_year, education_level,
                                    work_place, work_reward, current_situation, work_character, wanted_job,
                                    wanted_industry, education_experience, work_experience, url):
        """
        将个人数据插入到数据库中
        :param unique_id:
        :param picture:
        :param name:
        :param gender:
        :param age:
        :param work_year:
        :param education_level:
        :param work_place:
        :param work_reward:
        :param current_situation:
        :param work_character:
        :param wanted_job:
        :param wanted_industry:
        :param education_experience:
        :param work_experience:
        :param url:
        :return:
        """
        work_experience1 = ""
        for each in work_experience:
            work_experience1 += each + "\n"
        sql = f"insert into recuritment_person (unique_id, picture, name, gender, age, work_year, education_level, " \
            f"work_place, work_reward, current_situation, work_character, wanted_job, wanted_industry, " \
            f"education_experience, work_experience1, url) VALUES ('{unique_id}', '{picture}', '{name}', '{gender}', " \
            f"'{age}', '{work_year}', '{education_level}', '{work_place}', '{work_reward}', '{current_situation}', " \
            f"'{work_character}', '{wanted_job}', '{wanted_industry}', '{education_experience}', " \
            f"'{work_experience1}', '{url}')"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            print(f"{name} 已入库")
        except Exception as E:
            print(f"{name} 数据录入出错, 错误代码: {E}")

    def get_element_text_by_xpath(self, xpath):
        try:
            return self.browser.find_element_by_xpath(xpath=xpath).text
        except NoSuchElementException:
            return ""


if __name__ == '__main__':
    spider = Spider()
    spider.search_information()
    # spider.get_detail_info()
