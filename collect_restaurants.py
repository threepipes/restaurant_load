import sys

from scraping.gnavi import GnaviCrawler
from scraping.tabelog import TabelogCrawler
from scraping.hotpepper import HotpepperCrawler


def exec_generate_list(api, url_list):
    api.generate_restaurant_list(url_list)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please set arg: gn/tb/hp')
    api_name = sys.argv[1]
    if api_name == 'gn':
        GnaviCrawler().generate_restaurant_list(['https://r.gnavi.co.jp/area/aream3404/kods00066/rs/'])
    elif api_name == 'tb':
        TabelogCrawler().generate_restaurant_list(['https://tabelog.com/kyoto/C26100/rstLst/'])
    elif api_name == 'hp':
        HotpepperCrawler().generate_restaurant_list(['https://www.hotpepper.jp/yoyaku/SA91/'])
