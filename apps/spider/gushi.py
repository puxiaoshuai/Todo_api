import requests
from lxml import etree
import json
import re

url = "https://www.gushiwen.org/shiwen/default_0AA{}.aspx"
mp3_url = "https://so.gushiwen.org/viewplay.aspx?id={}"
head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
}
pomes = []


def request_one_page(page):
    try:
        response = requests.get(url=url.format(page), headers=head)
        if response.status_code == 200:
            parse_one_page(response.text)
        else:
            print("状态码错误")
    except Exception as err:
        pass


def parse_one_page(text):
    htmlElt = etree.HTML(text)
    div_content = htmlElt.xpath('//div[@class="sons"]')
    for div in div_content:
        title = div.xpath('.//div[@class="cont"]//b/text()')[0]
        caodai = div.xpath('.//div[@class="cont"]//p[@class="source"]//a/text()')[0]
        author = div.xpath('.//div[@class="cont"]//p[@class="source"]//a/text()')[1]
        # 详情不好取就到详情中去取
        # content=htmlElt.xpath('//div[@class="cont"]//div[@class="contson"]//text()')
        url = div.xpath('.//div[@class="cont"]/p/a/@href')[0]
        tags = div.xpath('.//div[@class="tag"]//a/text()')
        content,mp3 = request_detail(url=url)
        pome = {
            "title": title,
            'caodai': caodai,
            'author': author,
            'content': content.strip(),
            'tags': tags,
            'mp3_url': mp3

        }
        pomes.append(pome)

def request_detail(url):
    response = requests.get(url=url, headers=head)
    if response.status_code == 200:
        htmlEle = etree.HTML(response.text)
        content = "".join(htmlEle.xpath("//div[@class='contson']//text()"))
        content_id = re.findall('<textarea.*?id="txtare(.*?)">', response.text)[0]
        mp3 = parse_mp3(content_id)
        yiwen=htmlEle.xpath("")
        return content,mp3
    else:
        print("详情状态码错误")


def parse_mp3(id):
    try:
        resopnse = requests.get(url=mp3_url.format(id), headers=head)
        htmlEle = etree.HTML(resopnse.text)
        mp3 = htmlEle.xpath('//audio/@src')[0]
        return mp3
    except Exception as e:
        print("mp3解析错误"+e)
        return ""


def main():
    for page in range(1, 5):
        request_one_page(page=page)
        print("爬取了{}页".format(page))
        if page == 4:
            with open('gushi.json', 'w', encoding="utf-8") as f:
                f.write(json.dumps(pomes, ensure_ascii=False))
                print("写入完毕")


if __name__ == '__main__':
    main()
