# image_crawler

개인 공부 및 취미용으로 제작 된 Python 기반 이미지 다운로드용 크롤러입니다.
requests 모듈과 cssselector 기반으로 크롤링 및 파싱을 통한 이미지 다운로드를 수행합니다.
JavaScript 및 CAPTCHA 문제 해결을 위해 보조적으로 Selenium을 이용하여 우회합니다.
본 크롤러는 Chrome 66버전을 기반으로 구성되었습니다.

---

# How to Use

현재 크롤링이 정상적으로 동작 되도록 구현 된 것은 Twitter/Pixiv/루리웹입니다.

### user_info.ini

crawler_info 폴더의 user_info.ini에 필수 설정을 작성합니다.

[SYSTEM]
* CHROME_VER : 사용 크롬의 버전을 입력합니다.\n 본 프로젝트는 66버전을 기준으로 개발 되었습니다.
* CHROME_DIRVER_ROOT : 크롬 웹 드라이버의 경로를 입력 받습니다. 자신의 크롬 버전에 맞는 웹 드라이버가 필요합니다.
* CHROME_PATH : 설치 된 크롬이 위치한 경로를 입력 받습니다. 본 프로젝트는 디폴트 설치 경로를 사용합니다.
* CHROME_PORT : Selenium을 사용한 크롬의 외부 제어를 위한 debuggerAddress용 포트입니다. 적당한 미사용 포트를 입력합니다.
* DEFAULT_TIMEOUT : 다운로드 및 크롤링 시 디폴트 타임 아웃 값입니다.
* IMAGE_SAVE_PATH : 이미지가 저장 될 경로입니다. 해당 경로에 사이트별 하위 폴더가 생성 됩니다.
* USER_AGENT : 크롤러의 user-agent 값입니다.

[ACCOUNT]
* 유저의 어카운트 정보입니다. 현재는 Pixiv ID/PW, 루리웹 ID/PW만을 입력할 수 있습니다.

### Twitter

수집하려는 이미지를 업로드한 사용자의 최상위 주소를 입력 받습니다.
ex) https://twitter.com/{user_id}

* 현재 Twitter 크롤링은 해당 트위터의 가장 과거 이력까지 거슬러 올라가며 수집합니다.
* 차후 입력 받은 기간 내의 이미지만 다운로드 하도록 수정 예정입니다.

### Pixiv

수집하려는 이미지의 주소, 유저의 페이지 주소를 입력 받습니다.
ex1) https://www.pixiv.net/artworks/{illust_id}
ex2) https://www.pixiv.net/member.php?id={user_id}

* 현재 개발 중인 단계로 정상 동작을 보증하지 않습니다.

### 루리웹

수집하려는 이미지가 위치한 게시글의 주소를 입력 받습니다.
ex) https://bbs.ruliweb.com/community/board/300143/read/{post_num}

* 차후 이미지 댓글의 이미지 다운로드, 검색 결과의 모든 게시물 내 이미지 다운로드 등을 추가할 예정입니다.
