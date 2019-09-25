from crawler.base_crawler import BaseCrawler

class RuliwebCrawler(BaseCrawler):
    def __init__(self, crawler_file_util):
        self.file_util = crawler_file_util
        self.image_save_path = self.file_util.join_dir_path(self.file_util.user.get_image_save_path(), 'ruliweb')
        self.driver = None
        

    # Override this method
    def crawler_rule():
        return None
