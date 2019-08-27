class ErrorLog():

    def print_log(log_text):
        print(log_text)
        log_file = open(work_dir+'\log.txt','a', encoding = "utf-8")
        log_file.write(log_text)
        log_file.close()