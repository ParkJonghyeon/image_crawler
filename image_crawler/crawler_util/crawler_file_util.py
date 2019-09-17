import os
from urllib3 import poolmanager
import shutil
import time

from crawler_util.crawler_enum import TargetSite


# 차후에 싱글톤 클래스로 구현 시도할 것
class CrawlerFileUtil():
    def __init__(self, crawler_user, system_logger):
        self.pool_manager = poolmanager.PoolManager()
        self.user = crawler_user
        self.logger = system_logger
        self.stop_word = ['\\','/',':','*','?','"','<','>','|' ]


    # diretory 함수
    # 현재 작업 디렉토리, 주어진 경로명의 병합, 디렉토리의 존재 체크, 중복 파일명 체크
    def current_work_dir(self):
        return os.getcwd()


    def join_dir_path(self, base_path, *target_path):
        join_path = os.path.join(base_path, *target_path)
        if self.check_dir_exist(join_path) is True:
            return join_path
        else:
            return None


    def check_dir_exist(self, check_dir_path):
        try:
            if os.path.exists(check_dir_path) is True:
                return True
            else:
                os.makedirs(check_dir_path)
                return True
        except Exception as e_log:
            self.system_logger.print_log(e_log)
            return False


    def join_file_path(self, dir_path, file_name):
        join_path = os.path.join(dir_path, file_name)
        if self.check_file_exist(join_path) is False:
            return join_path
        else:
            return None


    def check_file_exist(self, check_file_path):
        return os.path.isfile(check_file_path)            


    # file download 함수
    # Doing resp.release_conn() with preload_content=False is required so that the connection can be reused by the pool manager. 
    def image_download_from_image_info(self, image_info):
        save_file_name = self.file_name_filter(image_info.image_date + '_' + image_info.image_title + '.png')
        save_file_root = self.join_file_path(image_info.image_save_path, save_file_name)
        
        if save_file_root is not None:
            print(image_info)
            print(image_info.image_url)
            # pixiv의 경우 orig 이미지에 접근하기 위해서 헤더에 referer가 필요
            if image_info.image_src is TargetSite.PIXIV:
                referer_headers={'Referer':image_info.other_data['referer']}
                resp = self.pool_manager.request('GET', image_info.image_url, headers=referer_headers, preload_content=False)
                # pixiv의 경우 jpg인지 png인지 확실하지 않아 png로 시도 후 실패하면 jpg로 재시도 -> 썸네일 크롤러에서 urllib과 bs4를 이용한 수집 방식으로 수정하면 제거
                if resp.status == 404:
                    resp = self.pool_manager.request('GET', image_info.image_url[:-4]+'.jpg', headers=referer_headers, preload_content=False)
            else:
                resp = self.pool_manager.request('GET', image_info.image_url, preload_content=False)
            out_file = open(save_file_root, 'wb')
            out_file.write(resp.data)
            out_file.close()
            resp.release_conn()
        else:
            print("이미 존재하는 이미지 파일!")


    # 시간 표기 함수
    # 현재 내 지역 기준으로 시간을 구하므로 localtime 사용
    def seconds_to_time(self, seconds_val, time_format='%Y_%m_%d'):
        return time.strftime(time_format, time.localtime(seconds_val))


    # 파일 이름에 사용 금지 된 문자 필터링
    def file_name_filter(self, file_name):
        for sw in self.stop_word:
            if sw in file_name:
                file_name = file_name.replace(sw,'_')
        return file_name