import configparser

class UserInfo:

    def __init__(self):
        config_parser = configparser.ConfigParser()
        config_parser.read('./crawler_user/userinfo.ini')
        self.__chrome_ver = config_parser['SYSTEM']['CHROME_VER']
        self.__chrome_driver_root = config_parser['SYSTEM']['CHROME_DIRVER_ROOT']
        self.__pixiv_id = config_parser['ACCOUNT']['PIXIV_ID']
        self.__pixiv_pw = config_parser['ACCOUNT']['PIXIV_PW']

    
    def get_chrome_ver(self):
        return self.__chrome_ver


    def get_chrome_root(self):
        return self.__chrome_driver_root


    def get_pixiv_id(self):
        return self.__pixiv_id


    def get_pixiv_pw(self):
        return self.__pixiv_pw