from selenium import webdriver
from crawler_util.system_messages import ProcessingMessage, ErrorMessage
from crawler_util.system_logger import ErrorLog


# 모든 크롤러가 가져야할 공통 기능 구현
# 드라이버 실행, 파일 저장, 에러 처리
# 각 크롤러에서 사이트 별로 동작해야하는 명령어 및 작업을 구현
class BaseCrawler():

    def __init__(self, user):
        self.user = user

    
    # 웹 드라이버 정상 실행 체크
    def driver_open(self, chrome_driver_root):
        if chrome_driver_root == None:
            print_log(ErrorMessage.DRIVER_ROOT_NOT_FOUND)
        try:
            return webdriver.Chrome(chrome_driver_root)
        except:
            print_log(ErrorMessage.DRIVER_CAN_NOT_OPEN)
            return None


    def run(self, input_url):
        driver = self.driver_open(self.user.get_chrome_root())
        driver.get(input_url)


    