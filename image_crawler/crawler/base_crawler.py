from selenium import webdriver
import subprocess

from crawler_info.info import ImageInfo
from crawler_util.system_messages import ProcessingMessage, ErrorMessage


# 모든 크롤러가 가져야할 공통 기능 구현
# 드라이버 실행, 에러 처리
# 각 크롤러에서 사이트 별로 동작해야하는 명령어 및 작업을 구현
class BaseCrawler():
    def __init__(self, crawler_file_util):
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.file_util.user.get_image_save_path(), 'base')
                
    
    # 웹 드라이버 정상 실행 체크
    def driver_open(self, chrome_driver_root):
        if chrome_driver_root == None:
            print_log(ErrorMessage.DRIVER_ROOT_NOT_FOUND)
        chrome_option = webdriver.ChromeOptions()
        chrome_option.add_experimental_option('debuggerAddress','127.0.0.1:'+self.file_util.user.get_chrome_port())
        # chrome_option.set_headless(headless=False)
        # chrome_option.add_argument(r'--user-data-dir=C:\Users\Lark\AppData\Local\Google\Chrome\User Data\Default')
        # chrome_option.add_argument(r'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36')
        self.file_util.check_dir_exist(r'.\webdriver\crawler_user_data')
        subp_chrome = subprocess.Popen([r'.\webdriver\chrome_run.bat', self.file_util.user.get_chrome_path(), self.file_util.user.get_chrome_port()], stdout=subprocess.PIPE)
        try:
            return webdriver.Chrome(executable_path=chrome_driver_root, options=chrome_option)
        except:
            print_log(ErrorMessage.DRIVER_CAN_NOT_OPEN)
            return None


    def run(self, input_url):
        if self.image_save_path is not None:
            self.driver = self.driver_open(self.file_util.user.get_chrome_root())
            self.driver.implicitly_wait(30)
            self.crawler_rule(input_url)
            # img = ImageInfo(image_save_path=self.image_save_path, image_url='example.img_url')
            # self.file_util.image_download_from_image_info(img)


    # Override this method
    def crawler_rule(self, input_url):
        self.driver.get(input_url)