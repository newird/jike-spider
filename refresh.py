import json

import requests
from requests.cookies import RequestsCookieJar


class Refresh:
    def __init__(self):
        self.url = 'https://web-api.okjike.com/api/graphql'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
            'cookie':'fetchRankedUpdate=1644809218924; x-jike-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiRXltZ0pcL2swSytRaXZJSXVqZkZCcXhwTEx2d2FuMkJpbGVGSXA3Rm1wQUwxREc3czk0RWhXbEdBemxLOTZLRG9sck50bkdUazRmcjFPc1ZuZEZPbDBZV2pxSTVCbDVFN3lnUVZKanFicmNFK3BZSk5WV1AyU0V0dlI3dGZmekdieDRodlwvTWFyS3hXMmhIZVRFeDNNOTQwOW95Mml0K085Njk4eXlEUGxNUUs5alBGK3NaUXF5eFwvem52XC92dm5PbWw1WDFLcDRNWTVUV0h5MWhDOHNKZTg2cTJKUHZEeWYwS3VIRTNSNW4wZ1wvY0FzUkdmbTgyNlFRQlpZcXBDajk4ZHVSQzRuUjhZWEx6eHRyQ2JyNk1UbkFVSDNJRGVsTXZyWjM5d3ZUVUJZb1BXNGQzQlBkQ1pudlNIUHBJbDZyMWIyZ2VVZVNzaGNHVXFnMDRhS3dWMGtVenpOSFNpbzFVOW1JRDErb3Z3UVE9IiwidiI6MywiaXYiOiJCa2k4ZUVOemVqd2VRMWxVbCtkUUd3PT0iLCJpYXQiOjE2NDQ4MTA3NTYuNjI5fQ.Vvozss7dWWAJ3IggEOj2Dz9t5XOPlTAZ01NSf2wnA0k; x-jike-refresh-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiUnZPcjF3Y3RvTnJBbHhKYUgrUVZabFVtZ2ZSS2IzbzNIM0RCUXVTcWp6UXVuRXhuMkpvMTNJOURvNjlJVTQ5RnFZQTN5Qndqb1BYWFBhNTlVQUMyeXN5YzVhQndLSGhnbDNJc091ZmpMc3hObnBMN09kbFJXaGNtWlcxblRrbVRieUVUVHV1NEoxcU5EelpjTExSS2R4b2dcL2ZiTTdrdU94NmRcL0tEVER5a1E9IiwidiI6MywiaXYiOiJ3MkVOOTNPMlFIblhSYXdXQnpjdlZBPT0iLCJpYXQiOjE2NDQ4MTA3NTYuNjI5fQ.UazY32BFjo6Yzwyp3oiB5YVMRNvCpy538ezeK_58z-8'
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
        r = requests.post(self.url,headers=self.headers,data=self.payload)
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)



