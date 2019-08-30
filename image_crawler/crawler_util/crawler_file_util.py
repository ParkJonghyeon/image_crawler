import os
from urllib3 import poolmanager
import shutil


# 차후에 싱글톤 클래스로 구현 시도할 것
class CrawlerFileUtil():
    def __init__(self, crawler_user, system_logger):
        self.pool_manager = poolmanager.PoolManager()
        self.user = crawler_user
        self.logger = system_logger


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
        print(image_info)
        print(image_info.image_url)
        resp = self.pool_manager.request('GET', image_info.image_url, preload_content=False)
        out_file = open(self.join_file_path(image_info.image_save_path,'test.jpg'), 'wb')
        shutil.copyfileobj(resp, out_file)
        out_file.close()
        resp.release_conn()
