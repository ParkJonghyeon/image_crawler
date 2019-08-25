from selenium import webdriver
from crawler_user.info import UserInfo
from system_messages import ErrorMessage
from urllib import parse

# 웹 드라이버 정상 실행 체크
def driver_open(chrome_driver_root):
    if chrome_driver_root == None:
        print(ErrorMessage.DRIVER_ROOT_NOT_FOUND)
    try:
        return webdriver.Chrome(chrome_driver_root)
    except:
        print(ErrorMessage.DRIVER_CAN_NOT_OPEN)
        return None


# 입력 받은 url의 http 포함 여부 체크
def url_scheme_check(target_url):
    valid_check_url = parse.urlparse(target_url)
    if valid_check_url.scheme is '':
        valid_check_url = valid_check_url._replace(scheme='http')
        return valid_check_url.geturl()
    else:
        return target_url


# main 실행 부
def main(user):
    driver = driver_open(user.get_chrome_root())
    input_url = url_scheme_check(input())
    driver.get(input_url)
    
    
if __name__ == '__main__':
    user = UserInfo()
    main(user)
