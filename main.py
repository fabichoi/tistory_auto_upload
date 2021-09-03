import os
import requests
import time

from datetime import datetime

from dotenv import load_dotenv

if __name__ == '__main__':

    load_dotenv(verbose=True)

    s = '2021-09-04 23:30:00'
    timestamp = time.mktime(datetime.strptime(s, '%Y-%m-%d %H:%M:%S').timetuple())

    access_token = os.getenv('ACCESS_TOKEN')
    output_type = os.getenv('OUTPUT_TYPE')
    blog_name = os.getenv('BLOG_NAME')
    title = 'title exam'
    content = 'content exam'
    visibility = 3
    category = 0
    published = timestamp
    tag = 'api,test,tistory'

    params = {
        'access_token': access_token,
        'output': output_type,
        'blogName': blog_name,
        'title': title,
        'content': content,
        'visibility': visibility,
        'category': category,
        'published': published,
        'tag': tag,
    }

    r = requests.post('https://www.tistory.com/apis/post/write', params=params)

    print(r.json())
