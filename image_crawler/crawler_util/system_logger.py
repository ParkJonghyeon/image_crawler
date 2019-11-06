class SystemLogger():

    def __init__(self, work_dir):
        self.work_dir = work_dir


    def print_log(self, log_text):
        print(log_text)
        log_file = open(self.work_dir+'\log.txt','a', encoding = "utf-8")
        log_file.write(log_text)
        log_file.close()