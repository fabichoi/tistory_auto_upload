import argparse
import csv
import json
import logging
import os
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv


class TistoryPostAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(TistoryPostAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namesapce, values, option_string=None):
        url = 'https://www.tistory.com/apis/post/write'
        init_params = self.get_init_params()
        extra_params = self.get_csv_file(values)
        params_list = self.make_posts(init_params, extra_params)

        for params in params_list:
            r = requests.post(url=url, data=params)
            if r.status_code == 200:
                logging.info('%s 글 작성 완료.' % params.get('title'))
            else:
                logging.error(json.loads(r.text))

    def make_posts(self, init_params, extra_params):
        posts = []

        for params in extra_params:
            params.update(init_params)
            date_utc = datetime.now(timezone.utc) + timedelta(hours=9)
            # 날짜 변환 적용
            params['title'] = params['title'].replace('${DATE}', date_utc.strftime('%Y.%m.%d'))

            # 발행일 포맷 변환
            pub_date = datetime.strptime(params.get('published'), '%H:%M:%S')
            pub_date = pub_date.replace(year=date_utc.year, month=date_utc.month, day=date_utc.day) - timedelta(hours=9)
            params['published'] = pub_date.timestamp()
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
        logging.info('csv file info: %s' % data)
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
