import os
import time
from datetime import datetime

import requests
import csv

from dotenv import load_dotenv


def make_posts(init_params, extra_params):
    posts = []

    for params in extra_params:
        params.update(init_params)
        # 발행일 포맷 변환
        published = time.mktime(datetime.strptime(params.get('published'), '%Y-%m-%d %H:%M:%S').timetuple())
        params['published'] = published
        posts.append(params)

    return posts


def get_csv_file(filename):
    data = []
    f = open(filename, 'r', encoding='utf-8')
    csv_reader = csv.DictReader(f)
    for line in csv_reader:
        data.append(line)
    f.close()

    return data


def get_init_params():
    load_dotenv(verbose=True)

    access_token = os.getenv('ACCESS_TOKEN')
    output_type = os.getenv('OUTPUT_TYPE')
    blog_name = os.getenv('BLOG_NAME')

    init_params = {
        'access_token': access_token,
        'output': output_type,
        'blogName': blog_name,
    }

    return init_params


if __name__ == '__main__':
    init_params = get_init_params()
    extra_params = get_csv_file('example.csv')
    params_list = make_posts(init_params, extra_params)

    for params in params_list:
        requests.post('https://www.tistory.com/apis/post/write', params=params)
