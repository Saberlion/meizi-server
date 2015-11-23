# -*- coding:utf8 -*-

import requests
import time
from lxml import etree

from app.db import ErrorPage, ErrDLPic, Meizi,DB_ADD


def getPicUrls(num):
    url = "http://meizi.us/view/%d.html" % num;
    # print url
    header_info = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1581.2 Safari/537.36',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    s = requests.session()
    # s.proxies = {'http': 'http://127.0.0.1:1080', 'https': 'https://127.0.0.1:1080'}
    try:
        r = s.get(url, headers=header_info, timeout=10)
    except Exception as e:
        print e
        return getPicUrls(num);

    content = r._content
    content = content.decode("utf8")

    page = etree.HTML(content)
    x = page.xpath('//*[@id="detail-portfolio-pager"]/div/img')
    if len(x) > 0:
        picUrl = x[0].get('src')
        return picUrl
    # print picUrl
    return None


def downloadImageFile(imgUrl):
    if imgUrl is None:
        return None
    local_filename = imgUrl.split('/')[-1]
    print "Download Image File=", local_filename
    try:
        r = requests.get(imgUrl, stream=True)  # here we need to set stream = True parameter
    except requests.ConnectionError as e:
        print e
        time.sleep(5)
        return downloadImageFile(imgUrl)

    #with open("D:\\Downloads\\" + local_filename, 'wb') as f:
    with open("/var/tmp/" + local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    return local_filename


def spider():

    for i in range(1, 50000, 1):
        print "尝试下载第%d张图片:" % i
        picUrl = getPicUrls(i)
        if picUrl is not None:
            DB_ADD(ErrorPage(i))
        else:
            continue

        filename = downloadImageFile(picUrl)
        if filename is not None:
            print "下载成功\n"

            DB_ADD(Meizi(filename))
        else:
            print "下载失败\n"
            DB_ADD(ErrDLPic(picUrl))



if __name__ == '__main__':
    spider()