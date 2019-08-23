from selenium import webdriver
from crawler_user.info import UserInfo
from system_messages import ErrorMessage

def driver_open(chrome_driver_root):
    if chrome_driver_root == None:
        print(ErrorMessage.DRIVER_ROOT_NOT_FOUND)
    try:
        return webdriver.Chrome(chrome_driver_root)
    except:
        print(ErrorMessage.DRIVER_CAN_NOT_OPEN)
        return None


def main(user):
    driver = driver_open(user.get_chrome_root())
    driver.get("https://google.com")
    

if __name__ == '__main__':
    user = UserInfo()
    main(user)
