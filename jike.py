import selenium.webdriver.chrome.options
from selenium import webdriver
from lxml import etree
import json
import time
import os
import random
import string
import requests
from time import sleep
import refresh
from selenium.webdriver.chrome.service import Service


class JiKe:
    def __init__(self, url):

        # chrome_opt = webdriver.ChromeOptions()
        # chrome_opt.add_argument("--proxy-server=http://171.92.21.43:9000")
        # self.browser = webdriver.Chrome(chrome_options=chrome_opt)
        self.options = selenium.webdriver.chrome.options.Options()
        # self.options.add_argument("headless")
        self.browser = None
        self.url = url
        self.image_list = []

    def get_page(self, save_login_cookies=False, load_login_cookies=False, scroll=False):
        """
        save_login_cookies: 保存登录cookies
        load_login_cookies: 加载登录cookies
        scroll:控制页面滚动
        """
        s = Service(executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
        self.browser = webdriver.Chrome(options=self.options, executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
        self.browser.get(self.url)
        if save_login_cookies:
            self.save_login_cookies()
        if load_login_cookies:
            self.load_login_cookies()

        if scroll:
            # 滑动至底部
            client_hg = scroll_top = 0
            p_scroll_top = -1
            scroll_hg = 1
            while round(scroll_top) + round(client_hg) < round(int(scroll_hg)):
                if p_scroll_top == scroll_top:
                    self.save_login_cookies()
                    self.load_login_cookies()
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                # 根据网络状态适当修改滑动加载时间
                time.sleep(12)
                js = 'let scroll_top = document.documentElement.scrollTop; return scroll_top;'
                p_scroll_top = scroll_top
                scroll_top = self.browser.execute_script(js)
                js = 'let client_hg = document.documentElement.clientHeight; return client_hg;'
                client_hg = self.browser.execute_script(js)
                js = 'let scroll_hg = document.body.scrollHeight; return scroll_hg;'
                scroll_hg = self.browser.execute_script(js)
        page = self.browser.page_source
        return page

    def save_login_cookies(self):
        """
        保存登录cookies
        """
        ref = refresh.Refresh()
        ref.save_cookies()
        # ref.load_cookies()
        #
        # cookies = self.browser.get_cookies()
        # with open('./cookies.json', 'w') as f:
        #     #f.write(json.dumps(cookies))
        #     json.dump(cookies,f)
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
        page_etree = etree.HTML(page)
        content_list = page_etree.xpath('//div[@class="flex flex-col flex-auto pt-2 w-full animate-show min-w-0"]')
        cnt = 0
        for index, content in enumerate(content_list):
            user = content.xpath('.//a[@class="sc-bdnxRM fEvjQr"]/text()')[0]
            create_time = content.xpath('.//time/@datetime')
            text = content.xpath(
                './/div[contains(@class,"break-words content_truncate__1z0HR")]/text()')
            href = content.xpath('.//a[@class="text-primary no-underline"]/@href')
            like = content.xpath('.//span[@class="Like___StyledSpan-sc-8xi69i-1 gURQoB"]/text()')

            area = content.xpath(
                './/a[@class="sc-bdnxRM cYiXfS Topic__TopicContainer-sc-si48dc-0 fiUuIG"]/text()')
            if area:
                area = area[0]
                # print(area)
            img_pattern = './/div[@class="sc-bdnxRM fzUdiI"]'
            if content.xpath(img_pattern):
                img_src = content.xpath(img_pattern + '//img/@src')
                if img_src:

                    url = img_src[0].split('?')[0]
                    # img_src = url + "?imageMogr2/auto-orient%7Cwatermark/3/image/aHR0cHM6Ly93YXRlcm1hcmsuamVsbG93LmNsdWIvP3RleHQ9JUU1JThEJUIzJUU1JTg4JUJCJTIwJTQwJUU2JTk2JTkwJUU3JTg0JUI2XyZoZWlnaHQ9NzU=/gravity/SouthEast/dx/10/dy/10"
                    print(url)
                    self.download(user, url=url)
                    # with open("url.txt", "a", encoding="utf-8") as f:
                    #     f.write(img_src[0] + "\n")

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
                    for image in images:
                        img_src = image.lstrip('url("').rstrip('")')
                        url = img_src.split('?')[0]
                        # img_src = url+"?imageMogr2/auto-orient%7Cwatermark/3/image/aHR0cHM6Ly93YXRlcm1hcmsuamVsbG93LmNsdWIvP3RleHQ9JUU1JThEJUIzJUU1JTg4JUJCJTIwJTQwJUU2JTk2JTkwJUU3JTg0JUI2XyZoZWlnaHQ9NzU=/gravity/SouthEast/dx/10/dy/10"
                        # # print(img_src)
                        # with open("url.txt","a",encoding="utf-8") as f:
                        #     f.write(img_src+"\n")
                        # print(url)
                        self.download(user, url)

    def download(self, user, url):
        path = 'E:\\jike\\images\\' + user
        if not os.path.exists(path):
            os.mkdir(path)
        sleep(random.random())

        resp = requests.get(url)
        if resp.status_code == 200:
            # file = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            file = url.split('?')[0][-10:]
            image = '{path}/{file}'.format(file=file, path=path)
            if "jpg" not in image and "jpeg" not in image and "png" not in image and "gif" not in image:
                image += ".png"
            with open(image, 'wb') as f:
                f.write(resp.content)


if __name__ == '__main__':
    url = 'https://web.okjike.com/u/3674272C-0234-4B76-B304-ED3489B531C9'
    jike = JiKe(url)
    page = jike.get_page(load_login_cookies=True, save_login_cookies=True, scroll=True)
    jike.geturl(page)
    # jike.load_login_cookies()
