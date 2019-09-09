import pyperclip
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from crawler.base_crawler import BaseCrawler
from crawler_info.info import ImageInfo
from crawler_util.crawler_enum import TargetSite, PixivPageCase
#픽시브 이미지는 해당 이미지의 url(썸네일 이미지에서 파싱 가능)과 referer 데이터(해당 이미지의 페이지 주소)를 알면
#urllib3의 poolmanager 등으로 직접 접근이 가능
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
        print("베이스 이동")
        self.driver.get(self.base_url)
        print("로그인 처리")
        if len(self.driver.find_elements_by_css_selector('.not-logged-in')) is not 0:
            self.user_login()
        print("입력 url 이동")
        self.driver.get(input_url)
        time.sleep(3)
        print("케이스 판단")
        page_case = self.detect_page_pattern(input_url)
        if page_case is PixivPageCase.ARTIST_TOP_PAGE:
            # 모두보기 클릭한 뒤의 주소를 던저줄 경우의 예외처리가 없음
            self.driver.find_element_by_css_selector('div div a[href*="/member_illust.php?id="] div').click()
            time.sleep(1)
            print("탑 페이지")
            tmp=self.crawling_artist_top_page()
        elif page_case is PixivPageCase.SINGLE_IMG_PAGE:
            print("싱글 페이지")
            tmp=self.crawling_single_img_page()
        elif page_case is PixivPageCase.MULTI_IMG_PAGE:
            print("멀티 페이지")
            tmp=self.crawling_multi_img_page(self.driver.current_url)
        elif page_case is PixivPageCase.ANIMATED_IMG_PAGE:
            print("애니메이션 페이지")
            tmp=self.crawling_animated_img_page()


    def user_login(self):
        if self.file_util.user.get_pixiv_id() is None:
            return False
        else:
            self.driver.get('https://accounts.pixiv.net/login')
            time.sleep(3)
            pyperclip.copy(self.file_util.user.get_pixiv_id())
            self.driver.find_element_by_css_selector('#LoginComponent input[type=text]').click()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform() # Ctrl+V 전달
            time.sleep(1)
            pyperclip.copy(self.file_util.user.get_pixiv_pw())
            self.driver.find_element_by_css_selector('#LoginComponent input[type=password]').click()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform() # Ctrl+V 전달
            time.sleep(1)
            self.driver.find_element_by_css_selector('#LoginComponent button[type=submit]').click()
            time.sleep(5)
            return True


    # 속도가 너무 느림. 입력받은 url을 파싱해서 직접 판단하도록 처리해볼것
    def detect_page_pattern(self, input_url):
        if input_url.split('?')[1][0:2] == 'id':
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
        # 썸네일 리스트에서 얻을 수 있는 정보로 타이틀, 아티스트, 기본 url, 날짜, 레퍼러, 이미지 id를 갖는 img_info
        # 작성
        # 썸네일 리스트에서 싱글, 멀티, 애니메이션 분류, 멀티의 경우 img_num을 img_info에 추가
        # 분류에 따라 각 함수를 실행
        print("공통 정보 획득")
        artist_data = self.driver.find_element_by_css_selector('h1')
        i_a = artist_data.text + '_' + self.driver.current_url.split('id=')[1]
        i_p = self.file_util.join_dir_path(self.image_save_path, i_a)
        print("페이지 탐색 시작")
        while True:
            img_thumb_list = self.driver.find_elements_by_css_selector('div>ul>li>div')
            print("썸네일 정보 입수 시작")
            for img_thumb in img_thumb_list:
                image_info = self.make_image_info_from_image_thumbnail(img_thumb)
                image_info.image_artist, image_info.image_save_path = i_a, i_p
                print("적당한 다운로더 실행")
                if image_info.other_data['img_total_num'] == 1:
                    tmp = self.crawling_single_img_page(image_info)
                elif image_info.other_data['img_total_num'] == 0:
                    tmp = self.crawling_animated_img_page(image_info)
                else:
                    tmp = self.crawling_multi_img_page(image_info)
            print("다음페이지 여부 확인")
            next_page_btn = self.driver.find_element_by_css_selector('a polyline[transform*="rotate(-90"]')
            if next_page_btn.is_displayed():
                next_page_btn.click()
            else:
                break
        return img_info_list


    def crawling_single_img_page(self, image_info=None):
        print("싱글 다운로더")
        # 사용자가 입력한 주소가 single 페이지의 주소인 경우
        if image_info is None:
            image_info = self.make_image_info_from_image_page()
        # top 페이지로부터 호출 된 경우 => 바로 download 작업으로 이동
        self.file_util.image_download_from_image_info(image_info)
        return image_info


    def crawling_multi_img_page(self, image_info=None):
        print("멀티 다운로더")
        image_info_list = []
        # 사용자가 입력한 주소가 multi 페이지의 주소인 경우
        if image_info is None:
            image_info = self.make_image_info_from_image_page()
            img_num = int(self.driver.find_element_by_css_selector('.gtm-manga-viewer-preview-modal-open div').text.split('/')[1])
        # top 페이지로부터 호출 된 경우
        else:
            img_num = image_info.other_data['img_total_num']

        split_url = image_info.image_url.split('p0')
        print("다수의 이미지 반복 다운로드 시작")
        for i_n in range(img_num):
            if i_n is not 0:
                i_u = split_url[0] + 'p' + str(i_n) + split_url[1]
            image_info.image_title = image_info.image_title + '_' + str(i_n)
            image_info.image_url = i_u
            self.file_util.image_download_from_image_info(image_info)
            image_info_list.append(image_info)
        return image_info_list


    def crawling_animated_img_page(self, image_info=None):
        return None


    # 정보 생성 메소드들은 최소한의 탐색으로 끝나게 구조 수정. 현재 방식은 느림
    # 타이틀에 \/:*?"<>| 해당 문자 들어갈경우 파일 쓰기에서 문제 발생 -> 타이틀 필터링 필요
    # 아티스트 탑 페이지의 썸네일로부터 image_info를 생성 할 경우 사용하는 함수
    def make_image_info_from_image_thumbnail(self, thumbnail_source):
        print("썸네일로부터 정보 생성 중")
        i_t = thumbnail_source.find_elements_by_css_selector('a')[1].text #a:last-child에서 에러, 이 방식도 종종 에러 확실한 경로 찾아볼 것
        thumbnail_url_split = thumbnail_source.find_element_by_css_selector('img').get_attribute('src').split('/img/')[1].split('_')
        if len(thumbnail_url_split) == 3:
            i_u = "https://i.pximg.net/img-original/img/" + thumbnail_url_split[0] + '_' + thumbnail_url_split[1] + '.png' # 다운로더가 정보 얻어오기 실패했을 경우 .jpg로 교체하여 재시도, 정확한 값을 얻어올 방법 필요
        else:
            i_u = "https://i.pximg.net/img-original/img/" + thumbnail_url_split[0] + '.gif' # 현재로서는 gif 그림 받을 방법이 없음
        i_d = self.img_url_to_date_and_id(i_u)
        referer_url = thumbnail_source.find_elements_by_css_selector('a')[1].get_attribute('href') #a:last-child에서 에러, 이 방식도 종종 에러 확실한 경로 찾아볼 것
        o_d = {'referer':referer_url, 'img_id':referer_url.split('illust_id=')[1]}
        # multi image
        if len(thumbnail_source.find_elements_by_css_selector('span')) > 0:
            o_d['img_total_num'] = int(thumbnail_source.find_element_by_css_selector('span').text)
        # animated image
        elif len(thumbnail_source.find_elements_by_css_selector('circle')) > 0:
            o_d['img_total_num'] = 0
        # single image
        else:
            o_d['img_total_num'] = 1
        return ImageInfo(image_title = i_t,
                         image_artist = None,
                         image_date = i_d,
                         image_url = i_u,
                         image_save_path = None,
                         image_src = TargetSite.PIXIV,
                         other_data = o_d)


    # 이미지의 페이지로부터 직접적으로 image_info를 생성 할 경우 사용하는 함수
    def make_image_info_from_image_page(self):
        print("이미지 페이지로부터 정보 생성 중")
        i_t = self.driver.find_element_by_css_selector('figcaption h1').text
        artist_data = self.driver.find_element_by_css_selector('aside section h2 div div a')
        i_a = artist_data.text + '_' + artist_data.get_attribute('href').split('id=')[1]
        i_u = self.driver.find_element_by_css_selector('div[role=presentation] a').get_attribute('href')
        i_d = self.img_url_to_date_and_id(i_u)
        i_p = self.file_util.join_dir_path(self.image_save_path, i_a)
        referer_url = self.driver.current_url
        o_d = {'referer':referer_url, 'img_id':referer_url.split('illust_id=')[1]}
        return ImageInfo(image_title = i_t,
                         image_artist = i_a,
                         image_date = i_d,
                         image_url = i_u,
                         image_save_path = i_p,
                         image_src = TargetSite.PIXIV,
                         other_data = o_d)


    def img_url_to_date_and_id(self, img_url):
        return '_'.join(img_url.split('/img/')[1].split('/')[0:6])