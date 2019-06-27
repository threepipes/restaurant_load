from logging import getLogger, DEBUG, StreamHandler
from scraping.common import Crawler, Extracter
from pyquery import PyQuery as pq
from requests import Response
from urllib.parse import urljoin
import re

logger = getLogger(__file__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

restaurant_tag_name = 'div.tagPlan_resContent p.this_name a'
nextpage_position = 'link[rel="next"]'
basename = 'ikyu'


class IkyuCrawler(Crawler):
    def __init__(self):
        super().__init__({
            'restaurant': restaurant_tag_name,
            'nextpage': nextpage_position,
        }, basename=basename, encoding='Shift_JIS')


class IkyuExtracter(Extracter):
    def __init__(self):
        super().__init__({'tel': 'span.guide-BasicInfo-tel_dd-reserve'}, basename=basename)

    def get_restaurant_data(self, restaurant_url: str):
        dom = pq(restaurant_url)
        is_050 = ''
        for link in dom('a'):
            plan_cand = pq(link).attr('href')
            if '?' in plan_cand:
                url_pre = plan_cand.split('?')[0]
                if url_pre in restaurant_url:
                    is_050 = 'o'
        try:
            tel = self.get_phone_number(dom)
        except Exception as e:
            logger.error(e)
            tel = ''
        if re.match('050', tel):
            is_050 = 'o'
        return {'tel': tel, 'url': restaurant_url, '050': is_050}


if __name__ == '__main__':
    api = IkyuCrawler()
    api.generate_restaurant_list(['https://restaurant.ikyu.com/area/tokyo/007/0018/'])
