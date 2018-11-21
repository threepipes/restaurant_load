from logging import getLogger, DEBUG, StreamHandler
from scraping.common import Crawler, Extracter
from pyquery import PyQuery as pq
from requests import Response
from urllib.parse import urljoin

logger = getLogger(__file__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

restaurant_tag_name = 'h3.detailShopNameTitle a'
nextpage_position = 'ul.searchResultPageLink a'
basename = 'hotpepper'


class HotpepperCrawler(Crawler):
    def __init__(self):
        super().__init__({
            'restaurant': restaurant_tag_name,
            'nextpage': nextpage_position,
        }, basename=basename)

    def get_nextlink(self, dom: pq, res: Response):
        for link in dom(self.nextpage_position):
            inner_dom = pq(link)
            button_image = inner_dom('img')
            if '次へ' in button_image.attr('alt'):
                url = urljoin(res.url, inner_dom.attr('href'))
                return url
        return None


class HotpepperExtracter(Extracter):
    def __init__(self):
        super().__init__({'tel': 'p.tel span'}, basename=basename)


if __name__ == '__main__':
    api = HotpepperCrawler()
    api.generate_restaurant_list(['https://www.hotpepper.jp/yoyaku/SA91/'])
