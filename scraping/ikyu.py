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


if __name__ == '__main__':
    api = IkyuCrawler()
    api.generate_restaurant_list(['https://restaurant.ikyu.com/area/tokyo/007/0018/'])
