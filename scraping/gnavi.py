from logging import getLogger, DEBUG, StreamHandler
from scraping.common import Crawler, Extracter
from pyquery import PyQuery as pq

logger = getLogger(__file__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

restaurant_tag_name = 'div.result-cassette__box-head a'
nextpage_position = 'a.pagination__arrow-item-inner-next'
basename = 'gnavi'


class GnaviCrawler(Crawler):
    def __init__(self):
        super().__init__({
            'restaurant': restaurant_tag_name,
            'nextpage': nextpage_position,
        }, basename=basename)


class GnaviExtracter(Extracter):
    def __init__(self):
        super().__init__({'tel': 'div.phone-guide__number'}, basename=basename)

    def get_phone_number(self, dom: pq):
        inner_dom = dom(self.tel_location)
        if not inner_dom:
            inner_dom = dom('div#header-main-phone-info span')
        return inner_dom.text().strip()



if __name__ == '__main__':
    api = GnaviCrawler()
    api.generate_restaurant_list(['https://r.gnavi.co.jp/area/aream3404/kods00066/rs/'])
