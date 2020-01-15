import sys

class LogToFile:
    def __init__(self,file_name, file_err_name):
        self.file = open(file_name, "w")
        self.file_err = open(file_err_name, "w")
        self.file_err_name = file_err_name

    def log_info(self, message):
        temp = sys.stdout
        sys.stdout = self.file 
        print(message)
        
        sys.stderr.flush()
        sys.stdout.flush()
        sys.stdout = temp

    def log_error(self, message):
        print(f'[-] An error has ocurred - see file: {self.file_err_name}')

        temp = sys.stdout
        sys.stdout = self.file_err 
        print(message)
        
        sys.stderr.flush()
        sys.stdout.flush()
        sys.stdout = temp