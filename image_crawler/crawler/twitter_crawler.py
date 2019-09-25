from crawler.base_crawler import BaseCrawler
from crawler_info.info import ImageInfo

class TwitterCrawler(BaseCrawler):
    def __init__(self, crawler_file_util):
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.file_util.user.get_image_save_path(), 'twitter')
        self.driver = None
        

    # Override this method
    def crawler_rule(self, input_url):
        self.driver.get(input_url)
        self.driver.implicitly_wait(15)

        while True:
            self.get_twitter_profile()
            self.get_twitter_contents()
            if self.can_scroll_down():
                continue
            break


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
        # 구조 일관성 유지를 위해 해당 함수는 선별 된 timeline_contents에 대해서 반복 작업만 수행하도록 변경
        # html 내에서 페이지의 스크롤 및 로드 된 timeline_contents를 찾는 것은 별도의 함수로 작업
        timeline = self.driver.find_element_by_css_selector('#timeline')
        timeline_contents = timeline.find_elements_by_css_selector('.js-stream-item.stream-item.stream-item')

        for content in timeline_contents:
            img_list = content.find_elements_by_css_selector('.AdaptiveMediaOuterContainer img')
            if len(img_list) > 0:
                content_seconds = int(content.find_element_by_css_selector('._timestamp.js-short-timestamp').get_attribute('data-time'))
                content_date = self.file_util.seconds_to_time(content_seconds, '%Y_%m_%d_%H_%M_%S')
                for img in img_list:
                    img_info = ImageInfo(image_title= 'twitter',
                                         image_artist= self.artist_name,
                                         image_date= content_date,
                                         image_url=img.get_attribute('src') + ':orig',
                                         image_save_path= self.image_save_path)
                    print(img_info)


    def can_scroll_down(self):
        return False
        

    def posted_within_period(self, content_seconds):
        return True