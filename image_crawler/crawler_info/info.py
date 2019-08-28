import configparser


class UserInfo():

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('./crawler_info/userinfo.ini')
        self.__chrome_ver = config_parser['SYSTEM']['CHROME_VER']
        self.__chrome_driver_root = config_parser['SYSTEM']['CHROME_DIRVER_ROOT']
        self.__default_timeout = float(config_parser['SYSTEM']['DEFAULT_TIMEOUT'])
        self.__image_save_path = config_parser['SYSTEM']['IMAGE_SAVE_PATH']
        self.__pixiv_id = config_parser['ACCOUNT']['PIXIV_ID']
        self.__pixiv_pw = config_parser['ACCOUNT']['PIXIV_PW']

    
    def get_chrome_ver(self):
        return self.__chrome_ver


    def get_chrome_root(self):
        return self.__chrome_driver_root


    def get_default_timeout(self):
        return self.__default_timeout


    def get_image_save_path(self):
        return self.__image_save_path


    def get_pixiv_id(self):
        return self.__pixiv_id


    def get_pixiv_pw(self):
        return self.__pixiv_pw


class ImageInfo():

    def __init__(self, image_title = 'default_title', image_artist = 'unknown_artist', image_date = 'unknown_date', image_url = None, image_save_path = None):
        self.image_title = image_title
        self.image_artist = image_artist
        self.image_date = image_date
        self.image_url = image_url
        self.image_save_path = image_save_path