import json

import requests
from requests.cookies import RequestsCookieJar


class Refresh:
    def __init__(self):
        self.url = 'https://web-api.okjike.com/api/graphql'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
            # 'cookie': "fetchRankedUpdate=1681039564307; x-jike-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiXC9iOElYYjVoMkx6XC9wdnpGWlo1ZlBnSXp1dnpCSmkxemh1d3VsSG00SmVvc2JtRHB6XC9UbzlBSUxRdzVIMjNreE03dkI5d2lWeXNzNVIrckVOR3czUFBTMTk0VEUwNjVcL1pucHdKdkZaeG14dXl0cHRJajlGNkpCT0k4cUp0Sm1LOSthR3NpbGdJSDdxYkRpdVMrbXlYT21ZT09aS0dSaEVrTmI2aVpTbHM2V0d3dXFyQjUxZ1AyejVqSW5FaDhDZjJibUxhYmhQSWtOeGJOK1Yycm02anJ2XC8xXC85QmFsdm1LYTExWENQUUZma2pJTVdFSFc3bEFRdDl1Zmxhcnpuc2lpZnd5U2ZyVXhVcWVaNjZJZjVnNytGS21aV3FPY3psRHVjWGNtUTUyeEc2NjFuSEpkY25IeWZFbEU5N0VwMk5OWTBMSmxZT01UeFNZWmhIOTVqTmJsQXpcL2k2aWJuMkRpNnJHalRQR3c4VT0iLCJ2IjozLCJpdiI6IjE1RTZ5VDkrYWVaWWVQeWowK3U3NlE9PSIsImlhdCI6MTY4MTA0NDEwMi42ODh9.SsyuF7azWcdLHwaM4gOHVtCX_pHwOmKwyIp4IEcIYr8; x-jike-refresh-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiQ0ZFT1hRUkYyeUZiSHZEak5XSlpJK3BmYUxSbzlVOGpVc1R2YW9Uam9hSVN4elwvcUI1eXNxSG1zT2VIc3Y5ekhSazdcL2U0a25Kb0h6M3lrek14UVZhUzZFOGJ3RXJKRnJscWx4ZlVyRUU5MmsxMEVWM1RYSnBUVkR2WnVoODZcL2lLTTNsS29iRUo5MFc2MTN0MUhaZHQyVThHT2l5eE5EY3BlYUpLYWRvdllFPSIsInYiOjMsIml2IjoicDI1NnVMQVE0RnQ0T2I2Z0dIXC9KSXc9PSIsImlhdCI6MTY4MTA0NDEwMi42ODh9.JQud8RiVLSBmqgtm102woTmsxVXdYmUxEupjwz83k8M"
        }
        self.payload = {'operationName': "refreshToken",
                        'query': "mutation refreshToken {\n  refreshToken {\n    accessToken\n    refreshToken\n  "
                                 "}\n}\n",
                        'variables': {}}

    def save_cookies(self):
        with open("cookies.txt", "r", encoding="utf-8") as f:
            cookies = json.load(f)
        # str_cookies = "fetchRankedUpdate="
        str_cookies = ""
        for item in cookies:
            str_cookies = str_cookies + item + "=" + cookies[item] + ";"
        self.headers['cookie'] = str_cookies
        r = requests.post(self.url, headers=self.headers, data=self.payload)
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
        print("refresh successfully")
    def get_cookies(self):
        r = requests.post(self.url, headers=self.headers, data=self.payload)
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
    def load_cookies(self):
        with open("cookies.txt", "r") as fp:
            cookies = json.load(fp)
            self.headers['cookie'] = cookies
    def test(self):
        url = "https://web.okjike.com/me"
        r = requests.get(url, self.headers)
        print(r.status_code)
        with open("a.html", "w", encoding="utf-8") as f:
            f.write(r.text)


if __name__ == '__main__':
    r = Refresh()
    r.load_cookies()
    r.save_cookies()
