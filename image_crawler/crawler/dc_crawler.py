from crawler.base_crawler import BaseCrawler

class DCCrawler(BaseCrawler):
    def __init__(self, crawler_file_util):
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.file_util.user.get_image_save_path(), 'dcinside')
        

    # Override this method
    def crawler_rule():
        return None