一个爬取即刻app网页版用户图片的爬虫

使用方法，创建cookies.txt ，填写cookies，格式为

``````
{"x-jike-access-token": "", "x-jike-refresh-token": ""}
``````

在`jike.py` main函数的url替换为想要爬取的用户的url，即可爬取用户发布的所有图片


项目部分参考[anotherfre/demo_scrapy](https://github.com/github/gitignore/blob/main/Python.gitignore)