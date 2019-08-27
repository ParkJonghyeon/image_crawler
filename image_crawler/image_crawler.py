from selenium import webdriver
from urllib3 import util, poolmanager
import os
import time

from crawler_user.info import UserInfo
from crawler_util.system_messages import ProcessingMessage, ErrorMessage
from crawler_util.system_logger import ErrorLog


# 웹 드라이버 정상 실행 체크
def driver_open(chrome_driver_root):
    if chrome_driver_root == None:
        print_log(ErrorMessage.DRIVER_ROOT_NOT_FOUND)
    try:
        return webdriver.Chrome(chrome_driver_root)
    except:
        print_log(ErrorMessage.DRIVER_CAN_NOT_OPEN)
        return None


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
            print_log(ErrorMessage.UNVALID_URL)
            return valid_check_url.url, None
    except Exception as e_log:
        print_log(ErrorMessage.URL_TIMEOUT)
        print_log(e_log)
        return valid_check_url.url, None


# main 실행 부
def main():
    input_url, web_type = url_scheme_check(input())
    
    if web_type is not None:
        driver = driver_open(user.get_chrome_root())
        driver.get(input_url)

    
if __name__ == '__main__':
    work_dir = os.getcwd()
    user = UserInfo()
    default_timeout = user.get_default_timeout()
    main()
