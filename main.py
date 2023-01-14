import os
import argparse
import json
import logging
from datetime import datetime

import requests
import csv

from dotenv import load_dotenv
from pytz import timezone

release_version = '2021.09.06'


class PostAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(PostAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namesapce, values, option_string=None):
        init_params = self.get_init_params()
        extra_params = self.get_csv_file(values)
        params_list = self.make_posts(init_params, extra_params)

        for params in params_list:
            r = requests.post('https://www.tistory.com/apis/post/write', params=params)
            if r.status_code == 200:
                logging.info('%s 글 작성 완료.' % params.get('title'))
            else:
                logging.error(json.loads(r.text))

    def make_posts(self, init_params, extra_params):
        posts = []

        for params in extra_params:
            params.update(init_params)
            # 발행일 포맷 변환
            dtime = datetime.strptime(params.get('published'), '%Y-%m-%d %H:%M:%S')
            published = dtime.astimezone(timezone('Asia/Seoul'))
            params['published'] = published
            posts.append(params)

        return posts

    def get_csv_file(self, filename):
        data = []
        try:
            with open(filename, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for line in csv_reader:
                    data.append(line)
        except Exception as e:
            logging.error('No such file or directory ' + filename)

        return data

    def get_init_params(self):
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
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser(description='Posts auto upload on Tistory.')
    parser.add_argument('filename', type=str, help="csv file", action=PostAction)
    args = parser.parse_args()
