from enum import Enum


class TargetSite(Enum):
    TWITTER = 1000
    PIXIV = 1001
    RULIWEB = 1002
    DCINSIDE = 1003


class PixivPageCase(Enum):
    ARTIST_TOP_PAGE = 9000
    SINGLE_IMG_PAGE = 9001
    MULTI_IMG_PAGE = 9002
    ANIMATED_IMG_PAGE = 9003
