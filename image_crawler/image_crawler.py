from urllib3 import util, poolmanager
import os, time

from crawler_info.info import UserInfo
from crawler_util.system_messages import ProcessingMessage, ErrorMessage
from crawler_util.system_logger import SystemLogger
from crawler_util.crawler_enum import TargetSite, CrawlingType
from crawler_util.crawler_file_util import CrawlerFileUtil
from crawler.twitter_crawler import TwitterCrawler
from crawler.pixiv_crawler import PixivCrawler
from crawler.ruliweb_crawler import RuliwebCrawler
from crawler.dc_crawler import DCCrawler


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
    prev_web_type = None
    img_crawler = None
    while True:
        user_input = input()
        if user_input == 'quit':
            break
        input_url, web_type = url_scheme_check(user_input)
    
        # 최초/이전 작업과 다른 사이트를 크롤링 할 경우 크롤러 객체를 재생성
        # 동일한 사이트에서 반복 작업이라면 생성 된 객체를 재사용
        if prev_web_type != web_type:
            # 기존에 생성 된 크롤러 객체가 있다면 열려있는 웹 드라이버를 종료
            if img_crawler is not None:
                img_crawler.driver_close()
            # 목적 사이트에 맞는 크롤러 객체 생성
            if web_type is TargetSite.TWITTER:
                input_url = input_url+'/media'
                img_crawler = TwitterCrawler(file_util, CrawlingType.DRIVER)
            elif web_type is TargetSite.PIXIV:
                img_crawler = PixivCrawler(file_util, CrawlingType.DRIVER)
            elif web_type is TargetSite.RULIWEB:
                img_crawler = RuliwebCrawler(file_util, CrawlingType.SESSION)
            elif web_type is TargetSite.DCINSIDE:
                img_crawler = DCCrawler(file_util, CrawlingType.SESSION)
            else:
                img_crawler = base_crawler.BaseCrawler(file_util, CrawlingType.DRIVER)
        img_crawler.run(input_url)
        prev_web_type = web_type

    
if __name__ == '__main__':
    work_dir = os.getcwd()
    user = UserInfo()
    logger = SystemLogger(work_dir)
    file_util = CrawlerFileUtil(user, logger)
    default_timeout = user.get_default_timeout()
    main()
