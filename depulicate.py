# 打开文件并读取行
with open("userlist.txt", "r") as file:
    urls = file.readlines()

# 使用集合去重
unique_urls = set(url.strip() for url in urls)

# 将去重后的URL写回文件
with open("userlist.txt", "w") as file:
    for url in unique_urls:
        file.write(url + "\n")
