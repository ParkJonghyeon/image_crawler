from enum import Enum


class TargetSite(Enum):
    TWITTER = 1000
    PIXIV = 1001
    RULIWEB = 1002
    DCINSIDE = 1003


class PixivPageCase(Enum):
    ARTIST_TOP_PAGE = 9000
    ARTIST_TOP_PAGE_VIEW_ALL = 9001
    SINGLE_IMG_PAGE = 9002
    MULTI_IMG_PAGE = 9003
    ANIMATED_IMG_PAGE = 9004
