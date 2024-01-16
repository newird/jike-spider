import requests

class Proxy:
    def __init__():
        pass
    def get_proxy(self):
        return requests.get("http://114.212.87.124:5010/get/").json()

    def delete_proxy(self,proxy):
        requests.get("http://114.212.87.124:5010/delete/?proxy={}".format(proxy))

    def getHtml(self):
        retry_count = 5
        proxy = self.get_proxy().get("proxy")
        while retry_count > 0:
            try:
                html = requests.get('http://www.ip111.cn', proxies={"http": "http://{}".format(proxy)})
                # 使用代理访问
                return html
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        self.delete_proxy(proxy)
        return None

proxy = Proxy()
print(proxy.getHtml().content)