import argparse
import logging

from blogspot import BlogspotPostAction
from tistory import TistoryPostAction

release_version = '2024.01.02'

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    service_name = 'Blogspot'
    parser = argparse.ArgumentParser(description=f'Posts auto upload on {service_name}.')

    if service_name == 'Blogspot':
        action = BlogspotPostAction
    elif service_name == 'Tistory':
        action = TistoryPostAction

    parser.add_argument('filename', type=str, help="csv file", action=action)
    args = parser.parse_args()
