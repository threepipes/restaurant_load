import sys

from scraping.gnavi import GnaviExtracter
from scraping.tabelog import TabelogExtracter
from scraping.hotpepper import HotpepperExtracter
from scraping.ikyu import IkyuExtracter


def exec_extract_list(api):
    api.extract()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please set arg: gn/tb/hp/ik')
    api_name = sys.argv[1]
    if api_name == 'gn':
        GnaviExtracter().extract()
    elif api_name == 'tb':
        TabelogExtracter().extract()
    elif api_name == 'hp':
        HotpepperExtracter().extract()
    elif api_name == 'ik':
        IkyuExtracter().extract()
