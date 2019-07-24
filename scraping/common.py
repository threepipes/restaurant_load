from typing import List
from pyquery import PyQuery as pq
from logging import getLogger, DEBUG, StreamHandler
from requests import Session, Response
from urllib.parse import urljoin
import datetime
import os
import time
import re

logger = getLogger(__file__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

base_dir = './output/'

class Crawler:
    def __init__(self, settings, basename='none', encoding=None):
        self.restaurant_tag_name = settings['restaurant']
        self.nextpage_position = settings['nextpage']
        self.basename = basename
        self.session = Session()
        self.encoding = encoding

    def generate_restaurant_list(self, list_page_urls: List[str]):
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M')
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        filename = f'{base_dir}{self.basename}_{timestamp}.csv'
        with open(filename, 'w') as f:
            f.write('name,url\n')
            for list_page in list_page_urls:
                res = self.session.get(list_page)
                if self.encoding:
                    res.encoding = self.encoding
                dom = pq(res.text)
                while True:
                    for restaurant in self.get_restaurant_list(dom, res):
                        f.write('{name},{url}\n'.format(**restaurant))
                    f.flush()
                    next_url = self.get_nextlink(dom, res)
                    if not next_url:
                        break
                    time.sleep(1)
                    res = self.session.get(next_url)
                    if self.encoding:
                        res.encoding = self.encoding
                    dom = pq(res.text)

    def get_restaurant_list(self, dom: pq, res: Response):
        restaurant_list = []
        for item in dom(self.restaurant_tag_name):
            restaurant_dom = pq(item)
            url = urljoin(res.url, restaurant_dom.attr('href'))
            restaurant = {
                'name': restaurant_dom.text().replace('　', ' ') + ' ' + 'Retty',
                'url': url,
            }
            restaurant_list.append(restaurant)
            logger.debug(restaurant)
        return restaurant_list

    def get_nextlink(self, dom: pq, res: Response):
        next_link = dom(self.nextpage_position)
        if not next_link:
            return None
        next_link_dom = pq(next_link)
        next_url = urljoin(res.url, next_link_dom.attr('href'))
        return next_url


class Extracter:
    def __init__(self, settings: dict, basename='none'):
        self.basename = basename
        self.tel_location = settings.get('tel', '')
        self.eval_score_location = settings.get('eval_score', '')
        self.extract_elements = [
            'name', 'url', 'tel', '050', 'eval_score'
        ]

    def extract(self):
        cands = []
        for path in os.listdir(base_dir):
            if re.search(self.basename + r'_\d+\.csv', path):
                cands.append(path)
        if not cands:
            logger.info('No basefile: You need to generate restaurants list.')
            return
        cands.sort()
        filename = cands[-1]
        self.extract_restaurants(filename)

    def extract_restaurants(self, filename: str):
        restaurant_list = self._get_list(base_dir + filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M')
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        filename = f'{base_dir}{self.basename}_list_{timestamp}.csv'

        with open(filename, 'w') as f:
            f.write(','.join(self.extract_elements) + '\n')
            for i, restaurant in enumerate(restaurant_list):
                data = self.get_restaurant_data(restaurant['url'])
                data['name'] = data.get('name', restaurant['name'])

                row = ','.join(map(lambda key: data[key], self.extract_elements))
                f.write(row + '\n')
                logger.debug(f'{i}/{len(restaurant_list)}: {data}')
                f.flush()
                time.sleep(1)

    def _get_list(self, filename: str):
        result = []
        header = None
        with open(filename) as f:
            for row in f:
                cols = row.strip().split(',')
                if header is None:
                    header = cols
                    continue
                data = {}
                for key, col in zip(header, cols):
                    data[key] = col
                result.append(data)
        return result

    def get_restaurant_data(self, restaurant_url: str):
        dom = pq(restaurant_url)
        tel = self.get_phone_number(dom)
        eval_score = self.get_eval_score(dom)
        is_050 = 'o' if re.match('050', tel) else ''
        return {
            'tel': tel,
            'url': restaurant_url,
            '050': is_050,
            'eval_score': eval_score
        }

    def get_phone_number(self, dom: pq):
        return dom(self.tel_location).text().strip()

    def get_eval_score(self, dom: pq):
        if self.eval_score_location:
            return dom(self.eval_score_location).text().strip()
        else:
            return ''


# if __name__ == '__main__':
#     generate_restaurant_list(['https://tabelog.com/tokyo/A1305/A130501/R8141/rstLst/RC02/'])
