import os
from datetime import datetime


class Logging:

    def __init__(self, file_name, path=None, level='All'):
        """
        Create log file or del and create new if existed, by default create file near Utility
        :param file_name: name log file
        :param path: path where must be saved log file (feature in development yet)
        :param level: Level loging: All - save all logs, Error - not save for warning and inf,
                                    Debug - not save inf.
        """
        self.path = path
        self.file_name = file_name
        self.level = level

        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        if not os.path.exists(self.file_name):
            log_file = open(self.file_name, "w", encoding='utf-8')
            log_file.write(f"{datetime.now()} - Start execute" + '\n')
            log_file.close()

    # old log type - test log which write always
    def add_log(self, string):
        log_file = open(self.file_name, "a", encoding='utf-8')
        log_file.write(f"{datetime.now()} - " + string + '\n')
        log_file.close()

    def error_log(self, string):
        log_file = open(self.file_name, "a", encoding='utf-8')
        log_file.write(f"{datetime.now()} - ERROR: " + string + '\n')
        log_file.close()

    def debug_log(self, string):
        if self.level in {"All", "Debug"}:
            log_file = open(self.file_name, "a", encoding='utf-8')
            log_file.write(f"{datetime.now()} - DebugLog: " + string + '\n')
            log_file.close()

    def warning_log(self, string):
        if self.level in {"All", "Debug"}:
            log_file = open(self.file_name, "a", encoding='utf-8')
            log_file.write(f"{datetime.now()} - Warning: " + string + '\n')
            log_file.close()

    def info_log(self, string):
        if self.level in {"All"}:
            log_file = open(self.file_name, "a", encoding='utf-8')
            log_file.write(f"{datetime.now()} - InfoLog: " + string + '\n')
            log_file.close()

    def del_log_file(self):
        os.remove(self.file_name)


class Errors:
    """
    Save errors for output after parse and log all errors in log file
    """
    def __init__(self, log_class):
        self.errors_list = list()
        self.errors_strings = str()
        self.log_class = log_class

    def add_error(self, error_string):
        self.errors_list.append(error_string)
        self.errors_strings += error_string + '\n'
        self.log_class.error_log(error_string)

    def clear_errors(self):
        self.errors_list = list()
        self.errors_strings = str()
