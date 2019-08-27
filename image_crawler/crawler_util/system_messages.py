from crawler_util.crawler_enum import TargetSite


class ProcessingMessage:

    def get_web_type(netloc):
        if 'twitter' in netloc:
            return TargetSite.TWITTER
        elif 'pixiv' in netloc:
            return TargetSite.PIXIV
        elif 'ruliweb' in netloc:
            return TargetSite.RULIWEB
        elif 'dcinside' in netloc:
            return TargetSite.DCINSIDE


class ErrorMessage:

    DRIVER_ROOT_NOT_FOUND = "Driver root is None!"
    DRIVER_CAN_NOT_OPEN = "Driver can't open!"

    URL_TIMEOUT = "url timeout!"
    UNVALID_URL = "Input url is unvalid!"