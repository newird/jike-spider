from nturl2path import url2pathname
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
    def __init__(self, url,save_path):

        self.options = selenium.webdriver.FirefoxOptions()
        # self.options.add_argument("--headless")
        self.browser = None
        self.url = url
        self.image_list = []
        self.save_path = save_path
    def get_lastupdate(self,user):
        if os.path.exists("e://jike//images//"+user+"//time.txt"):
            with open("e://jike//images//"+user+"//time.txt","r") as f:
                time = f.readline()
        else :
            time = 0
        print(time)
        return time

    def get_page(self, save_login_cookies=False, load_login_cookies=False, scroll=False):
        """
        save_login_cookies: 保存登录cookies
        load_login_cookies: 加载登录cookies
        scroll:控制页面滚动
        """
        s = Service(executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
        self.browser = webdriver.Firefox(executable_path=r'C:\Program Files\Firefox Developer Edition\geckodriver.exe',options=self.options)
        self.browser.get(self.url)
        if save_login_cookies:
            self.save_login_cookies()
        if load_login_cookies:
            self.load_login_cookies()


        if scroll:

            # 滑动至底部
            client_hg = scroll_top = 0
            scroll_hg = 1
            while round(scroll_top) + round(client_hg) < round(int(scroll_hg)+100):
                # if p_scroll_hg == scroll_hg:
                #     cnt += 1
                #     if cnt == 3:
                #         break
                #     else :
                #         sleep(6)
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                # 根据网络状态适当修改滑动加载时间
                time.sleep(6)
                js = 'let scroll_top = document.documentElement.scrollTop; return scroll_top;'
                # p_scroll_top = scroll_top
                # print("loading more...\n")
                scroll_top = self.browser.execute_script(js)
                js = 'let client_hg = document.documentElement.clientHeight; return client_hg;'
                client_hg = self.browser.execute_script(js)
                js = 'let scroll_hg = document.body.scrollHeight; return scroll_hg;'
                p_scroll_hg = scroll_hg
                scroll_hg = self.browser.execute_script(js)

                if scroll_hg >= 2000:
                    break

        page = self.browser.page_source
        print("finished")
        return page
        

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
        print("start download")
        page_etree = etree.HTML(page)
        user = page_etree.xpath('//h2[@class="sc-bdvvtL jpfEiy"]/text()')[0]

        content_list = page_etree.xpath('//div[@class="flex flex-col border-b border-tint-border"]')
        # content_list = page_etree.xpath('//div[@class="flex flex-col flex-auto pt-2 w-full animate-show min-w-0"]')
        # print(content_list)
        cnt = 0
        for index, content in enumerate(content_list):
            # user = content.xpath('.//div[@class="flex flex-row pt-0.5 pb-1"]/text()')[0]
            create_time = content.xpath('.//time/@datetime')[0]
            file_path = save_path + user + "//time.txt"
            if not os.path.exists(save_path + user):
                os.makedirs(save_path + user)
            if os.path.isfile(file_path):
                with open(file_path, 'r') as f:
                    last_time = f.readline().strip()
                    if last_time == create_time:
                        print("已经下载过了")
                        return

            # print(create_time)
            if cnt == 0 :
                with open("E://jike/images//"+user +"//time.txt","w+") as f:
                    f.write(create_time)
                    cnt = 1
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
                # print(img_src)
                if img_src:


                    url = img_src[0].split('?')[0]
                    # img_src = url + "?imageMogr2/auto-orient%7Cwatermark/3/image/aHR0cHM6Ly93YXRlcm1hcmsuamVsbG93LmNsdWIvP3RleHQ9JUU1JThEJUIzJUU1JTg4JUJCJTIwJTQwJUU2JTk2JTkwJUU3JTg0JUI2XyZoZWlnaHQ9NzU=/gravity/SouthEast/dx/10/dy/10"
                    print(url)
                    self.download(user, area, url=url)
                    # with open("url.txt", "a", encoding="utf-8") as f:
                    # f.write(user+"|"+area+"|"+url + "\n")

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
                        # f.write(url+"\n")
                        #  f.write(user+"|"+area+"|"+url + "\n")
                        print(url)
                        self.download(user, area, url)

    def download(self, user, area, url):
        path = save_path + user
        if not os.path.exists(path):
            os.mkdir(path)
        if area == "978-7-020-06838-?":
            area = "978"
        path = path + "\\" + area
        if not os.path.exists(path):
            os.mkdir(path)
        sleep(random.random())
        print("downloaded")
        resp = requests.get(url)
        if resp.status_code == 200:
            # file = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            file = url.split('?')[0][-10:]
            image = '{path}/{file}'.format(file=file, path=path)
            if "jpg" not in image and "jpeg" not in image and "png" not in image and "gif" not in image:
                image += ".png"
            with open(image, 'wb') as f:
                f.write(resp.content)
        else:
            print("error")
            refresh.Refresh().save_cookies()


if __name__ == '__main__':
   
    # url = "https://web.okjike.com/" 
    # url = "" #山之
    url = "https://web.okjike.com/u/F2CF24F9-A022-4969-8691-FD1576BE8593"
    save_path = "E://jike/images//"
    jike = JiKe(url,save_path=save_path)
    page = jike.get_page(load_login_cookies=True, save_login_cookies=True, scroll=True)
    jike.geturl(page)
    # print("next")
    # sleep(600)
    # jike.load_lpogin_cookies()
    # jike.get_lastupdate("山之")