import os
from datetime import datetime


class Logging:

    def __init__(self, file_name, level='All'):
        """
        For save in log file, with different levels logging
        :param file_name: name log file
        :param level: Level loging: All - save all logs, Error - only errors,
                                    Debug - errors, debug, warning, not save inf.
        """
        self.file_name = file_name
        self.level = level

        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        if not os.path.exists(self.file_name):
            log_file = open(self.file_name, "w")
            log_file.write(f"{datetime.now()} - Start execute" + '\n')
            log_file.close()

    def error_log(self, string):
        log_file = open(self.file_name, "a")
        log_file.write(f"{datetime.now()} - ERROR: " + string + '\n')
        log_file.close()

    def debug_log(self, string):
        if self.level in {"All", "Debug"}:
            log_file = open(self.file_name, "a")
            log_file.write(f"{datetime.now()} - DebugLog: " + string + '\n')
            log_file.close()

    def warning_log(self, string):
        if self.level in {"All", "Debug"}:
            log_file = open(self.file_name, "a")
            log_file.write(f"{datetime.now()} - Warning: " + string + '\n')
            log_file.close()

    def info_log(self, string):
        if self.level in {"All"}:
            log_file = open(self.file_name, "a")
            log_file.write(f"{datetime.now()} - InfoLog: " + string + '\n')
            log_file.close()

    def del_log_file(self):
        os.remove(self.file_name)
