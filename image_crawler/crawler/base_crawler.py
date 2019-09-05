from selenium import webdriver

from crawler_info.info import ImageInfo
from crawler_util.system_messages import ProcessingMessage, ErrorMessage


# 모든 크롤러가 가져야할 공통 기능 구현
# 드라이버 실행, 에러 처리
# 각 크롤러에서 사이트 별로 동작해야하는 명령어 및 작업을 구현
class BaseCrawler():
    def __init__(self, crawler_user, crawler_file_util, use_selenium=True):
        self.user = crawler_user
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.user.get_image_save_path(), 'base')
        self.use_selenium = use_selenium
                
    
    # 웹 드라이버 정상 실행 체크
    def driver_open(self, chrome_driver_root):
        if chrome_driver_root == None:
            print_log(ErrorMessage.DRIVER_ROOT_NOT_FOUND)
        chrome_option = webdriver.ChromeOptions()
        chrome_option.set_headless(headless=True)
        try:
            return webdriver.Chrome(executable_path=chrome_driver_root)
        except:
            print_log(ErrorMessage.DRIVER_CAN_NOT_OPEN)
            return None


    def run(self, input_url):
        if self.image_save_path is not None:
            if self.use_selenium is True:
                self.driver = self.driver_open(self.user.get_chrome_root())
            self.crawler_rule(input_url)
            # img = ImageInfo(image_save_path=self.image_save_path, image_url='example.img_url')
            # self.file_util.image_download_from_image_info(img)


    # Override this method
    def crawler_rule(self, input_url):
        self.driver.get(input_url)