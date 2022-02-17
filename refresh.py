import json

import requests
from requests.cookies import RequestsCookieJar


class Refresh:
    def __init__(self):
        self.url = 'https://web-api.okjike.com/api/graphql'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
            'cookie': "fetchRankedUpdate=1644895018488; x-jike-access-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiMjRkMG5keFZHTFpBcUx5Y3RkVXJTUGVFXC9SejhOTVVUOXhDMmdqRG41VUxsTUJcL3NxeDZYdFhLajRWelJyZGFBcXJpMTNrVnNRYnZiZ0VXcnpnSjlCbXFVeFpBcW81VE1VbHk3YXNmTTM4WWV6S3pjOVZlYmF3dXhha1VWN2IwTVc5T1V6Z0FCQUxvTjJaZmdKb1NIXC81UHBjYk5xV1dtR3RzaVBtUXJKQlFrUUR4a0pIQTRBdDV5OFNNRkJMZ0lsdlhHXC9FVkoxT3Jid3R3dlJBeWFkRHJNNjIwZ2l2R0NXMWlMdm9oWnRGek9PTnp5RDhHNDVDeFZhRTdscXJkOHhpUFViVDR0dHZvYTdteTk3K3VFUFBNV1wvemJCbUkxUDlYQzRBQ2tYOVREaHowdEUxbHErZTRFTlFKaUptNGdqSm1TeFdrSysxSnZIdnV6MGlZOVB5Y1p2MEppUUIyNFJSeXZ6MExHRWFXd2s9IiwidiI6MywiaXYiOiIrYzVqenZ0N1pqSVJoQU12amtOZlNBPT0iLCJpYXQiOjE2NDQ5MjcxNDguNjc3fQ.zEE265rXDsW2HrrZlJDFNyuFTxeORrGi7i3FXe6uHPQ; x-jike-refresh-token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjoiZjl3ZGhPb0pXQjlJdzNlZlFaUXBsSlR3WlYxVkk2aVFZT0ZUUUV3UkhRTUFyS3llKyt6OUdpcWJHNTB2VzRBQ2U2c2RNakJrOWpmZW8rZ1hoSGNqd01QVFpoVDB2WXpQMk5RVmpTXC8xR3Vpb3pzbEFrWFU1elRXRDlOVTMwWTJwZHlabVE2NENcL1JSQ25IdW93Q054bkhUQUNHNlNPcWNcL0VhOENHZ1wva240Zz0iLCJ2IjozLCJpdiI6IlI4bHBJTlNIZ1FNS21uTUl5eEpHbXc9PSIsImlhdCI6MTY0NDkyNzE0OC42Nzd9.IQMxbRghvQAls3ZJ6wkO8Yi8qyKZcg34fJyvy966W1M"
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

    def test(self):
        url = "https://web.okjike.com/me"
        r = requests.get(url, self.headers)
        print(r.status_code)
        with open("a.html", "w", encoding="utf-8") as f:
            f.write(r.text)


if __name__ == '__main__':
    Refresh().test()
