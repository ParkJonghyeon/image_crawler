import time
from threading import Thread

from crawler.base_crawler import BaseCrawler
from crawler_info.info import ImageInfo

class TwitterCrawler(BaseCrawler):
    def __init__(self, crawler_file_util, crawling_type):
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.file_util.user.get_image_save_path(), 'twitter')
        self.crawling_type = crawling_type
        self.driver = None
        self.start_seconds = 0
        self.end_seconds = 0
        

    # Override this method
    def crawler_rule(self, input_url):
        self.driver.get(input_url)
        self.driver.implicitly_wait(15)
        print("타겟 트위터 사용자의 정보 수집 중")
        self.get_twitter_profile()
        print("입력한 수집 시작점까지 스크롤을 시작합니다.")
        self.scroll_down_until_start_seconds()
        self.get_twitter_contents()


    def get_twitter_profile(self):
        profile_header = self.driver.find_element_by_css_selector('.ProfileHeaderCard')
        # == ('h1 a').text
        profile_name = profile_header.find_element_by_css_selector('.ProfileHeaderCard-nameLink.u-textInheritColor.js-nav').text
        # 트위터 닉네임에 @을 사용하는 경우 @이하 부분 제거용
        if '@' in profile_name:
            profile_name = profile_name.split('@')[0]
        # == ('h2 a').text
        profile_screenname = profile_header.find_element_by_css_selector('.username.u-dir').text
        self.artist_name = profile_name + '_' + profile_screenname
        self.image_save_path = self.file_util.join_dir_path(self.image_save_path, self.artist_name)


    def get_twitter_contents(self):
        # blob 링크는 js를 사용한 영상 다운로드 방법을 시도해볼것
        timeline_contents = self.driver.find_elements_by_css_selector('.stream-container .js-stream-item.stream-item.stream-item')

        for content in reversed(timeline_contents):
            img_list = content.find_elements_by_css_selector('.AdaptiveMediaOuterContainer img')
            if len(img_list) > 0:
                content_seconds = int(content.find_element_by_css_selector('._timestamp.js-short-timestamp').get_attribute('data-time'))
                if self.start_seconds <= content_seconds and content_seconds <= self.end_seconds:
                    content_date = self.file_util.seconds_to_time(content_seconds, '%Y_%m_%d_%H_%M_%S')
                    for idx, img in enumerate(img_list):
                        image_info = ImageInfo(image_title= self.artist_name+'_twitter_'+str(idx),
                                             image_artist= self.artist_name,
                                             image_date= content_date,
                                             image_url=img.get_attribute('src') + ':orig',
                                             image_save_path= self.image_save_path)
                        print(image_info.image_date)
                        #스레드 위치는 이미지 정보를 만드는 부분부터 별개로 분리하여 조정
                        self.file_util.image_download_from_image_info(image_info)


    def scroll_down_until_start_seconds(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            timeline_contents = self.driver.find_elements_by_css_selector('.stream-container .js-stream-item.stream-item.stream-item')
            last_contents_seconds = int(timeline_contents[-1].find_element_by_css_selector('._timestamp.js-short-timestamp').get_attribute('data-time'))
            # 마지막 로딩 된 콘텐츠와 수집 시작 날짜를 비교
            if last_contents_seconds >= self.start_seconds:
                print("입력한 수집 시작점에 해당하는 위치까지 스크롤 중")
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.5)
            else:
                print("입력한 수집 시작점 위치 발견. 수집을 시작합니다.")
                break
            # 더이상 스크롤이 불가능한 경우에도 스크롤 다운 중단
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("더 이상 스크롤 할 수 없습니다. 수집을 시작합니다.")
                break
            last_height = new_height


    def posted_within_period(self, content_seconds):
        if self.start_seconds <= content_seconds and content_seconds <= self.end_seconds:
            return True
        else:
            return False


    def set_crawling_period(self, start_seconds, end_seconds):
        self.start_seconds = start_seconds
        self.end_seconds = end_seconds