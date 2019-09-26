import requests, time, random
from crawler.base_crawler import BaseCrawler
from crawler_info.info import ImageInfo
from crawler_util.crawler_enum import TargetSite, RuliwebPageCase


class RuliwebCrawler(BaseCrawler):
    def __init__(self, crawler_file_util):
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.file_util.user.get_image_save_path(), 'ruliweb')
        self.session = None
        self.login_req_board_num = ['310001', '310002', '310003', '310004', '310005', '310006', '310007']
        

    # Override this method
    def crawler_rule(self, input_url):
        # url형식 또는 html 형식을 파악해 post 또는 board를 실행
        # 필요에 따라 유저 로그인 수행(루리웹은 로그인 필요한 게시판이 한정되어있으므로 로그인 필요한 예외 주소로 구분)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.file_util.user.get_user_agent(),
        })

        page_case = self.detect_page_pattern(input_url)
        if page_case is RuliwebPageCase.BOARD_PAGE:
            self.crawling_board(input_url)
        elif page_case is RuliwebPageCase.POST_PAGE:
            self.crawling_post(input_url)
        return None


    def user_login(self):
        LOGIN_INFO = {
            'user_id': self.file_util.user.get_ruliweb_id(),
            'user_pw': self.file_util.user.get_ruliweb_pw()
        }
        login_result = self.session.post('https://user.ruliweb.com/member/login_proc', data=LOGIN_INFO)


    def detect_page_pattern(self, input_url):
        split_url = input_url.split('board/')[1].split('/')
        if split_url in self.login_req_board_num:
                self.user_login()

        if 'read' in split_url:
            return RuliwebPageCase.POST_PAGE
        else:
            return RuliwebPageCase.BOARD_PAGE


    def crawling_post(self, input_url):
        # request 모듈로 페이지와 댓글 모두 가져와진다면 request로 수행
        # 단일 게시물의 이미지를 모두 다운로드, 설정 여부에 따라 image_reply를 추가 실행
        return None


    def crawling_image_reply(self):
        # 이미지 덧글의 모든 이미지 수집
        return None


    def crawling_board(self, input_url):
        # 보드에서 주소를 확보해 post를 반복 실행
        return None


    def crawling_post_on_selenium(self):
        return None


    def crawling_image_reply_on_selenium(self):
        return None


    def crawling_board_on_selenium(self):
        return None
