import json

import requests
from requests.cookies import RequestsCookieJar


class Refresh:
    def __init__(self):
        self.url = 'https://web-api.okjike.com/api/graphql'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
            'cookie': "sid=8075cba4-97f9-4f09-8ff3-da6732150192; x-jike-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiMG42K1diemlJUk54UDhuck5VTVlzQUxGR3JjTU0rUjVWN3Z3eHloVjZNamhOMzRtU2RZQzdwYk90MXkyaHpBWlh0NTNRQzY4SXFCcGFmaHlITjBJd0VzQ2xsTExwV1JRZ2tYc0xwMkk5K05tWWRWYmRjNjhCbXBqNGd5RHNcL2pEazRyZnhFb29GWFVvN2ZMS3Rhd0FUOGYzanRKeXhRdEl0dGgzeStONDRCNGJYR2c0T3h5UUtwZ1pzTG05VlFhbmg2WkxkTm4xZis4RCtVaHNFS1wvWXlhcDUrSnZ2ZFdXblQxSXprUWFVZkZVa3hwRXh4OUtyOEpqcURHN2cwc3hOeFlSaEhGK0dad2R0QzJUU29BUTZrRHVHbEk3QmpMN2R1M213SjJUbXBhbk1xNEFJcitRNUFiSk55VExGWTFGNEROdXNGc09URTJ5N0phbFRqWFhPeXBZeDJ1V054NWNGakd2bVZtYmxUMDA9IiwidiI6MywiaXYiOiJaT3p3UlNDczh2K1NVYWREeUdpWXp3PT0iLCJpYXQiOjE2ODA5NTQxNjYuNTI5fQ.DKSX5wVSTsyyZXzTwHAplgVvAJS0NIk-DuqTsn4vN2Q; x-jike-refresh-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoib2FvZFQ0YUJGV01sMHZ2cmM5SDN5QTBHMHRveHhnbFFYQWgwWGU4TnQ4SXdJYm1JRkkyM0UrSnlWMVBVaVZZcVkwRDhxQXNsVUVCbUJhQ1hzcE5lV0VVc2Y1SDZkUkdRUGxkQUdFa1Uyb3JiUkxRcXhIVnBlTW1UeUxFZEJXeE0xZDNUXC9UMXhqVmZzaWVGSVlCaXRvN1UybTF2QmpzaVlBa2t1NFFYTE95bz0iLCJ2IjozLCJpdiI6Ims5eUdrWGJvQjlJYXNxMHNPMm9VZ3c9PSIsImlhdCI6MTY4MDk1NDE2Ni41Mjl9.CI5hTWlKfWKJ16_VzR5fAqLv8ZIbX39c-KL72sxHn_s; fetchRankedUpdate=1680954166773"
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
    def test(self):
        url = "https://web.okjike.com/me"
        r = requests.get(url, self.headers)
        print(r.status_code)
        with open("a.html", "w", encoding="utf-8") as f:
            f.write(r.text)


if __name__ == '__main__':
    r = Refresh()
    r.get_cookies()
    r.save_cookies()
