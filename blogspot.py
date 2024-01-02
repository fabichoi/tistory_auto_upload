import argparse
import csv
import json
import logging
import os
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv


class BlogspotPostAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(BlogspotPostAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namesapce, values, option_string=None):
        init_params = self.get_init_params()
        extra_params = self.get_csv_file(values)
        params_list = self.make_posts(init_params, extra_params)

        url = f'https://www.googleapis.com/blogger/v3/blogs/{os.getenv("G_BLOG_ID")}/posts/'
        headers = {
            'Authorization': 'Bearer ' + init_params.get('access_token')
        }

        for params in params_list:
            r = requests.post(url=url, data=json.dumps(params), headers=headers)
            if r.status_code == 200:
                logging.info('%s 글 작성 완료.' % params.get('title'))
            else:
                logging.error(json.loads(r.text))

    def make_posts(self, init_params, extra_params):
        posts = []

        for params in extra_params:
            date_utc = datetime.now(timezone.utc) + timedelta(hours=9)
            params['kind'] = 'blogger#post'
            params["blog"] = {
                "id": os.getenv('G_BLOG_ID')
            }
            # 날짜 변환 적용
            params['title'] = params['title'].replace('${DATE}', date_utc.strftime('%Y.%m.%d'))

            # 발행일 포맷 변환
            pub_date = datetime.strptime(params.get('published'), '%H:%M:%S')
            pub_date = pub_date.replace(year=date_utc.year, month=date_utc.month, day=date_utc.day)
            params['published'] = pub_date.replace(tzinfo=timezone(timedelta(hours=9))).isoformat()
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

        init_params = {
            'client_id': os.getenv('G_CLIENT_ID'),
            'client_secret': os.getenv('G_CLIENT_SECRET'),
            'refresh_token': os.getenv('G_REFRESH_TOKEN'),
            'grant_type': 'refresh_token',
            'redirect_uri': 'http://localhost'
        }

        oauth2_url = 'https://oauth2.googleapis.com/token'
        r = requests.post(oauth2_url, params=init_params)
        if r.status_code == 200:
            access_token = json.loads(r.text).get('access_token')
            init_params.update({
                'access_token': access_token
            })
        else:
            logging.info('Authorization Failed.')
            raise Exception

        return init_params
