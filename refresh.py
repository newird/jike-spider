import json

import requests
from requests.cookies import RequestsCookieJar


class Refresh:
    def __init__(self):
        self.url = 'https://web-api.okjike.com/api/graphql'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
            'cookie': "sid=21ce87b9-9a42-4082-a558-19cd51a5ac3d; x-jike-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoibXVjWDJYUzM4VFZoXC9SaXR4SStGd3BcL0JJOFplbFwvUFdZeE5BN284Zk93dEtkWDBqMlNpZmFPbVhpZ2JTQUNzdG9QOGpzOWh4Mkt6VVR4SnVEK2hWb2pvWUpHaHpRV3FRaUpkYXlENkJBZUpqMFE2NjVJNjc4R2pyZ1IrN1BuQng0RjhuK1htYitSTzFMSnI1QmU5eVwvSG4xblFhbTlvSDdCVTJ6VjdaUDQ1MFIrUnF0SGd1bGo0N0N2MjVVREVPYUJcL1NzbnlYTGF4OHRiYXZiREFIWDdpV0pVUFJzdTFySk9raDd4QXpKcXo2Qlo5dUJUYXB5RzB2ZzQ1WkRlUlM2UGlnS0NCZ1ZVdUdibDBiMitBQk9xVDgwR1VuckpySTViUWNXbDJCS2pidUlpeGFqSVQ2OXhOcWxuTmg5d2R3WDA3em9jZWxTMkxic0tlN1ZTWDExU3lHUUtadkN3ajFuSWFRZ3dTb1wvUlN3PSIsInYiOjMsIml2IjoiS3dzWG1xTU1Jd0ZoWmNMWGlyQnJ0UT09IiwiaWF0IjoxNjY0NTQ0ODcwLjYzfQ.XyTXKOU0Lknosf8RYXqdS0MtL3chJeyY0bI0TkdMXYU; x-jike-refresh-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiS2VUUHZjOVAza1Zyc2dQNXVSemFvU2FkSzBSNzduOUlOR2dLMFRPcU5NRHNlZ2haS0FCR3M1K2orbHZBOHJCTVdHR1VoVzByWjJJdHJabnF4NHhQMkhZaDAwSkdueVBFKzRJVFRPRjNhOGJKYUxGZDFqMkhcL2pDNnRxNUE2YmFjdjhoXC9oR2xKZ0JPcjlKblVmZmd2S0xTOVMrcERnZTNhUzlXek03VERobFk9IiwidiI6MywiaXYiOiJtNlZ2eHRZM00rWmlUSFhhWVhNSEFRPT0iLCJpYXQiOjE2NjQ1NDQ4NzAuNjN9.qparbxqhP-Xh74FwWSYfq0DqWxUhQJlmY0H8Bi7Y3Ow; fetchRankedUpdate=1664544873476"
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
