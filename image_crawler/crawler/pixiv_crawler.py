import pyperclip, time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from crawler.base_crawler import BaseCrawler
from crawler_info.info import ImageInfo
from crawler_util.crawler_enum import TargetSite, PixivPageCase
#픽시브 이미지는 해당 이미지의 url(썸네일 이미지에서 파싱 가능)과 referer 데이터(해당 이미지의 페이지 주소)를 알면 urllib3의 poolmanager 등으로 직접 접근이 가능
#여러장의 이미지는 span 등의 값으로 개수를 알아올수 있음
#셀레니움은 느리므로 해당 이미지의 썸네일 정도만 긁게 하고 세부적인 파싱은 urllib으로


class PixivCrawler(BaseCrawler):
    def __init__(self, crawler_file_util):
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.file_util.user.get_image_save_path(), 'pixiv')
        self.base_url = 'https://www.pixiv.net'
        

    # Override this method
    def crawler_rule(self, input_url):
        # crawler_user_data에서 브라우저의 프로필을 관리
        # 한번 로그인해두면 재실행시에도 로그인 되어있을 수 있음
        # 실행마다 로그인 상태를 체크하여 유저정보 ini에 픽시브 계정 데이터가 있는 경우만 로그인 시도
        self.driver.get(self.base_url)
        if len(self.driver.find_elements_by_css_selector('.not-logged-in')) is not 0:
            self.user_login()
        self.driver.get(input_url)
        time.sleep(5)
        page_case = self.detect_page_pattern(input_url)
        if page_case is PixivPageCase.ARTIST_TOP_PAGE:
            self.crawling_artist_top_page()
        elif page_case is PixivPageCase.SINGLE_IMG_PAGE:
            self.crawling_single_img_page(self.driver.current_url)
        elif page_case is PixivPageCase.MULTI_IMG_PAGE:
            self.crawling_multi_img_page(self.driver.current_url)
        elif page_case is PixivPageCase.ANIMATED_IMG_PAGE:
            self.crawling_animated_img_page()


    def user_login(self):
        if self.file_util.user.get_pixiv_id() is None:
            return False
        else:
            self.driver.get('https://accounts.pixiv.net/login')
            self.file_util.time.sleep(5)
            pyperclip.copy(self.file_util.user.get_pixiv_id())
            self.driver.find_element_by_css_selector('#LoginComponent input[type=text]').click()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform() # Ctrl+V 전달
            time.sleep(1)
            pyperclip.copy(self.file_util.user.get_pixiv_pw())
            self.driver.find_element_by_css_selector('#LoginComponent input[type=password]').click()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform() # Ctrl+V 전달
            time.sleep(1)
            self.driver.find_element_by_css_selector('#LoginComponent button[type=submit]').click()
            time.sleep(15)
            return True


    def detect_url_pattern(self, input_url):
        
        if input_url.split('?')[1][0:2] is 'id':
            return PixivPageCase.ARTIST_TOP_PAGE        #주소 패턴으로 탑 페이지와 뷰 페이지를 구분
        else:
            view_area = self.driver.find_element_by_css_selector('div[role=presentation]')
            picture_area = view_area.find_elements_by_css_selector('div[role=presentation]>div')
            if len(picture_area) == 0:
                return PixivPageCase.ANIMATED_IMG_PAGE  #div[role=presentation] 하위에 canvas
            elif len(picture_area) == 1:
                return PixivPageCase.SINGLE_IMG_PAGE    #div[role=presentation] 하위에 이미지를 위한 단일 div
            else:
                return PixivPageCase.MULTI_IMG_PAGE     #div[role=presentation] 하위에 이미지와 미리보기를 위한 2개의 div


    # 픽시브 이미지는 이미지의 i.pximg 주소를 파싱하여 원본 주소, 작성 날짜 파악 가능
    # 이미지의 종류에 따라 single, multi, animated 호출
    def crawling_artist_top_page(self):
        img_info_list = []
        return img_info_list


    def crawling_single_img_page(self, referer_url):
        # 아티스트 정보 획득 후 저장 경로 재설정
        referer_data = {'referer':referer_url}
        img_info = ImageInfo(image_title='',
                             image_artist='',
                             image_date='',
                             image_url='',
                             image_save_path=self.image_save_path,
                             image_src=TargetSite.PIXIV,
                             other_data=referer_data)
        return list(img_info)


    def crawling_multi_img_page(self, referer_url):
        img_info_list = []
        referer_data = {'referer':referer_url}
        return img_info_list


    def crawling_animated_img_page(self):
        return None