from logging import getLogger, DEBUG, StreamHandler
from scraping.common import Crawler, Extracter

logger = getLogger(__file__)
logger.addHandler(StreamHandler())
logger.setLevel(DEBUG)

restaurant_tag_name = 'div.list-rst__rst-name a'
nextpage_position = 'li.c-pagination__item a[rel="next"]'
basename = 'tabelog'


class TabelogCrawler(Crawler):
    def __init__(self):
        super().__init__({
            'restaurant': restaurant_tag_name,
            'nextpage': nextpage_position,
        }, basename=basename)


class TabelogExtracter(Extracter):
    def __init__(self):
        super().__init__({
            'tel': 'p.rstdtl-side-yoyaku__tel-number',
            'eval_score': 'span.rdheader-rating__score-val-dtl',
        }, basename=basename)


if __name__ == '__main__':
    tableau = TabelogCrawler()
    tableau.generate_restaurant_list(['https://tabelog.com/tokyo/A1305/A130501/R8141/rstLst/RC02/'])
