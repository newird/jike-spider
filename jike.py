from datetime import datetime
import selenium.webdriver.chrome.options
from selenium import webdriver
from lxml import etree
import json
import time
import os
import random
import requests
from time import sleep
import refresh
from selenium.webdriver.chrome.service import Service


class JiKe:
    def __init__(self, url,save_path):

        self.options = selenium.webdriver.FirefoxOptions()
        # self.options.add_argument("--headless")
        self.browser = None
        self.url = url
        self.image_list = []
        self.save_path = save_path
        self.user = ""


    def get_page(self, save_login_cookies=False, load_login_cookies=False, scroll=False):
        """
        save_login_cookies: 保存登录cookies
        load_login_cookies: 加载登录cookies
        scroll:控制页面滚动
        """
        # s = Service(executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
        self.browser = webdriver.Firefox(options=self.options)
        self.browser.get(self.url)
        if save_login_cookies:
            self.save_login_cookies()
        if load_login_cookies:
            self.load_login_cookies()

        page = self.browser.page_source

        tail_len = 15000
        prev_len = len(page)
        self.geturl(page)

        if scroll:
            # refresh
            cnt = 0
            while True:
                cnt += 1
                if cnt % 20 == 0:
                    self.load_login_cookies()
                    self.save_login_cookies()

                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                # 根据网络状态适当修改滑动加载时间
                time.sleep(12)
                page = self.browser.page_source
                cul_len = len(page)
                print(cul_len)
                new_page = page[prev_len-tail_len:cul_len]
                prev_len = cul_len
                if self.geturl(new_page):
                    print("had downloaded!")
                    return




        

    def save_login_cookies(self):
        """
        保存登录cookies
        """
        ref = refresh.Refresh()
        ref.save_cookies()

        cookies = self.browser.get_cookies()
        with open('./cookies.json', 'w') as f:
            # f.write(json.dumps(cookies))
            json.dump(cookies, f)
        return True

    def load_login_cookies(self):
        """
        读取本地cookies文件加载cookies模拟登录
        """

        with open("cookies.json", "r") as fp:
            file = json.loads(fp.read())

            for cookie in file:
                self.browser.add_cookie({
                    'domain': cookie['domain'],
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': cookie['path']
                })
        with open('cookies.txt', 'r') as f:
            file = json.load(f)
            for cookie in file:
                self.browser.add_cookie({
                    'domain': ".okjike.com",
                    'name': cookie,
                    'value': file[cookie],
                    'path': "/"
                })

        self.browser.get(self.url)
        return True

    def geturl(self, page):

        print("new page")
        page = "<html> <head> <meta charset='utf-8'> </head> <body>" + page
        # print(page)
        page_etree = etree.HTML(page)

        if not self.user:
            user = page_etree.xpath('//h2[@class="sc-bdvvtL jpfEiy"]/text()')[0]
            self.user = user
        content_list = page_etree.xpath('//div[@class="flex flex-col border-b border-tint-border"]')

        for index, content in enumerate(content_list):
            # if not user:
            #     user = content.xpath('.//div[@class="flex flex-row pt-0.5 pb-1"]/text()')
            #     if user :
            #         user = user[0]


            # create_time = content.xpath('.//time/@datetime')[0][:10]
            is_pin = content.xpath('//div[@class="sc-bdvvtL sc-gsDKAQ ZQisl hIxhWw"]/text()')

            # text = content.xpath(
            #     './/div[contains(@class,"break-words content_truncate__1z0HR")]/text()')
            # href = content.xpath('.//a[@class="text-primary no-underline"]/@href')
            # like = content.xpath('.//span[@class="Like___StyledSpan-sc-8xi69i-1 gURQoB"]/text()')

            area = content.xpath(
                './/a[@class="flex flex-row inline-flex items-center justify-center text-tag-3 font-semibold py-1.5 pl-2 pr-2.5 rounded-full bg-bg-on-body-2 text-bg-jike-blue hover:shadow-[0_0_2px] transition mt-[13px]"]/text()')
            if area:
                area = area[0]
            else:
                area = "null"
            img_pattern = './/div[@class="sc-bdvvtL sc-gsDKAQ MessagePictureGrid__RadiusContainer-sc-pal5rf-0 lneceV hIxhWw lcqRTT"]'

            if content.xpath(img_pattern):

                img_src = content.xpath(img_pattern + '//img/@src')
                if img_src:
                    url = img_src[0].split('?')[0]
                    print(url)
                    self.download(area, url=url)


                else:
                    """
                    JavaScript
                    """
                    js = """
                        let src_list = [];
                        let temp_div = document.querySelectorAll("div.flex.flex-col.flex-auto.pt-2.w-full.animate-show.min-w-0")[(%s)];
                        let image_list = temp_div.getElementsByClassName("sc-bdnxRM MessagePictureGrid__Cell-sc-pal5rf-3");
                        for(let image of image_list){
                            let bg_image = window.getComputedStyle(image).backgroundImage;
                            src_list.push(bg_image);
                        }
                        return src_list;
                    """ % (index,)
                    images = self.browser.execute_script(js)


                    all_downloaded = True
                    for image in images:
                        img_src = image.lstrip('url("').rstrip('")')
                        url = img_src.split('?')[0]
                        print(url)
                        if is_pin :
                            print(is_pin[0])
                        else :
                            all_downloaded &= self.download(area, url)  
                    return all_downloaded

    def download(self,  area, url):
        path = save_path + self.user
        if not os.path.exists(path):
            os.mkdir(path)
        if area == "978-7-020-06838-?":
            area = "978"
        path = path + "\\" + area
        if not os.path.exists(path):
            os.mkdir(path)
        sleep(random.uniform(1, 2))
        # print("downloading")
        resp = requests.get(url)
        if resp.status_code == 200:
            file = url.split('?')[0][-18:]
            image = '{path}/{file}'.format(file=file, path=path)
            if "jpg" not in image and "jpeg" not in image and "png" not in image and "gif" not in image:
                image += ".png"
            if os.path.exists(image) :
                print("is exist")
                return True
            with open(image, 'wb') as f:
                f.write(resp.content)
            return False
        else:
            print("error")
            refresh.Refresh().save_cookies()


if __name__ == '__main__':
   

    save_path = "N:\\nas\\setu\\jike\\"
    with open("userlist.txt",'r') as f:
        for line in f.readlines():
            url = line.strip()
            jike = JiKe(url,save_path)
            jike.get_page(load_login_cookies=True, save_login_cookies=True, scroll=True)
