from urllib3 import util, poolmanager
import os, time

from crawler_info.info import UserInfo
from crawler_util.system_messages import ProcessingMessage, ErrorMessage
from crawler_util.system_logger import SystemLogger
from crawler_util.crawler_enum import TargetSite
from crawler_util.crawler_file_util import CrawlerFileUtil
from crawler import *


# 입력 받은 url의 https 포함 여부 체크
# 타겟 사이트들은 https를 기본 지원하므로 http는 고려하지 않음
def url_scheme_check(target_url):
    valid_check_url = util.parse_url(target_url)
    if valid_check_url.scheme is None:
        valid_check_url = valid_check_url._replace(scheme='https')
    try:
        open_test = poolmanager.PoolManager().request('GET', valid_check_url.url, timeout=float(default_timeout))
        if open_test.status == 200:
            return valid_check_url.url, ProcessingMessage.get_web_type(valid_check_url.netloc)
        else:
            logger.print_log(ErrorMessage.UNVALID_URL)
            return valid_check_url.url, None
    except Exception as e_log:
        logger.print_log(ErrorMessage.URL_TIMEOUT)
        logger.print_log(e_log)
        return valid_check_url.url, None


# main 실행 부
def main():
    while True:
        user_input = input()
        if user_input == 'quit':
            break
        input_url, web_type = url_scheme_check(user_input)
    
        if web_type is TargetSite.TWITTER:
            input_url = input_url+'/media'
            img_crawler = twitter_crawler.TwitterCrawler(file_util)
        elif web_type is TargetSite.PIXIV:
            img_crawler = pixiv_crawler.PixivCrawler(file_util)
        elif web_type is TargetSite.RULIWEB:
            img_crawler = ruliweb_crawler.RuliwebCrawler(file_util)
        elif web_type is TargetSite.DCINSIDE:
            img_crawler = dc_crawler.DCCrawler(file_util)
        else:
            img_crawler = base_crawler.BaseCrawler(file_util)
        img_crawler.run(input_url)

    
if __name__ == '__main__':
    work_dir = os.getcwd()
    user = UserInfo()
    logger = SystemLogger(work_dir)
    file_util = CrawlerFileUtil(user, logger)
    default_timeout = user.get_default_timeout()
    main()
