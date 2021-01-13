import requests
import os
import json
from pyquery import PyQuery as pq

def get_one_page(url):
    """
        爬取具体一页 sample: url=https://maoyan.com/board/4?offset=0
        @param url: 要抓取页面的url
        @return: 网页的html文本
    """

    headers = {
        'User-Agent': os.getenv('USER_AGENT'),
        'Cookie': os.getenv('COOKIE')
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_one_page(text):
    """
        解析html文本
        @param text: 要被解析的html文本
        @return: generator[{
            'index', 'image', 'title', 'actor', 'time', 'score'
        }]
    """

    doc = pq(text)
    dds = doc('dd').items()

    for dd in dds:
        index = dd('.board-index').text()
        image = dd('.board-img').attr('data-src')
        title = dd('.name').text()
        actor = dd('.star').text().strip()
        time = dd('.releasetime').text().strip()
        score = dd('.integer').text() + dd('.fraction').text()
        
        yield {
            'index': index,
            'image': image,
            'title': title,
            'actor': actor[3:] if len(actor) > 3 else '',
            'releasetime': time[5:] if len(time) > 5 else '',
            'score': score
        }


def write_to_file(content):
    with open(os.getenv('RESULT_FILE'), 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')