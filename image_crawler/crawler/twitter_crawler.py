from crawler.base_crawler import BaseCrawler
from crawler_info.info import ImageInfo

class TwitterCrawler(BaseCrawler):
    def __init__(self, crawler_user, crawler_file_util, use_selenium=True):
        self.user = crawler_user
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.user.get_image_save_path(), 'twitter')
        self.use_selenium = use_selenium
        

    # Override this method
    def crawler_rule(self, input_url):
        self.driver.get(input_url)
        self.driver.implicitly_wait(15)
        self.get_twitter_profile()
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
        self.artist_name = profile_name + '(' + profile_screenname + ')'
        self.image_save_path = self.file_util.join_dir_path(self.image_save_path, self.artist_name)


    def get_twitter_contents(self):
        #blob 링크는 js를 사용한 영상 다운로드 방법을 시도해볼것
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
        
