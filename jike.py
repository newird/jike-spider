import selenium.webdriver.chrome.options
from selenium import webdriver
import json
from datetime import datetime, timedelta
import os
import requests
from time import sleep
import refresh

# import proxy
from selenium.webdriver.common.by import By


class JiKe:
    def __init__(self, url, save_path, start_time):
        self.options = selenium.webdriver.FirefoxOptions()
        self.options.add_argument("--headless")
        self.browser = None
        self.url = url
        # self.proxy = proxy.Proxy()
        self.image_list = []
        self.save_path = save_path
        self.user = ""
        self.debug = False
        self.start_time = start_time

    def get_page(self):
        """
        save_login_cookies: 保存登录cookies
        load_login_cookies: 加载登录cookies
        scroll:控制页面滚动
        """
        # s = Service(executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
        self.browser = webdriver.Firefox(options=self.options)
        self.browser.get(self.url)
        self.save_login_cookies()
        self.load_login_cookies()
        self.browser.get(self.url)

        # window_size = self.browser.get_window_size()
        # mid_x = window_size['width'] / 2
        # actions = ActionChains(self.browser)
        # actions.move_by_offset(mid_x, 0)
        # actions.perform()

        previous_elements = []
        height = 1000
        cnt_arrive_bottom = 0
        last_execution_time = datetime.now()
        while True:
            # 检查当前时间和上次执行时间的间隔
            if datetime.now() - last_execution_time >= timedelta(minutes=10):
                self.log(str(datetime.now()))
                self.log("time to refresh")
                self.save_login_cookies()
                self.load_login_cookies()
                last_execution_time = datetime.now()
            if len(previous_elements) > 1:
                self.browser.execute_script(
                    """
                    let element = arguments[0];
                    let bounding = element.getBoundingClientRect();
                    if (bounding.top < 0 || bounding.left < 0 || bounding.right > window.innerWidth || bounding.bottom > window.innerHeight) {
                        element.scrollIntoView({behavior: 'auto', block: 'nearest', inline: 'nearest'});
                    }
                """,
                    previous_elements[-1],
                )
            # for i in range(last_scroll_position, height, 300):
            # self.browser.execute_script("window.scrollTo(0, {});".format(i))
            # time.sleep(0.1)
            self.browser.execute_script("window.scrollTo(0, {});".format(height))
            sleep(3)
            js = "let scroll_hg = document.body.scrollHeight; return scroll_hg;"
            height = self.browser.execute_script(js)

            new_elements = self.browser.find_elements(
                By.XPATH, '//div[@class="flex flex-col border-b border-tint-border"]'
            )
            if len(new_elements) > len(previous_elements):
                cnt_arrive_bottom = 0
                for content in new_elements[len(previous_elements) :]:
                    if self.geturl(content):
                        self.log("already downloaded")
                        self.browser.close()
                        return
                previous_elements = new_elements  # 更新已处理的元素列表
            else:
                cnt_arrive_bottom += 1
                if cnt_arrive_bottom == 5:
                    self.log("bottom")
                    self.browser.close()
                    return

    def get_proxy(self):
        return requests.get("http://114.212.83.23:5010/get/").json()

    def delete_proxy(self, proxy):
        requests.get("http://114.212.83.23:5010/delete/?proxy={}".format(proxy))

    def save_login_cookies(self):
        """
        保存登录cookies
        """
        ref = refresh.Refresh()
        ref.save_cookies()

        cookies = self.browser.get_cookies()
        with open("./cookies.json", "w") as f:
            # f.write(json.dumps(cookies))
            json.dump(cookies, f)
        # return True

    def load_login_cookies(self):
        """
        读取本地cookies文件加载cookies模拟登录
        """

        with open("cookies.json", "r") as fp:
            file = json.loads(fp.read())

            for cookie in file:
                self.browser.add_cookie(
                    {
                        "domain": cookie["domain"],
                        "name": cookie["name"],
                        "value": cookie["value"],
                        "path": cookie["path"],
                    }
                )
        with open("cookies.txt", "r") as f:
            file = json.load(f)
            for cookie in file:
                self.browser.add_cookie(
                    {
                        "domain": ".okjike.com",
                        "name": cookie,
                        "value": file[cookie],
                        "path": "/",
                    }
                )

        # self.browser.get(self.url)
        # return True

    def geturl(self, content):
        if not self.user:
            user_elements = self.browser.find_elements(
                By.XPATH, '//h2[@class="sc-bdvvtL jpfEiy"]'
            )
            user = user_elements[0].text
            self.user = user
            self.log(user)

        create_time_elements = content.find_elements(By.XPATH, ".//time")
        create_time = (
            create_time_elements[0].get_attribute("datetime")[:19]
            if create_time_elements
            else "1010101010"
        )
        create_time = create_time.replace(":", "")
        self.log(create_time)

        text_elements = content.find_elements(
            By.XPATH, './/div[contains(@class,"break-words content_truncate__tFX8J")]'
        )
        text = text_elements[0].text if text_elements else " "
        self.log(text)

        area_elements = content.find_elements(
            By.XPATH,
            './/a[contains(@class, "flex flex-row inline-flex items-center justify-center text-tag-3 font-semibold py-1.5 pl-2 pr-2.5 rounded-full bg-bg-on-body-2 text-bg-jike-blue hover:shadow-[0_0_2px] transition mt-[13px]")]',
        )
        area = area_elements[0].text if area_elements else "null"
        self.log(area)

        pin = content.find_elements(
            By.XPATH, './/div[contains(@class, "sc-bdvvtL sc-gsDKAQ ZQisl hIxhWw")]'
        )
        if pin:
            self.log("is pin")

        if self.save_post(area, create_time, text):
            return (not pin) and True

        img_elements = content.find_elements(
            By.XPATH,
            './/div[contains(@class, "MessagePictureGrid__RadiusContainer-sc-pal5rf-0")]//img',
        )
        if img_elements:
            img_src = img_elements[0].get_attribute("src").split("?")[0]
            self.download(area, create_time, img_src, "image")

        img_div_elements = content.find_elements(
            By.XPATH,
            './/div[@class="sc-bdvvtL sc-gsDKAQ MessagePictureGrid__RadiusContainer-sc-pal5rf-0 jKiyoA hIxhWw lcqRTT"]',
        )
        if img_div_elements:
            js = """
                let src_list = [];
                let image_list = arguments[0].getElementsByClassName("MessagePictureGrid__Cell-sc-pal5rf-3");
                for (let image of image_list) {
                    let bg_image = window.getComputedStyle(image).backgroundImage;
                    src_list.push(bg_image);
                }
                return src_list;
            """
            images = self.browser.execute_script(
                js, content
            )  # 'content' 是作为参数传递
            for image in images:
                img_src = image.lstrip('url("').rstrip('")')
                url = img_src.split("?")[0]

            for image in images:
                img_src = image.lstrip('url("').rstrip('")')
                url = img_src.split("?")[0]
                self.download(area, create_time, url, "image")

        video_pattern = (
            By.XPATH,
            './/div[contains(@class, "VideoContent__VideoContentContainer")]',
        )
        video_elements = content.find_elements(*video_pattern)
        if video_elements:
            # 确保视频元素在视图中
            self.browser.execute_script(
                """
                let element = arguments[0];
                let bounding = element.getBoundingClientRect();
                if (bounding.top < 0 || bounding.left < 0 || bounding.right > window.innerWidth || bounding.bottom > window.innerHeight) {
                    element.scrollIntoView({behavior: 'auto', block: 'nearest', inline: 'nearest'});
                }
            """,
                video_elements[0],
            )
            sleep(0.2)
            # 重新获取视频元素以确保它是最新的
            video_elements = content.find_elements(*video_pattern)
            # for element in video_elements:
            #     # 获取元素的外部 HTML
            #     outer_html = element.get_attribute('outerHTML')
            #     self.log(outer_html)
            if video_elements:
                # 尝试提取视频源 URL
                video_elements_inside = video_elements[0].find_elements(
                    By.TAG_NAME, "video"
                )
                if video_elements_inside:
                    video_src = video_elements_inside[0].get_attribute("src")
                    if video_src:
                        url = video_src
                        # 可选，去除 URL 的查询参数
                        # url = video_src.split('?')[0]
                        self.download(area, create_time, url, "video")
            else:
                # 如果重新获取的元素中没有 'video' 标签
                self.log("Video tag not found in the updated element.")

        return False


    def log(self, text):
        if self.debug:
            print(text)
        log_file_path = os.path.join(self.save_path, self.start_time + ".log")

        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(text + "\n")

    def save_post(self, area, create_time, text):
        path = self.getpath(area)
        new_path = os.path.join(path, create_time)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        else:
            return True
        post_file_path = os.path.join(new_path, "post.txt")
        with open(post_file_path, "a+", encoding="utf-8") as f:
            f.write(text)


    def download(self, area, create_time, url, type):
        path = self.getpath(area)
        resp = self.get_resource(url)
        if resp.status_code == 200:
            save_to = self.check_suffix(url, path, type)
            self.save_post(area, create_time, url)
            self.log(url + (" is exist" if os.path.exists(save_to) else ""))
            if os.path.exists(save_to):
                return True
            self.image_list.append(save_to)
            with open(save_to, "wb") as f:
                f.write(resp.content)
            return False
        else:
            self.log("error")
            refresh.Refresh().save_cookies()
            return True

    def get_resource(self, url):
        # sleep(0.1)
        # self.log("downloading")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        retry_count = 100
        proxy = self.get_proxy().get("proxy")
        # self.log(proxy)
        try:
            return requests.get(url, headers=headers)
        except Exception:
            while retry_count > 0:
                try:
                    resp = requests.get(
                        url,
                        headers=headers,
                        proxies={"http": "http://{}".format(proxy)},
                    )
                    return resp
                except Exception:
                    retry_count -= 1
                    self.delete_proxy(proxy)
                    self.log(proxy)
                    proxy = self.get_proxy().get("proxy")

    def getpath(self, area):
        path = os.path.join(self.save_path , self.user)
        if not os.path.exists(path):
            os.mkdir(path)
        if area == "978-7-020-06838-?":
            area = "978"
        path = os.path.join(path, area)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def check_suffix(self, url, path, type):

        file = url.split("?")[0][-18:]
        if type == "image":
            image = os.path.join(path, file)
            if not (image.endswith('.jpg') or image.endswith('.jpeg') 
                    or image.endswith('.png') or image.endswith('.gif')):
                image += ".png"
            return image

        elif type == "video":
            video = os.path.join(path, file)
            return video

        else:
            pass



if __name__ == "__main__":
    path_parts = ["N:", "nas", "setu", "jike"]
    save_path = os.path.join(*path_parts)
    start_time = datetime.now().strftime("%y%m%d%H%M%S")
    with open("userlist.txt", "r") as f:
        for line in f.readlines():
            url = line.strip()
            jike = JiKe(url, save_path, start_time)
            jike.get_page()
