from datetime import datetime
from selenium.webdriver.chrome.options import Options
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

        self.options = Options()
        self.options.add_argument("--headless")
        self.browser = None
        self.url = url
        self.image_list = []
        self.save_path = save_path
        self.user = ""
        # 获取当前工作目录的绝对路径
        self.current_dir = os.path.abspath(os.path.dirname(__file__))    

    def log(self,message) :
        today = datetime.today().strftime('%Y-%m-%d')
        logfile = '/log/' + today + '.txt'
        logtxt = self.current_dir  + logfile 
        with open(logtxt , 'a+' , ) as f:
            print(message , file =  f) 
        print(message )
    def get_page(self,to_end = False):
        """
        save_login_cookies: 保存登录cookies
        load_login_cookies: 加载登录cookies
        scroll:控制页面滚动
        """
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.get(self.url)
        self.save_login_cookies()
        self.load_login_cookies()

        page = self.browser.page_source

        tail_len = 30000
        prev_len = len(page)
#        self.geturl(page)

        # refresh
        cnt = 0
        while True:
            time.sleep(6)
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            # 根据网络状态适当修改滑动加载时间
            print("refresh new page")
            time.sleep(12)
        
            page = self.browser.page_source
            cul_len = len(page)
            print(cul_len)
            new_page = page[prev_len-tail_len:cul_len]
            prev_len = cul_len
            if not self.geturl(new_page):
                self.log("had downloaded!")
                self.browser.quit()
                return

    def save_login_cookies(self):
        """
        保存登录cookies
        """
        ref = refresh.Refresh()
        ref.save_cookies()

        cookies = self.browser.get_cookies()
        with open(self.current_dir + '/cookies.json', 'w') as f:
            # f.write(json.dumps(cookies))
            json.dump(cookies, f)
        return True

    def load_login_cookies(self):
        """
        读取本地cookies文件加载cookies模拟登录
        """

        with open(self.current_dir + "/cookies.json", "r") as fp:
            file = json.loads(fp.read())

            for cookie in file:
                self.browser.add_cookie({
                    'domain': cookie['domain'],
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'path': cookie['path']
                })
        with open(self.current_dir + '/cookies.txt', 'r') as f:
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

        page = "<html> <head> <meta charset='utf-8'> </head> <body>" + page
        # print(page)
        page_etree = etree.HTML(page)

        if not self.user:
            user = page_etree.xpath('//h2[@class="sc-bdvvtL jpfEiy"]/text()')[0]
            self.user = user
            print(self.user)
        content_list = page_etree.xpath('//div[@class="flex flex-col border-b border-tint-border"]')
        download_state = False
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
                    self.log(url)
                    download_state |= self.download(area, url=url)


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

                        self.log(url)
                        if is_pin :
                            self.log(is_pin[0])
                        else :
                            download_state |= self.download(area, url)
            
        return  download_state
    def download(self,  area, url):
        path = save_path + self.user
        if not os.path.exists(path):
            os.mkdir(path)
        if area == "978-7-020-06838-?":
            area = "978"
        path = path + "/" + area
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
                self.log("is exist")
                return False
            with open(image, 'wb') as f:
                f.write(resp.content)
                return True
        return True 

if __name__ == '__main__':
   
    save_path = "/home/newird/nas/nas/setu/jike/"
    current_path = os.path.abspath(os.path.dirname(__file__))    
    with open(current_path + "/userlist.txt",'r') as f:
        for line in f.readlines():
            url = line.strip()
            if url.startswith('#'):
                continue
            jike = JiKe(url,save_path)
            jike.get_page()
