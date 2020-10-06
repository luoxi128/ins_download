import requests
import re
import os
import json
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# url = 'http://i.rcuts.com/update.php?id=153'
# url_ins = input("input the link here:")
proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "http://127.0.0.1:1080",
}
api = "http://118.24.49.88/Video/X.php"  # from kejishou

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/68.0.3440.106 Safari/537.36'}


def query_api(api_temp, data_temp):
    try:
        logging.debug("trying " + api_temp + " for ins page " + data_temp["url"])
        response = requests.post(api_temp, data=data_temp)
        if response.status_code == 200:
            return response.text
        else:
            logging.error('请求错误状态码：' + response.status_code)
    except Exception as e:
        print(e)
        return None


def main():
    url = input("input the link here: ")
    url_ins = {'url': url}  # make a dictionary

    res = query_api(api, url_ins)  # send the url to api and get respond
    result = json.loads(res)

    if result["code"] == 0:  # if it's a url from instagram
        urls_pic = []
        it2 = re.finditer(r'https:\\\/\\\/.+?(?=")', res)  # extract url
        for match in it2:
            # print("match:", match.group())
            url_pic = re.sub(r'\\', "", match.group(0))  # clean the \
            urls_pic.append(url_pic)  # put all urls into an array

        logging.info("The task has page amount " + str(len(urls_pic)))
        general_name = input("file name:")
        n = 1
        path = "./picture"  # file path
        if not os.path.exists(path):
            os.makedirs(path)  # if there isn't such a file then create one

        for each_url in urls_pic:
            logging.debug("Downloading " + each_url)
            picture = requests.get(each_url, proxies=None)  # get the url content
            file_format = re.search(r'(?<=\.).{3,5}(?=\?)', each_url)
            # print(file_format)
            name = "picture/" + general_name + str(n).zfill(2) + "." + file_format.group()
            with open(name, 'wb') as f:
                f.write(picture.content)  # write to the disk
                f.close()
            n = n + 1
        logging.info("Task finishes Successfully！！！")
    else:
        logging.error("Ops!Something wrong, please try again.")


if __name__ == "__main__":
    main()
