from selenium import webdriver
from crawler_user.info import UserInfo


def main(user):
    driver = webdriver.Chrome(user.get_chrome_root())
    

if __name__ == '__main__':
    user = UserInfo()
    main(user)
