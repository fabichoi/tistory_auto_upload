import os
import requests
import time

from datetime import datetime, timedelta
from dotenv import load_dotenv


def make_posts(titles, content, visibility, category, start_date, tag, init_params):
    li = []
    n = len(titles)

    for i in range(n):
        additional_params = {
            'title': titles[i],
            'content': content,
            'visibility': visibility,
            'category': category,
            'published': time.mktime((start_date + timedelta(days=i)).timetuple()),
            'tag': tag,
        }
        additional_params.update(init_params)
        li.append(additional_params)

    return li


if __name__ == '__main__':
    load_dotenv(verbose=True)

    s = '2021-09-04 23:30:00'
    timestamp = time.mktime(datetime.strptime(s, '%Y-%m-%d %H:%M:%S').timetuple())

    access_token = os.getenv('ACCESS_TOKEN')
    output_type = os.getenv('OUTPUT_TYPE')
    blog_name = os.getenv('BLOG_NAME')

    init_params = {
        'access_token': access_token,
        'output': output_type,
        'blogName': blog_name,
    }

    titles = [
        "예제 글 1",
        "예제 글 2",
        "예제 글 3",
    ]

    content = ''
    category = 1
    visibility = 3
    published = timestamp
    tag = 'tag1,tag2,tag3'

    start_date = datetime.strptime('2021-09-05 23:30:00', '%Y-%m-%d %H:%M:%S')
    params_list = make_posts(titles, content, visibility, category, start_date, tag, init_params)

    for params in params_list:
        requests.post('https://www.tistory.com/apis/post/write', params=params)

    # r = requests.post('https://www.tistory.com/apis/post/write', params=params)
    # print(r.json())
